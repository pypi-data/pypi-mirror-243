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
from generax.distributions.flow_models import *

################################################################################################################

if __name__ == '__main__':
  from debug import *
  import matplotlib.pyplot as plt
  from generax.nn.resnet import TimeDependentResNet
  # enable x64
  from jax.config import config
  config.update("jax_enable_x64", True)

  N = 50  # number of data points
  D = 50  # data dimensionality
  K = 50  # latent dimensionality


  key = random.PRNGKey(99)
  key, key_w, key_z, key_eps = random.split(key, 4)
  x_train = jnp.zeros((D, N))
  w = random.normal(key_w, shape=(D, K))
  z = random.normal(key_z, shape=(K, N))
  mean = jnp.dot(w, z).T
  x_train = mean + random.normal(key_eps, mean.shape)
  print("True principal axes:")
  print(w)
  plt.scatter(x_train[:, 0], x_train[:, 1])

  def unpack_sample(s):
      w = s[:D * K].reshape(D, K)
      z = s[D * K:].reshape(K, N)
      return w, z

  def ppca_log_prob(s):
      """
      log p(x, w, z)
      """
      w, z = unpack_sample(s)
      # Prior
      log_pw = jax.scipy.stats.norm.logpdf(w, 0, 1).sum()
      log_pz = jax.scipy.stats.norm.logpdf(z, 0, 1).sum()
      # Likelihood
      log_px_wz = jax.scipy.stats.norm.logpdf(x_train, jnp.dot(w, z).T, 1).sum()
      return log_pw + log_pz + log_px_wz

  gradlogp = jax.grad(ppca_log_prob)

  x_shape = (D * K + K * N,)

  flow = RealNVP(input_shape=(D * K + K * N,),
                    key=key,
                    n_flow_layers=5,
                    n_blocks=4,
                    hidden_size=32,
                    working_size=16)

  p0 = gx.Gaussian(input_shape=x_shape)

  def train_iterator(key, batch_size):
    while True:
      key, _ = random.split(key, 2)
      keys = random.split(key, batch_size)
      yield dict(x=keys)

  def objective(flow, data, key):
    keys = data['x']
    x = eqx.filter_vmap(flow.sample)(keys)
    params, static = eqx.partition(flow, eqx.is_inexact_array)
    no_grad_flow = eqx.combine(jax.lax.stop_gradient(params), static)
    log_px = eqx.filter_vmap(no_grad_flow.log_prob)(x)
    elbo = (log_px - jax.vmap(ppca_log_prob)(x)).mean()

    objective = elbo

    aux = dict(objective=objective,
               elbo=elbo)
    return objective, aux

  train_iter = train_iterator(key, batch_size=128)
  objective(flow, next(train_iter), key)


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
  chain.append(optax.adamw(3e-4))
  chain.append(optax.scale_by_schedule(schedule))
  optimizer = optax.chain(*chain)

  # Create the trainer and optimize
  from generax.trainer import Trainer
  trainer = Trainer(checkpoint_path='tmp/realnvp_vi')
  flow = trainer.train(model=flow,
                        objective=objective,
                        evaluate_model=lambda x: x,
                        optimizer=optimizer,
                        num_steps=5000,
                        double_batch=-1,
                        data_iterator=train_iter,
                        checkpoint_every=5000,
                        test_every=-1,
                        retrain=True)

  elbo = trainer.aux_history['elbo']
  fig, ax = plt.subplots(1, 1)
  ax.plot(elbo)
  ax.set_title('ELBO')
  plt.savefig('misc/realnvp_train_elbo.png')

  import pdb; pdb.set_trace()
