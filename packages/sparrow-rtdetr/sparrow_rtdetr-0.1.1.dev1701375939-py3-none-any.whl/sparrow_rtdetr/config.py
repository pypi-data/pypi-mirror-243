from dataclasses import dataclass


@dataclass
class Config:
    # Backbone
    depth: int = 50
    freeze_at: int = 0
    return_idx: tuple[int, ...] = (1, 2, 3)
    multi_scale: tuple[int, ...] = (
        480,
        512,
        544,
        576,
        608,
        640,
        640,
        640,
        672,
        704,
        736,
        768,
        800,
    )

    # Encoder
    image_size: tuple[int, int] = (640, 640)

    # Decoder
    feat_channels: tuple[int, int, int] = (256, 256, 256)
    num_classes: int = 80

    # PostProcessor
    num_top_queries: int = 300
