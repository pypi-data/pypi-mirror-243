from collections import defaultdict
from time import time_ns
from typing import Any, DefaultDict, Dict, List, Optional, Union
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts.chat import ChatPromptValue
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult

from promptquality.chain_run import chain_run
from promptquality.constants.scorers import Scorers
from promptquality.set_config import set_config
from promptquality.types.chains.node_type import ChainNodeType
from promptquality.types.chains.row import ChainRow
from promptquality.types.config import Config
from promptquality.types.custom_scorer import CustomScorer
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.utils.logger import logger


class GalileoPromptCallback(BaseCallbackHandler):
    def __init__(
        self,
        project_name: Optional[str] = None,
        run_name: Optional[str] = None,
        scorers: Optional[List[Union[Scorers, CustomScorer, RegisteredScorer, str]]] = None,
        config: Optional[Config] = None,
        **kwargs: Any,
    ) -> None:
        """
        LangChain callbackbander for logging prompts to Galileo.

        Parameters
        ----------
        project_name : str
            Name of the project to log to
        """
        # Galileo parameters.
        self.project_name = project_name
        self.run_name = run_name
        self.scorers = scorers
        self.config = config or set_config()

        # Row information.
        # Mapping of root of the chain to all children.
        self.root_child_mapping: DefaultDict = defaultdict(list)
        self.root_nodes: List[UUID] = list()
        # Mapping of parent to children.
        self.parent_child_mapping: DefaultDict = defaultdict(list)
        # Mapping of child to parent.
        self.child_parent_mapping: Dict[UUID, Optional[UUID]] = dict()

        self.chain_inputs: Dict[UUID, Dict[str, Any]] = dict()
        self.serializations: Dict[UUID, Dict[str, Any]] = dict()

        self.rows: Dict[UUID, ChainRow] = dict()

    def set_relationships(self, run_id: UUID, node_type: ChainNodeType, parent_run_id: Optional[UUID] = None) -> None:
        self.child_parent_mapping[run_id] = parent_run_id
        if parent_run_id:
            self.parent_child_mapping[parent_run_id].append(run_id)
        root_id = self.get_root_id(run_id)
        self.root_child_mapping[root_id].append(run_id)
        self.rows[run_id] = ChainRow(
            node_id=run_id,
            node_type=node_type,
            # -1 because the step is incremented after the callback is run.
            step=len(self.root_child_mapping[root_id]) - 1,
            chain_id=parent_run_id,
            chain_root_id=root_id,
        )
        if root_id == run_id:
            self.root_nodes.append(run_id)

    def get_root_id(self, run_id: UUID) -> UUID:
        parent_id = self.child_parent_mapping[run_id]
        if parent_id:
            return self.get_root_id(parent_id)
        else:
            return run_id

    def mark_step_start(
        self,
        run_id: UUID,
        serialized: Dict[str, Any],
        prompt: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        root_id = self.get_root_id(run_id)
        self.rows[run_id].serialized = serialized
        self.rows[run_id].prompt = prompt
        self.rows[run_id].params = kwargs.get("invocation_params", dict())
        self.rows[run_id].inputs = self.chain_inputs.get(root_id, dict())

        # Set the prompt for all of the parent nodes if it isn't set.
        parent_id = self.child_parent_mapping[run_id]
        while parent_id:
            if self.rows[parent_id].prompt is None:
                self.rows[parent_id].prompt = prompt
            parent_id = self.child_parent_mapping.get(parent_id)

    def mark_step_end(self, run_id: UUID, response: Optional[str] = None, **kwargs: Dict[str, Any]) -> None:
        self.rows[run_id].latency = time_ns() - self.rows[run_id].creation_timestamp
        if response:
            self.rows[run_id].response = response
            # Update the output of the parent nodes.
            parent_id = self.child_parent_mapping.get(run_id)
            while parent_id:
                self.rows[parent_id].response = response
                parent_id = self.child_parent_mapping.get(parent_id)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""
        self.set_relationships(run_id, node_type=ChainNodeType.llm, parent_run_id=parent_run_id)
        self.mark_step_start(run_id, serialized, prompts[0], **kwargs)

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        self.set_relationships(run_id, node_type=ChainNodeType.chat, parent_run_id=parent_run_id)

        chat_messages = ChatPromptValue(messages=messages[0])
        self.mark_step_start(run_id, serialized, prompt=chat_messages.to_string(), **kwargs)

    def on_llm_end(
        self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Run when LLM ends running."""

        # Flatten the response and pull out the generation.
        generation = response.flatten()[0].generations[0][0]
        self.mark_step_end(run_id, response=generation.text, **kwargs)

        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.rows[run_id].query_input_tokens = usage.get("prompt_tokens", 0)
            self.rows[run_id].query_output_tokens = usage.get("completion_tokens", 0)
            self.rows[run_id].query_total_tokens = usage.get("total_tokens", 0)

        if generation.generation_info:
            self.rows[run_id].finish_reason = generation.generation_info.get("finish_reason", "")

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM errors."""
        del self.rows[run_id]

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain starts running."""
        self.set_relationships(run_id, node_type=ChainNodeType.chain, parent_run_id=parent_run_id)
        # We only support string inputs.
        self.chain_inputs[run_id] = {k: v for k, v in inputs.items() if isinstance(v, str)}
        self.mark_step_start(run_id, serialized, **kwargs)

    def on_chain_end(
        self, outputs: Union[str, Dict[str, Any]], *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Run when chain ends running."""
        self.rows[run_id].finish_reason = "chain_end"
        response: Optional[str] = None
        if isinstance(outputs, str):
            response = outputs
        elif isinstance(outputs, dict):
            response = outputs.get("text")
        self.mark_step_end(run_id, response=response, **kwargs)

    def on_chain_error(
        self, error: BaseException, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    ) -> Any:
        """Run when chain errors."""

    def finish(self) -> None:
        rows_to_log: List[ChainRow] = list()
        # Exclude chains that don't have children.
        for root_id in self.root_nodes:
            for node_id in self.root_child_mapping[root_id]:
                row = self.rows.get(node_id)
                if row is None:
                    logger.debug(f"Skipping row {node_id} because its row doesn't exist.")
                # If the node is a non-chain node, or is a parent node with any children, include it.
                elif row.node_type != ChainNodeType.chain or node_id in self.parent_child_mapping.keys():
                    rows_to_log.append(row)
                else:
                    logger.debug(f"Skipping row {node_id} because it is an empty chain.")
        chain_run(rows_to_log, self.project_name, self.run_name, self.scorers, config=self.config)
