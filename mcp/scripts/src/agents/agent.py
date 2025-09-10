"""Router agent for query classification"""
from scripts.agents.base_agent import BaseAgent
from loguru import logger

class RouterAgent(BaseAgent):
   """Agent for routing user queries to appropriate handlers"""
   
   def process(self, state):
      """Process state and determine query type"""
      question = state.get('question', '').strip()
      prompt = self.llm.router_prompt
      classification = self.llm.generate(prompt, {"message": question})
      
      return {"classification": classification}
   
   def route(self, state):
      """Route based on classification
         Args:state: Current state
         Returns:Next node name
      """
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