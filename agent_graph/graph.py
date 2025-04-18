import json
import logging
from typing import Any
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

from agents.agents import ReservationAgent
from agents.tools_agents import (
    FetchReservationsAgent,
    AddReservationAgent,
    UpdateReservationAgent,
    DeleteReservationAgent,
    CheckAvailabilityAgent,
    EndNodeAgent
)
from agents.router_agent import RouterAgent, DataExtractorAgent
from states.state import AgentGraphState
from prompts.prompts import RESERVATION_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0.5, tools=None, session=None):
    graph = StateGraph(AgentGraphState)

    # ----- Async Düğümler -----
    async def reservation_agent_node(state):
        return await ReservationAgent(
            state=state,
            model=model,
            server=server,
            model_endpoint=model_endpoint,
            stop=stop,
            guided_json=None,
            temperature=temperature,
            session=session,
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            prompt=RESERVATION_SYSTEM_PROMPT,
            tools=tools,
            feedback=state['reservation_response'],
        )

    async def data_extractor_node(state):
        return await DataExtractorAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_response=lambda: state.get('reservation_response', [])
        )

    async def router_node(state):
        return await RouterAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_response=lambda: state.get('reservation_response', [])
        )

    async def fetch_reservations_node(state):
        return await FetchReservationsAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            customer_data=lambda: state.get('reservation_query', [])
        )

    async def add_reservation_node(state):
        return await AddReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_data=lambda: state.get('new_reservation', [])
        )

    async def update_reservation_node(state):
        return await UpdateReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            update_data=lambda: state.get('update_reservation', [])
        )

    async def delete_reservation_node(state):
        return await DeleteReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            delete_data=lambda: state.get('delete_reservation', [])
        )

    async def check_availability_node(state):
        return await CheckAvailabilityAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            availability_data=lambda: state.get('availability_check', [])
        )

    async def end_node(state):
        return await EndNodeAgent(
            state=state,
            model=model,
            server=server
        ).invoke()

    # ----- Düğümleri ekle -----
    graph.add_node("reservation_agent", reservation_agent_node)
    graph.add_node("data_extractor", data_extractor_node)
    graph.add_node("router", router_node)
    graph.add_node("fetch_reservations_tool", fetch_reservations_node)
    graph.add_node("add_reservation_tool", add_reservation_node)
    graph.add_node("update_reservation_tool", update_reservation_node)
    graph.add_node("delete_reservation_tool", delete_reservation_node)
    graph.add_node("check_availability_tool", check_availability_node)
    graph.add_node("end", end_node)

    # Giriş ve çıkış noktaları
    graph.set_entry_point("reservation_agent")
    graph.set_finish_point("end")

    # Koşullu yönlendirme
    def route_from_reservation(state):
        try:
            if state.get("reservation_response"):
                last_response = state["reservation_response"][-1]
                content = last_response.content if hasattr(last_response, "content") else str(last_response)
                data = json.loads(content)
                tool_action = data.get("tool_action")
                action_type = data.get("action_type")
                if (tool_action and tool_action != "null") or action_type in ["list_reservations", "create_reservation", "update_reservation", "delete_reservation", "check_availability"]:
                    return "data_extractor"
                else:
                    return "end"
            return "end"
        except Exception as e:
            logger.warning(f"Reservation yanıtı işlenirken hata oluştu: {str(e)}, end'e yönlendiriliyor")
            return "end"

    graph.add_conditional_edges("reservation_agent", route_from_reservation, {
        "data_extractor": "data_extractor",
        "end": "end"
    })

    graph.add_edge("data_extractor", "router")

    def route_request(state):
        return state.get("router_output", "end")

    graph.add_conditional_edges("router", route_request, {
        "fetch_reservations_tool": "fetch_reservations_tool",
        "add_reservation_tool": "add_reservation_tool",
        "update_reservation_tool": "update_reservation_tool",
        "delete_reservation_tool": "delete_reservation_tool",
        "check_availability_tool": "check_availability_tool",
        "end": "end"
    })

    graph.add_edge("reservation_agent", "end")
    return graph

def compile_workflow(graph):
    logger.info("LangGraph derleniyor...")
    return graph.compile()

def build_graph() -> Any:
    try:
        graph = create_graph()
        return compile_workflow(graph)
    except Exception as e:
        logger.error(f"Graph oluşturma hatası: {str(e)}")
        raise