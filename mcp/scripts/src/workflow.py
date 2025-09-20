"""Workflow engine for coordinating agents"""
from langgraph.graph import StateGraph, END
from src.state import GraphState
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.tool_selecting_agent import ToolSelectingAgent
from src.agents.tool_executing_agent import ToolExecutingAgent
from src.agents.input_parameter_agent import InputParameterAgent
from src.agents.output_generation_agent import OutputGenerationAgent

from loguru import logger

class WorkflowEngine:
    """Engine for managing workflow between agents"""
    
    def __init__(self, llm_interface=None):
        """Initialize workflow engine"""
        self.llm_interface = llm_interface
        
        # Initialize agents
        #self.orchestrator_agent = OrchestratorAgent(llm_interface)
        #self.tool_selecting_agent = ToolSelectingAgent(llm_interface)
        #self.tool_executing_agent = ToolExecutingAgent(llm_interface)
        #self.input_parameter_agent = InputParameterAgent(llm_interface)
        #self.output_generation_agent = OutputGenerationAgent(llm_interface)

        self.orchestrator_agent = OrchestratorAgent()
        self.tool_selecting_agent = ToolSelectingAgent()
        self.tool_executing_agent = ToolExecutingAgent()
        self.input_parameter_agent = InputParameterAgent()
        self.output_generation_agent = OutputGenerationAgent()

        # Build workflow graph
        self.graph = self._build_graph()
        self.runnable = self.graph.compile()

    
    def _build_graph(self):
        """Build workflow graph with nodes and edges"""
        # Create state graph
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("orchestrator", self.orchestrator_agent.process)
        workflow.add_node("tool_selecting_agent", self.tool_selecting_agent.process)
        workflow.add_node("tool_executing_agent", self.tool_executing_agent.process)
        workflow.add_node("input_parameter_agent", self.input_parameter_agent.process)
        workflow.add_node("output_generation_agent", self.output_generation_agent.process)
        workflow.add_node("generation_router_agent", self.generation_router_agent.process)
        # Add conditional edges from router

        workflow.add_conditional_edges(
            "orchestrator",
            self.orchestrator_agent.route,
            {
                "route_tool_selecting_agent": "tool_selecting_agent", 
                "route_tool_executing_agent": "tool_executing_agent",
                "route_input_parameter_agent": "input_parameter_agent",
                "route_output_generation_agent": "output_generation_agent",
                "error": END
            }
        )
        
        # Add terminal edges
        workflow.add_edge("tool_selecting_agent", "orchestrator")
        workflow.add_edge("tool_executing_agent", "output_generation_agent")
        workflow.add_edge("input_parameter_agent", "orchestrator")
        workflow.add_edge("output_generation_agent", END)
        
        # Set entry point
        workflow.set_entry_point("orchestrator")
        
        return workflow
    
    def process_question(self, question):
        return self.runnable.invoke({"question": question})
