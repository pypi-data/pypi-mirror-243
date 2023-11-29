import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable
import einops
import equinox as eqx
from abc import ABC, abstractmethod
import diffrax
from jaxtyping import Array, PRNGKeyArray
import generax as gx
import argparse
import os

################################################################################################################

class Polynomial(eqx.Module):

  coeff: Array
  deg: int = eqx.field(static=True)
  area: float

  def __init__(self, coeff: Array):
    """
    The coefficients are expected to be in the order of increasing degree.
    p(x) = coeff[0] + coeff[1]*x + coeff[2]*x^2 + ...
    """
    assert coeff.ndim == 1
    self.coeff = coeff
    self.deg = self.coeff.shape[0]
    self.area = self.H1(1.0) - self.H1(0.0)

  @staticmethod
  def from_points(x: Array,
                  y: Array,
                  deg: int) -> 'Polynomial':
    coeff = jnp.polyfit(x, y, deg)
    return Polynomial(coeff[::-1])

  def __call__(self, x: Array) -> Array:
    """
    Evaluate p(x)
    """
    return jnp.polyval(self.coeff[::-1], x)

  def H1(self, x: Array) -> Array:
    """
    Anti-derivative of p(x)
    """
    coeff = self.coeff/(1 + jnp.arange(self.deg))
    return jnp.polyval(coeff[::-1], x)*x

  def H2(self, x: Array) -> Array:
    """
    Anti-derivative of x*p(x)
    """
    coeff = self.coeff/(2 + jnp.arange(self.deg))
    return jnp.polyval(coeff[::-1], x)*x**2

  def H3(self, x: Array) -> Array:
    """
    Anti-derivative of (1-x)*p(x)
    """
    coeff = self.coeff*(1/(1 + jnp.arange(self.deg)) - x/(2 + jnp.arange(self.deg)))
    return jnp.polyval(coeff[::-1], x)*x

  def delta_H1(self, x: Array) -> Array:
    """
    H1(1) - H1(x)
    """
    return self.H1(1) - self.H1(x)

  def delta_H2(self, x: Array) -> Array:
    """
    H2(1) - H2(x)
    """
    return self.H2(1) - self.H2(x)

  def delta_H3(self, x: Array) -> Array:
    """
    H3(1) - H3(x)
    """
    return self.H3(1) - self.H3(x)

################################################################################################################

class VINeuralODE(eqx.Module):
  """Neural ODE"""

  p0: gx.ProbabilityDistribution
  vector_field: eqx.Module
  logp: Callable
  gradlogp: Callable
  adjoint: diffrax.AbstractAdjoint
  stepsize_controller: diffrax.AbstractAdaptiveStepSizeController

  interp_points: Array

  def __init__(self,
               p0: gx.ProbabilityDistribution,
               vf: eqx.Module,
               logp: Callable,
               adjoint: Optional[str] = 'recursive_checkpoint',
               controller_rtol: Optional[float] = 1e-3,
               controller_atol: Optional[float] = 1e-5,
               args: argparse.Namespace = None
  ):
    """**Arguments**:

    - `vf`: A function that computes the vector field.  It must output
            a vector of the same shape as its input.
    - `adjoint`: The adjoint method to use.  Can be one of the following:
       - `"recursive_checkpoint"`: Use the recursive checkpoint method.  Doesn't support jvp.
       - `"direct"`: Use the direct method.  Supports jvps.
       - `"seminorm"`: Use the seminorm method.  Does fast backprop through the solver.
    - `controller_rtol`: The relative tolerance of the stepsize controller.
    - `controller_atol`: The absolute tolerance of the stepsize controller.
    """
    self.p0 = p0
    self.vector_field = vf
    self.logp = logp
    self.gradlogp = jax.grad(logp)

    self.interp_points = jnp.array([[0.0, args.weight_start],
                                    [1.0, args.weight_end]])

    if adjoint == 'recursive_checkpoint':
      self.adjoint = diffrax.RecursiveCheckpointAdjoint()
    elif adjoint == 'direct':
      self.adjoint = diffrax.DirectAdjoint()
    elif adjoint == 'seminorm':
      adjoint_controller = diffrax.PIDController(
          rtol=1e-3, atol=1e-6, norm=diffrax.adjoint_rms_seminorm)
      self.adjoint = diffrax.BacksolveAdjoint(stepsize_controller=adjoint_controller)

    self.stepsize_controller = diffrax.PIDController(rtol=controller_rtol, atol=controller_atol)

  def __call__(self, key: PRNGKeyArray) -> Array:
    """**Arguemnts**:
    - `key`: The random key to use to pull samples from the prior.

    **Returns**:
    - `z`: The output of the neural ODE.
    - `log_likelihood`: The log likelihood of the neural ODE if `log_likelihood=True`.
    """
    assert key.shape == (2,)

    # Split the model into its static and dynamic parts so that backprop
    # through the ode solver can be faster.
    params, static = eqx.partition(self.vector_field, eqx.is_array)

    def f(t, x_and_logpx, inputs):
      x, log_qt, kl, total_vf_norm, total_jac_frob_norm = x_and_logpx
      params, interp_points = inputs

      # Recombine the model
      model = eqx.combine(params, static)

      # Fill the model with the current time
      def apply_vf(x):
        return model(t, x)

      # Brute force dlogpx/dt.  See NeuralODE https://arxiv.org/pdf/1806.07366.pdf
      eye = jnp.eye(x.shape[-1])

      def jvp_flat(x, dx):
        return jax.jvp(apply_vf, (x,), (dx,))

      dxdt, dutdxt = jax.vmap(jvp_flat, in_axes=(None, 1), out_axes=1)(x, eye)
      dxdt = dxdt[:, 0]
      dlogpxdt = -jnp.trace(dutdxt)

      weighting = Polynomial.from_points(x=interp_points[:,0],
                                         y=interp_points[:,1],
                                         deg=1)
      dh1 = weighting.delta_H1(t)
      dh2 = weighting.delta_H2(t)
      dh3 = weighting.delta_H3(t)

      check = dh1 - dh2
      import pdb; pdb.set_trace()

      gradlogp0 = jax.grad(self.p0.log_prob)(x)
      gradlogpx = self.gradlogp(x)
      dkldt = -dh3*jnp.vdot(gradlogp0, dxdt)
      dkldt += -dh2*jnp.vdot(gradlogpx, dxdt)
      dkldt += dh1*dlogpxdt

      # Normalize by a constant
      dkldt /= weighting.area
      assert dkldt.shape == ()

      dtjfndt = jnp.sum(dutdxt**2)
      dvfnormdt = jnp.sum(dxdt**2)

      return dxdt, dlogpxdt, dkldt, dvfnormdt, dtjfndt

    term = diffrax.ODETerm(f)
    solver = diffrax.Dopri5()

    # Determine which times we want to save the neural ODE at.
    k1, k2 = random.split(key, 2)
    t0, t1 = 0.0, 1.0
    saveat = diffrax.SaveAt(ts=[t1])

    x0, log_q0 = self.p0.sample_and_log_prob(k2)
    log_q1 = log_q0
    kl = jnp.array(0.0)
    total_vf_norm = jnp.array(0.0)
    total_jac_frob_norm = jnp.array(0.0)

    y0 = (x0,
          log_q1,
          kl,
          total_vf_norm,
          total_jac_frob_norm)
    args = (params, self.interp_points)
    f(jnp.array(0.4), y0, args)

    # Run the ODE solver
    solution = diffrax.diffeqsolve(term,
                                   solver,
                                   saveat=saveat,
                                   t0=t0,
                                   t1=t1,
                                   dt0=0.001,
                                   y0=y0,
                                   args=args,
                                   adjoint=self.adjoint,
                                   stepsize_controller=self.stepsize_controller,
                                   throw=True,
                                   max_steps=4096)
    outs = solution.ys

    # Only take the first time
    outs = jax.tree_util.tree_map(lambda x: x[0], outs)
    z, log_q1, kl, total_vf_norm, total_jac_frob_norm = outs
    return z, log_q1, kl, total_vf_norm, total_jac_frob_norm

################################################################################################################

class GMM(gx.ProbabilityDistribution):

  means: float
  def __init__(self, means: int, **kwargs):
    self.means = means
    super().__init__(**kwargs)

  def log_prob(self,
                x: Array,
                y: Optional[Array] = None,
                key: Optional[PRNGKeyArray] = None) -> Array:
    assert x.ndim == 1

    logp1 = jax.scipy.stats.norm.logpdf(x, self.means, 1).sum()
    logp2 = jax.scipy.stats.norm.logpdf(x, -self.means, 1).sum()
    logp = jnp.logaddexp(logp1, logp2) - jnp.log(2)
    assert logp.shape == ()
    return logp

  def sample_and_log_prob(self,
                          key: PRNGKeyArray,
                          y: Optional[Array] = None) -> Array:
    dim = self.input_shape[0]
    k1, k2, k3 = random.split(key, 3)
    x0, x1 = random.normal(k1, shape=(2,) + x_shape)
    x0 = x0 + self.means
    x1 = x1 - self.means
    u = random.uniform(k2, shape=())
    x = jnp.where(u > 0.5, x0, x1)
    return x, self.log_prob(x)

################################################################################################################

if __name__ == '__main__':
  from debug import *
  import matplotlib.pyplot as plt
  from generax.nn.resnet import TimeDependentResNet
  # enable x64
  from jax.config import config

  # take some command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--means', type=float, default=8.0)
  parser.add_argument('--weight_start', type=float, default=1.0)
  parser.add_argument('--weight_end', type=float, default=0.1)
  args = parser.parse_args()

  folder_name = f'misc/vi/cnf_gmm_{args.weight_start}_{args.weight_end}'
  folder_name = folder_name.replace('.', '_')
  gx.util.ensure_path_exists(folder_name)

  key = random.PRNGKey(0)
  x_shape = (2,)

  p0 = gx.Gaussian(input_shape=x_shape)
  p1 = GMM(means=8, input_shape=x_shape)

  if False:
    x_range, y_range = jnp.linspace(-15, 15, 100), jnp.linspace(-15, 15, 100)
    x_grid, y_grid = jnp.meshgrid(x_range, y_range)
    xy = jnp.stack([x_grid, y_grid], axis=-1)
    xy = xy.reshape((-1, 2))
    logp = eqx.filter_vmap(p1.log_prob)(xy)
    logp = logp.reshape(x_grid.shape)

    logp0 = eqx.filter_vmap(p0.log_prob)(xy)
    logp0 = logp0.reshape(x_grid.shape)

    betas = jnp.linspace(0.0, 1.0, 10)
    n_cols = 5
    n_rows = int(jnp.ceil(len(betas)/n_cols))
    size = 4
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*size, n_rows*size))
    ax_iter = iter(axes.ravel())
    for i, beta in enumerate(betas):
      ax = next(ax_iter)

      k1, k2 = random.split(key, 2)
      a_points = random.uniform(k1, shape=(10, 2)) - 0.5
      b_points = random.uniform(k2, shape=(10, 2)) - 0.5
      a_points = a_points.at[0].set(1.0)
      a_points = a_points.at[-1].set(0.0)

      b_points = b_points.at[0].set(0.0)
      b_points = b_points.at[-1].set(1.0)

      a = Polynomial.from_points(x=a_points[:,0],
                                  y=a_points[:,1],
                                  deg=9)
      b = Polynomial.from_points(x=b_points[:,0],
                                  y=b_points[:,1],
                                  deg=9)

      a_line = a(jnp.linspace(0, 1, 10))
      b_line = b(jnp.linspace(0, 1, 10))

      # ax.contourf(x_grid, y_grid, jnp.exp(a(beta)*logp0 + b(beta)*logp), levels=100)
      # ax.contourf(x_grid, y_grid, jnp.exp((1-3.5*beta*(1-beta))*((1-beta)*logp0 + beta*logp)), levels=100)
      ax.contourf(x_grid, y_grid, jnp.exp((1-beta)*logp0 + beta**2*logp), levels=100)
      ax.set_title(f'beta={beta:.2f}')
    plt.show()
    import pdb; pdb.set_trace()


  vf = TimeDependentResNet(input_shape=x_shape,
                            working_size=16,
                            hidden_size=32,
                            out_size=x_shape[-1],
                            n_blocks=3,
                            cond_shape=None,
                            embedding_size=16,
                            out_features=32,
                            key=key)

  def train_iterator(key, batch_size):
    while True:
      key, _ = random.split(key, 2)
      keys = random.split(key, batch_size)
      yield dict(x=keys)

  def objective(vf, data, key):
    keys = data['x']
    opt_model = VINeuralODE(p0,
                            vf,
                            p1.log_prob,
                            adjoint='seminorm',
                            controller_rtol=1e-5,
                            controller_atol=1e-5,
                            args=args)
    z, log_qz, kl, total_vf_norm, total_jac_frob_norm = eqx.filter_vmap(opt_model)(keys)
    kl = kl
    elbo = eqx.filter_vmap(p1.log_prob)(z) - log_qz

    objective = kl + 0.01*(total_vf_norm + total_jac_frob_norm)
    objective = objective.mean()

    aux = dict(objective=objective,
               kl=kl,
               log_qz=log_qz,
               vf_norm=total_vf_norm,
               jac_norm=total_jac_frob_norm,
               elbo=elbo)
    aux = jax.tree_util.tree_map(lambda x: x.mean(), aux)
    return objective, aux

  train_iter = train_iterator(key, batch_size=1024)
  objective(vf, next(train_iter), key)

  # Create the optimizer
  import optax
  schedule = optax.warmup_cosine_decay_schedule(init_value=0.0,
                                    peak_value=1.0,
                                    warmup_steps=1000,
                                    decay_steps=3e5,
                                    end_value=0.1,
                                    exponent=1.0)
  chain = []
  chain.append(optax.clip_by_global_norm(15.0))
  chain.append(optax.adamw(1e-3))
  chain.append(optax.scale_by_schedule(schedule))
  optimizer = optax.chain(*chain)

  # Create the trainer and optimize
  from generax.trainer import Trainer
  trainer = Trainer(checkpoint_path=os.path.join(folder_name, 'model'))
  vf = trainer.train(model=vf,
                        objective=objective,
                        evaluate_model=lambda x: x,
                        optimizer=optimizer,
                        num_steps=5000,
                        double_batch=-1,
                        data_iterator=train_iter,
                        checkpoint_every=500,
                        test_every=-1,
                        retrain=True,
                        just_load=False)

  from generax.distributions.flow_models import *
  flow = ContinuousNormalizingFlow(input_shape=x_shape,
                                    net=vf,
                                    key=key,
                                    controller_atol=1e-5,
                                    controller_rtol=1e-5)
  ts = jnp.linspace(0, 1, 6)

  def ode_solve(x0):
    solution = flow.transform.neural_ode(x0,
                                inverse=True,
                                log_likelihood=True,
                                save_at=ts)
    return solution.ys, solution.log_det

  n_samples = 1000
  keys = random.split(key, n_samples)
  x0, log_p0s = eqx.filter_vmap(flow.prior.sample_and_log_prob)(keys)
  xts, log_dets = jax.vmap(ode_solve)(x0)
  log_pxs = log_p0s[:,None] - log_dets

  n_rows, n_cols = 1, ts.shape[0]
  size = 4
  fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*size, n_rows*size))
  for i in range(n_cols):
    axes[i].scatter(*xts[:, i].T, c=jnp.exp(log_pxs[:, i]), alpha=0.5, s=10)
    axes[i].set_title(f"t={ts[i]:.2f}")
    axes[i].set_aspect('equal', 'box')

  plot_folder = os.path.join(folder_name, 'plots')
  gx.util.ensure_path_exists(plot_folder)

  plt.savefig(os.path.join(plot_folder, 'gmm_ppath_elbo.png'))
  plt.close()


  n_rows, n_cols = 1, len(trainer.aux_history)
  size = 4
  fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*size, n_rows*size))
  for i, (key, val) in enumerate(trainer.aux_history.items()):
    axes[i].plot(val)
    axes[i].set_title(key)

  plt.savefig(os.path.join(plot_folder, 'train_elbo_gmm.png'))
