# Written by @lyuwenyu
# Licensed under Apache License 2.0
import torch.distributed as tdist
import torch.nn as nn


def get_activation(act: str, inpace: bool = True) -> nn.Module:
    """Convert a string activation name to a torch.nn.Module activation object."""
    act = act.lower()

    if act == "silu":
        m = nn.SiLU()

    elif act == "relu":
        m = nn.ReLU()

    elif act == "leaky_relu":
        m = nn.LeakyReLU()

    elif act == "silu":
        m = nn.SiLU()

    elif act == "gelu":
        m = nn.GELU()

    elif act is None:
        m = nn.Identity()

    elif isinstance(act, nn.Module):
        m = act

    else:
        raise RuntimeError("")

    if hasattr(m, "inplace"):
        m.inplace = inpace

    return m


def is_dist_available_and_initialized():
    if not tdist.is_available():
        return False
    if not tdist.is_initialized():
        return False
    return True


def get_world_size():
    if not is_dist_available_and_initialized():
        return 1
    return tdist.get_world_size()
