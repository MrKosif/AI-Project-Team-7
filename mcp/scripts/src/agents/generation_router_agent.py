from loguru import logger

class GenerationRouterAgent():
   
    def process(self, state):
        """Process state and determine query type"""
        question = state.get('question', '').strip()
        prompt = self.llm.router_prompt
        classification = self.llm.generate(prompt, {"message": question})

        return {"classification": classification}
    
    def route(self, state):
        classification = state.get("classification", "").strip()
        try:
            if classification == "selamlama":
                logger.info("The prompt has been classified as greetings")
                return "say_hello"
            elif classification == "rag":
                logger.info("The prompt has been classified as rag")
                return "call_agent"
            else:
                return "error"
        except Exception as e:
            logger.error(f"There has been an error with classification routing. \n {e}")
            return "error"