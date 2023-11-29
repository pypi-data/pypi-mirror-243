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


class VINeuralODE(eqx.Module):
  """Neural ODE"""

  p0: gx.ProbabilityDistribution
  vector_field: eqx.Module
  gradlogp: Callable
  adjoint: diffrax.AbstractAdjoint
  stepsize_controller: diffrax.AbstractAdaptiveStepSizeController

  def __init__(self,
               p0: gx.ProbabilityDistribution,
               vf: eqx.Module,
               gradlogp: Callable,
               adjoint: Optional[str] = 'recursive_checkpoint',
               controller_rtol: Optional[float] = 1e-3,
               controller_atol: Optional[float] = 1e-5,
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
    self.gradlogp = gradlogp

    if adjoint == 'recursive_checkpoint':
      self.adjoint = diffrax.RecursiveCheckpointAdjoint()
    elif adjoint == 'direct':
      self.adjoint = diffrax.DirectAdjoint()
    elif adjoint == 'seminorm':
      adjoint_controller = diffrax.PIDController(
          rtol=1e-3, atol=1e-6, norm=diffrax.adjoint_rms_seminorm)
      self.adjoint = diffrax.BacksolveAdjoint(
          stepsize_controller=adjoint_controller)

    self.stepsize_controller = diffrax.PIDController(
        rtol=controller_rtol, atol=controller_atol)

  def __call__(self,
               key: PRNGKeyArray) -> Array:
    """**Arguemnts**:
    - `key`: The random key to use to pull samples from the prior.

    **Returns**:
    - `z`: The output of the neural ODE.
    - `log_likelihood`: The log likelihood of the neural ODE if `log_likelihood=True`.
    """
    assert key.shape == (2,)
    k1, k2 = random.split(key, 2)

    # Split the model into its static and dynamic parts so that backprop
    # through the ode solver can be faster.
    params, static = eqx.partition(self.vector_field, eqx.is_array)

    def f(t, x_and_logpx, params):
      x, log_px, kl = x_and_logpx

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

      log_p0 = self.p0.log_prob(x)
      gradlogpx = self.gradlogp(x)
      dkldt = -0.5*(1-t)**2*jnp.vdot(log_p0, dxdt)
      dkldt += -0.5*(1-t)*(1+t)*jnp.vdot(gradlogpx, dxdt)
      dkldt += (1-t)*dlogpxdt

      # dkldt = -jnp.vdot(gradlogpx, dxdt) + dlogpxdt

      return dxdt, dlogpxdt, dkldt

    term = diffrax.ODETerm(f)
    solver = diffrax.Dopri5()

    # Determine which times we want to save the neural ODE at.
    t0, t1 = 0.0, 1.0
    saveat = diffrax.SaveAt(ts=[t1])

    x0, log_px0 = self.p0.sample_and_log_prob(k2)
    log_det = jnp.array(0.0)
    kl = jnp.array(0.0)

    # Run the ODE solver
    solution = diffrax.diffeqsolve(term,
                                   solver,
                                   saveat=saveat,
                                   t0=t0,
                                   t1=t1,
                                   dt0=0.0001,
                                   y0=(x0, log_det, kl),
                                   args=params,
                                   adjoint=self.adjoint,
                                   stepsize_controller=self.stepsize_controller,
                                   throw=True,
                                   max_steps=4096)
    outs = solution.ys

    # Only take the first time
    outs = jax.tree_util.tree_map(lambda x: x[0], outs)
    z, log_det, kl = outs
    log_px = log_px0 + log_det
    return z, log_px, kl

################################################################################################################


if __name__ == '__main__':
  from debug import *
  import matplotlib.pyplot as plt
  from generax.nn.resnet import TimeDependentResNet
  # enable x64
  from jax.config import config
  config.update("jax_enable_x64", True)

  key = random.PRNGKey(0)
  x_shape = (10,)

  def funnel(x):
    assert x.ndim == 1
    x0, x1 = x[0], x[1:]
    logp = jax.scipy.stats.norm.logpdf(x0, 0, 3).sum()
    logp += jax.scipy.stats.norm.logpdf(x1, 0, jnp.exp(x0 / 2)).sum()
    return logp

  gradlogp = jax.grad(funnel)

  vf = TimeDependentResNet(input_shape=x_shape,
                           working_size=16,
                           hidden_size=32,
                           out_size=x_shape[-1],
                           n_blocks=4,
                           cond_shape=None,
                           embedding_size=16,
                           out_features=32,
                           key=key)

  p0 = gx.Gaussian(input_shape=x_shape)

  def train_iterator(key, batch_size):
    while True:
      key, _ = random.split(key, 2)
      keys = random.split(key, batch_size)
      yield dict(x=keys)

  def objective(vf, data, key):
    keys = data['x']
    opt_model = VINeuralODE(p0,
                            vf,
                            gradlogp,
                            adjoint='recursive_checkpoint',
                            controller_rtol=1e-5,
                            controller_atol=1e-5)
    z, log_px, kl = jax.vmap(opt_model)(keys)
    kl = kl.mean()
    elbo = (log_px - jax.vmap(funnel)(z)).mean()

    objective = kl

    aux = dict(objective=objective,
               kl=kl,
               elbo=elbo)
    return objective, aux

  train_iter = train_iterator(key, batch_size=128)
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
  trainer = Trainer(checkpoint_path='tmp/funnel_temp')
  vf = trainer.train(model=vf,
                     objective=objective,
                     evaluate_model=lambda x: x,
                     optimizer=optimizer,
                     num_steps=2000,
                     double_batch=-1,
                     data_iterator=train_iter,
                     checkpoint_every=5000,
                     test_every=-1,
                     retrain=True,
                     just_load=False)

  # Pull samples
  from generax.distributions.flow_models import ContinuousNormalizingFlow
  flow = ContinuousNormalizingFlow(input_shape=x_shape,
                                   net=vf,
                                   key=key,
                                   controller_atol=1e-5,
                                   controller_rtol=1e-5)
  keys = random.split(key, 1000)
  samples = eqx.filter_vmap(flow.sample)(keys)
  y, x = samples[:,0], samples[:,1]
  plt.scatter(x, y)
  plt.savefig('misc/funnel_samples_temp2.png')
  import pdb; pdb.set_trace()

  kl = trainer.aux_history['kl']
  elbo = trainer.aux_history['elbo']
  fig, (ax1, ax2) = plt.subplots(1, 2)
  ax1.plot(kl)
  ax1.set_title('KL')
  ax2.plot(elbo)
  ax2.set_title('ELBO')
  plt.savefig('misc/funnel_kl.png')

  import pdb
  pdb.set_trace()
