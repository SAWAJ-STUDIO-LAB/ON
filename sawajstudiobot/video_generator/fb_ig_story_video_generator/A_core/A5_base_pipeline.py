# Re-export universal BasePipeline (Story variant)
from universal.U4_base_pipeline import BasePipeline as _BasePipeline


class BasePipeline(_BasePipeline):
    """Story-specific BasePipeline — includes all status keys."""
    pass


__all__ = ["BasePipeline"]
