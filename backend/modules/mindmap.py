import logging
from typing import List
from backend.gemini_client import gemini_client
from backend.schemas.mindmap import MindMapRequest, MindMapResponse, MindMapNode
from backend.utils.prompts import MINDMAP_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def generate_mindmap(request: MindMapRequest) -> MindMapResponse:
    """
    Generates a structured hierarchical mind map for visual topic exploration.
    """
    topic = request.topic.strip()
    prompt = MINDMAP_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        topic=topic
    )

    try:
        raw_data = gemini_client.generate_json(prompt, temperature=0.5)
        nodes_raw = []
        if isinstance(raw_data, dict):
            nodes_raw = raw_data.get("nodes", [])
        elif isinstance(raw_data, list):
            nodes_raw = raw_data

        parsed_nodes: List[MindMapNode] = []
        for item in nodes_raw:
            if not isinstance(item, dict):
                continue
            nid = str(item.get("id", f"node_{len(parsed_nodes)}")).strip()
            lbl = str(item.get("label", "Concept")).strip()
            desc = str(item.get("description", "")).strip()
            parent = item.get("parent_id")
            parent_str = str(parent).strip() if parent else None

            if nid and lbl:
                parsed_nodes.append(
                    MindMapNode(id=nid, label=lbl, description=desc, parent_id=parent_str)
                )

        if not parsed_nodes:
            parsed_nodes = [
                MindMapNode(id="root", label=topic, description=f"Central topic of {topic}.", parent_id=None),
                MindMapNode(id="sub_1", label="Foundations", description="Core concepts and principles.", parent_id="root"),
                MindMapNode(id="sub_2", label="Applications", description="Practical usage & examples.", parent_id="root"),
                MindMapNode(id="sub_3", label="Advanced Topics", description="Deep dive and research.", parent_id="root")
            ]

        return MindMapResponse(topic=topic, nodes=parsed_nodes)

    except Exception as err:
        logger.error(f"Error generating mind map: {err}")
        return MindMapResponse(
            topic=topic,
            nodes=[
                MindMapNode(id="root", label=topic, description=f"Central theme: {topic}", parent_id=None),
                MindMapNode(id="node_1", label="Overview", description="Primary definitions", parent_id="root"),
                MindMapNode(id="node_2", label="Core Mechanisms", description="Key working principles", parent_id="root"),
                MindMapNode(id="node_3", label="Key Examples", description="Real world applications", parent_id="root")
            ]
        )
