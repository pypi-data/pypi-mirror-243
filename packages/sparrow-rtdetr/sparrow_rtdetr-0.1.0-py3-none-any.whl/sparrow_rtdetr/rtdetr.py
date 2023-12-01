# Written by @lyuwenyu
# Licensed under Apache License 2.0
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .backbone import PResNet
from .config import Config
from .decoder import RTDETRTransformer
from .encoder import HybridEncoder
from .post_processor import PostProcessor

__all__ = ["RTDETR"]


class RTDETR(nn.Module):
    __inject__ = ["backbone", "encoder", "decoder"]

    def __init__(
        self,
        num_classes: int = Config.num_classes,
        image_size: tuple[int, int] = Config.image_size,
    ):
        super().__init__()
        self.backbone = PResNet(
            depth=Config.depth,
            freeze_at=Config.freeze_at,
            return_idx=Config.return_idx,
            pretrained=True,
        )
        self.encoder = HybridEncoder(eval_spatial_size=image_size)
        self.decoder = RTDETRTransformer(
            num_classes=num_classes,
            feat_channels=Config.feat_channels,
            eval_spatial_size=image_size,
        )
        self.orig_target_size = torch.tensor(image_size)
        self.postprocessor = PostProcessor(
            num_classes=num_classes,
            num_top_queries=Config.num_top_queries,
        )

    def forward(self, x, targets=None):
        if self.training:
            sz = np.random.choice(Config.multi_scale)
            x = F.interpolate(x, size=[sz, sz])

        x = self.backbone(x)
        x = self.encoder(x)
        x = self.decoder(x, targets)

        if not self.training:
            x = self.postprocessor(x, self.orig_target_size)

        return x

    def deploy(self):
        self.eval()
        for m in self.modules():
            if hasattr(m, "convert_to_deploy"):
                m.convert_to_deploy()
        return self
