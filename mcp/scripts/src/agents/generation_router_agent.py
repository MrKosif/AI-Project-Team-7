from loguru import logger

class GenerationRouterAgent():

    def process(self)
   
    def route(self, state):
        """Process state and determine query type"""
        input_status = state.get('input_status', '').strip()
        answer_status = state.get('answer_status', '').strip()

        if input_status == "missing" or answer_status == "missing":
            return "route_output_generation_agent"
            print("Routing to Output Generation Agent due to missing input or answer status.")
        else:
            return "route_orchestrator"
            print("Routing back to Orchestrator as all statuses are present.")

        return {"classification": classification}