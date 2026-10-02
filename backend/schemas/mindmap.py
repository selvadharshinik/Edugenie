from typing import List, Optional
from pydantic import BaseModel, Field

class MindMapRequest(BaseModel):
    topic: str = Field(..., min_length=2, description="Central topic for mind map generation.")

class MindMapNode(BaseModel):
    id: str = Field(..., description="Unique node ID.")
    label: str = Field(..., description="Node label/title.")
    description: str = Field(default="", description="Brief description or detail.")
    parent_id: Optional[str] = Field(None, description="ID of parent node (None for root node).")

class MindMapResponse(BaseModel):
    topic: str = Field(..., description="Central root topic.")
    nodes: List[MindMapNode] = Field(..., description="List of hierarchical nodes forming the mind map.")
