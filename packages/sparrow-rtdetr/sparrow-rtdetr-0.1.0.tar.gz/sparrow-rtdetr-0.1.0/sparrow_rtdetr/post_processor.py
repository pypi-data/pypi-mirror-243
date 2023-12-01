# Written by @lyuwenyu
# Licensed under Apache License 2.0
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

__all__ = ["PostProcessor"]


class PostProcessor(nn.Module):
    """Post processor for RT-DETR. used for inference."""

    __share__ = ["num_classes", "use_focal_loss", "num_top_queries"]

    def __init__(self, num_classes=80, num_top_queries=300) -> None:
        super().__init__()
        self.num_top_queries = num_top_queries
        self.num_classes = num_classes
        self.deploy_mode = False

    def extra_repr(self) -> str:
        return f"num_classes={self.num_classes}, num_top_queries={self.num_top_queries}"

    # def forward(self, outputs, orig_target_sizes):
    def forward(self, outputs, orig_target_sizes):
        logits, boxes = outputs["pred_logits"], outputs["pred_boxes"]
        # orig_target_sizes = torch.stack([t["orig_size"] for t in targets], dim=0)

        bbox_pred = torchvision.ops.box_convert(boxes, in_fmt="cxcywh", out_fmt="xyxy")
        bbox_pred *= orig_target_sizes.repeat(1, 2).unsqueeze(1)

        scores = F.sigmoid(logits)
        scores, index = torch.topk(scores.flatten(1), self.num_top_queries, axis=-1)
        labels = index % self.num_classes
        index = index // self.num_classes
        boxes = bbox_pred.gather(
            dim=1, index=index.unsqueeze(-1).repeat(1, 1, bbox_pred.shape[-1])
        )

        # TODO for onnx export
        if self.deploy_mode:
            return labels, boxes, scores

        return {"boxes": boxes, "labels": labels, "scores": scores}

    def deploy(self):
        self.eval()
        self.deploy_mode = True
        return self

    @property
    def iou_types(self):
        return ("bbox",)
