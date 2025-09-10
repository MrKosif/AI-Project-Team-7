"""
State definitions for workflow engine
"""
from typing import TypedDict, Optional

class GraphState(TypedDict):
  """State representation for the workflow graph"""
  conversation_history: list[str]
  current_user_query: str
  selected_tool: Optional[str]
  tool_inputs: Optional[dict[str, any]]
  tool_result: Optional[str]
  available_tools: list[dict[str, any]]
  input_status: Optional[str]
  answer_status: Optional[str]


  