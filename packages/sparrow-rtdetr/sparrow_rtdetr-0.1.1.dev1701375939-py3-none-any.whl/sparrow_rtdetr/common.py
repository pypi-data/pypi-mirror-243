# Written by @lyuwenyu
# Licensed under Apache License 2.0
import torch.nn as nn

from .utils import get_activation


class ConvNormLayer(nn.Module):
    def __init__(
        self, ch_in, ch_out, kernel_size, stride, padding=None, bias=False, act=None
    ):
        super().__init__()
        self.conv = nn.Conv2d(
            ch_in,
            ch_out,
            kernel_size,
            stride,
            padding=(kernel_size - 1) // 2 if padding is None else padding,
            bias=bias,
        )
        self.norm = nn.BatchNorm2d(ch_out)
        self.act = nn.Identity() if act is None else get_activation(act)

    def forward(self, x):
        return self.act(self.norm(self.conv(x)))
