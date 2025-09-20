from loguru import logger
from src.prompts import prompts
from src.model import GeminiFlash25

class OrchestratorAgent():

    def __init__(self):
        self.llm = GeminiFlash25()
   
    def process(self, state):
        """Process state and determine query type"""
        conversation_history = state.get('conversation_history', '').strip()
        current_user_query = state.get('current_user_query', '').strip()
        selected_tool = state.get('selected_tool', '').strip()
        tool_inputs = state.get('tool_inputs', '').strip()
        tool_result = state.get('tool_result', '').strip()
        available_tools = state.get('available_tools', '').strip()
        input_status = state.get('input_status', '').strip()
        answer_status = state.get('answer_status', '').strip()

        prompt = prompts._init_orchestrator_prompt()
        full_prompt = prompt.format(user_question=current_user_query,
                                    conversation_history=conversation_history,
                                    selected_tool=selected_tool,
                                    tool_inputs=tool_inputs,
                                    tool_result=tool_result,
                                    available_tools=available_tools,
                                    input_status=input_status,
                                    answer_status=answer_status)
        routed_agent = self.llm.ask_question(full_prompt)

        return {"routed_agent": routed_agent}
   
    def route(self, state):
        routed_agent = state.get('routed_agent', '').strip()

        try:
            if routed_agent == "tool_selecting_agent":
                logger.info("tool_selecting_agent has been selected by the orchestrator")
                return "route_tool_selecting_agent"
            
            elif routed_agent == "tool_executing_agent":
                logger.info("tool_executing_agent has been selected by the orchestrator")
                return "route_tool_executing_agent"



            else:
                return "error"
        except Exception as e:
            logger.error(f"There has been an error with classification routing. \n {e}")
            return "error"