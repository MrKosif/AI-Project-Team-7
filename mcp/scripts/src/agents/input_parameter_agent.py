from loguru import logger

class InputParameterAgent():
   
    def process(self, state):
        """Process state and determine query type"""
        question = state.get('question', '').strip()
        prompt = self.llm.router_prompt
        classification = self.llm.generate(prompt, {"message": question})

        return {"classification": classification}