from time import time_ns
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from promptquality.types.chains.node_type import ChainNodeType
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.types.run import ScorersConfiguration


class ChainRow(BaseModel):
    """
    Chains are constructed of `ChainRow`s. Each ChainRow represents a node in the chain and are modeled as a tree.

    Each chain has a root node, which is the first node in the chain. Each non-root node in the chain has a parent node.
    Parent nodes are necessarily chain nodes.

    The required fields for a chain row are `node_id`, `node_type`, `chain_root_id`, and `step`. The remaining fields
    are optional and are populated as the chain is executed.
    """

    node_id: UUID = Field(description="ID of that node in the chain. This maps to `run_id` from `langchain`.")
    node_type: ChainNodeType = Field(description="Type of node in the chain.")
    # Chain fields.
    chain_root_id: UUID = Field(description="ID of the root node in the chain.")
    chain_id: Optional[UUID] = Field(
        default=None,
        description="ID of the parent node of the current node. This maps to `parent_run_id` from `langchain`.",
    )
    step: int = Field(
        description="Step in the chain. This is always increasing. The root node is step 1, with other nodes incrementing from there."
    )
    serialized: Optional[dict] = Field(
        default=None,
        description="Serialized version of the node This is typically a JSON field that contains the structure for the step.",
    )
    # Inputs and prompt.
    inputs: Optional[dict] = Field(default=None, description="Inputs to the node.")
    prompt: Optional[str] = Field(default=None, description="Prompt for the node.")
    # Response fields.
    response: Optional[str] = Field(default=None, description="Response received after the node's execution.")
    creation_timestamp: int = Field(default_factory=time_ns, description="Timestamp when the node was created.")
    finish_reason: str = Field(default="", description="Reason for the node's completion.")
    latency: Optional[int] = Field(default=None, description="Latency of the node's execution.")
    query_input_tokens: int = Field(default=0, description="Number of tokens in the query input.")
    query_output_tokens: int = Field(default=0, description="Number of tokens in the query output.")
    query_total_tokens: int = Field(default=0, description="Total number of tokens in the query.")
    # Metadata.
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters passed to the node.")

    # Ignore extra fields.
    model_config = ConfigDict(extra="ignore", validate_assignment=True)


class ChainIngestRequest(BaseModel):
    rows: List[ChainRow] = Field(default_factory=list)
    prompt_scorers_configuration: Optional[ScorersConfiguration] = Field(default=None, validate_default=True)
    prompt_registered_scorers_configuration: Optional[List[RegisteredScorer]] = Field(
        default=None, validate_default=True
    )


class ChainIngestResponse(BaseModel):
    num_rows: int
    message: str
