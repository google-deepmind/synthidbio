"""Hashing function implementation."""

import torch


def accumulate_hash(
    current_hash: torch.LongTensor,
    data: torch.LongTensor,
    multiplier: int = 6364136223846793005,
    increment: int = 1,
) -> torch.LongTensor:
  """Accumulate hash of data on current hash.

  Method uses adapted linear congruential generator (LCG)with newlib/musl
  parameters.

  This function has following property -
  f(x, data[T]) = f(f(x, data[:T - 1]), data[T])

  This function expects current_hash.shape and data.shape[:-1] to
  match/broadcastable.

  Args:
    current_hash: (shape,)
    data: (shape, tensor_len)
    multiplier: (int) multiplier of linear congruential generator
    increment: (int) increment of linear congruential generator

  Returns:
    updated hash (shape,)
  """
  for i in range(data.shape[-1]):
    current_hash = torch.add(current_hash, data[..., i])
    current_hash = torch.mul(current_hash, multiplier)
    current_hash = torch.add(current_hash, increment)
  return current_hash
