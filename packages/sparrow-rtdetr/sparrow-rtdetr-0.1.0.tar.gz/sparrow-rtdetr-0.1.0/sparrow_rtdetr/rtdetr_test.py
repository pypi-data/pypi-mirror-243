import torch

from .loss import SetCriterion
from .rtdetr import RTDETR


def test_320x320_resolution():
    model = RTDETR(image_size=(320, 320)).eval()
    model(torch.rand((1, 3, 320, 320)))


def test_compute_loss():
    model = RTDETR().train()
    criterion = SetCriterion(
        weight_dict={"loss_vfl": 1, "loss_bbox": 5, "loss_giou": 2},
        losses=["vfl", "boxes"],
        alpha=0.75,
        gamma=2.0,
    )
    targets = [
        {"boxes": torch.rand((4, 4)) * 640, "labels": torch.randint(0, 80, (4,))}
    ]
    outputs = model(torch.rand((1, 3, 640, 640)), targets)
    criterion(outputs, targets)
