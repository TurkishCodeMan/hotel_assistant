"""
Ajan Graf Tanımı ve Orkestrasyon
--------------------------------
LangGraph kütüphanesi kullanarak ajanlar arasındaki 
akış ve iletişim mantığını tanımlar.
"""

import json
import logging
from typing import Dict, Any, Annotated, Callable
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from langgraph.graph import StateGraph, END

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

from states.state import AgentGraphState, state, get_agent_graph_state
from utils.utils import get_current_utc_datetime, check_for_content

# Prompt şablonları
from prompts.prompts import (
    RESERVATION_SYSTEM_PROMPT,
)

# Logger ayarları
logger = logging.getLogger(__name__)

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0.5,):
    """
    Ana ajan grafiğini oluşturur
    
    Args:
        server: API sunucusu (opsiyonel)
        model: Kullanılacak LLM modeli (opsiyonel)
        stop: Durdurma koşulları (opsiyonel)
        model_endpoint: Model API uç noktası (opsiyonel)
        temperature: Model sıcaklık değeri (opsiyonel)
    
    Returns:
        StateGraph: Yapılandırılmış ajan grafiği
    """
    graph = StateGraph(AgentGraphState)

    # ----- Ajan Düğümleri -----
    
    # 1. Rezervasyon Ajanı - Kullanıcı isteğini anlar ve gerekli aksiyonu belirler
    graph.add_node(
        "reservation_agent",
        lambda state: ReservationAgent(
            state=state,
            model=model,
            server=server,
            model_endpoint=model_endpoint,
            stop=stop,
            guided_json=None,
            temperature=temperature
        ).invoke(
            research_question=state['research_question'],  
            conversation_state=state,
            prompt=RESERVATION_SYSTEM_PROMPT,
            feedback=state['reservation_response'],
        )
    )
    
    # 2. Veri Çıkarıcı Ajan - Rezervasyon ajanından gelen yanıttan veri çıkarır
    graph.add_node(
        "data_extractor",
        lambda state: DataExtractorAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_response=lambda: state.get('reservation_response', [])
        )
    )
    
    # 3. Router Ajan - Veri çıkarıcının hazırladığı verilerle yönlendirme yapar
    graph.add_node(
        "router",
        lambda state: RouterAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_response=lambda: state.get('reservation_response', [])
        )
    )

    # ----- Tool Ajanları -----
    
    # 1. Rezervasyon Listeleme Aracı
    graph.add_node(
        "fetch_reservations_tool",
        lambda state: FetchReservationsAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            customer_data=lambda: state.get('reservation_query', [])
        )
    )
    
    # 2. Rezervasyon Ekleme Aracı
    graph.add_node(
        "add_reservation_tool",
        lambda state: AddReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            reservation_data=lambda: state.get('new_reservation', [])
        )
    )
    
    # 3. Rezervasyon Güncelleme Aracı
    graph.add_node(
        "update_reservation_tool",
        lambda state: UpdateReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            update_data=lambda: state.get('update_reservation', [])
        )
    )
    
    # 4. Rezervasyon Silme Aracı
    graph.add_node(
        "delete_reservation_tool",
        lambda state: DeleteReservationAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            delete_data=lambda: state.get('delete_reservation', [])
        )
    )
    
    # 5. Oda Müsaitliği Kontrol Aracı
    graph.add_node(
        "check_availability_tool",
        lambda state: CheckAvailabilityAgent(
            state=state,
            model=model,
            server=server
        ).invoke(
            research_question=state['research_question'],
            conversation_state=state,
            availability_data=lambda: state.get('availability_check', [])
        )
    )
    
    # 6. Akış Sonlandırma Düğümü
    graph.add_node(
        "end",
        lambda state: EndNodeAgent(
            state=state,
            model=model,
            server=server
        ).invoke()
    )

    # Grafik giriş ve çıkış noktalarını tanımla
    graph.set_entry_point("reservation_agent")
    graph.set_finish_point("end")
    
    # ----- Kenarları Tanımla -----
    
    # 1. Rezervasyon ajanından koşullu yönlendirme ekle
    def route_from_reservation(state):
        """
        Rezervasyon ajanından gelen yanıta göre ya data_extractor'a ya da end'e yönlendirir
        """
        try:
            # Reservation response kontrolü
            if state.get("reservation_response"):
                last_response = state["reservation_response"][-1]
                content = last_response.content if hasattr(last_response, "content") else str(last_response)
                
                data = json.loads(content)
                tool_action = data.get("tool_action")
                action_type = data.get("action_type")
                
                # Eğer tool_action belirtilmişse veya action_type rezervasyon işlemi ise data_extractor'a gönder
                if (tool_action is not None and tool_action != "null") or \
                   (action_type in ["list_reservations", "create_reservation", "update_reservation", 
                                    "delete_reservation", "check_availability"]):
                    logger.info(f"İşlem tespit edildi (action_type: {action_type}), data_extractor'a yönlendiriliyor")
                    return "data_extractor"
                else:
                    # Tool_action ve kabul edilen action_type yoksa end'e gönder (sohbet tarzı cevaplar için)
                    logger.info("İşlem tipi tespit edilmedi, doğrudan end'e yönlendiriliyor")
                    return "end"
            else:
                # Yanıt yoksa end'e yönlendir
                return "end"
        except Exception as e:
            # Herhangi bir hata durumunda end'e yönlendir
            logger.warning(f"Reservation yanıtı işlenirken hata oluştu: {str(e)}, end'e yönlendiriliyor")
            return "end"
    
    # ReservationAgent'tan koşullu kenar ekle
    graph.add_conditional_edges(
        "reservation_agent",
        route_from_reservation,
        {
            "data_extractor": "data_extractor",
            "end": "end"
        }
    )
    
    # 2. Veri çıkarıcıdan router'a
    graph.add_edge("data_extractor", "router")
    
    # 4. Router yönlendirmesi
    def route_request(state):
        """
        Router ajanının döndürdüğü düğüm adını kullanarak yönlendirme yapar
        """
        # router_output değerini al, varsayılan olarak "end" kullan
        next_node = state.get("router_output", "end")
        logger.info(f"Route_request fonksiyonu çağrıldı, yönlendirme: {next_node}")
        return next_node
    
    # Router'dan koşullu yönlendirme - hedef düğümleri mapping ile belirtelim
    graph.add_conditional_edges(
        "router",
        route_request,
        {
            "fetch_reservations_tool": "fetch_reservations_tool",
            "add_reservation_tool": "add_reservation_tool",
            "update_reservation_tool": "update_reservation_tool", 
            "delete_reservation_tool": "delete_reservation_tool",
            "check_availability_tool": "check_availability_tool",
            "end": "end"
        }
    )
    
    # 5. Araç düğümlerinden rezervasyon ajanına dönüş
    graph.add_edge("fetch_reservations_tool", "end")
    graph.add_edge("update_reservation_tool", "end")
    graph.add_edge("delete_reservation_tool", "end")
    graph.add_edge("check_availability_tool", "end")
    
    # 6. Rezervasyon ekleme işlemi sonrası doğrudan sonlandır
    graph.add_edge("add_reservation_tool", "end")

    return graph


def compile_workflow(graph):
    """
    Agent grafiğini derleyerek çalıştırılabilir bir iş akışı oluşturur
    
    Args:
        graph: Derlenecek ajan grafiği
        
    Returns:
        Compiled: Derlenmiş iş akışı
    """
    try:
        logger.info("LangGraph derleniyor...")
        workflow = graph.compile()
        logger.info("LangGraph derleme işlemi tamamlandı.")
        return workflow
    except Exception as e:
        logger.error(f"Graph derleme hatası: {str(e)}")
        # Hatayı tekrar fırlat
        raise

def build_graph() -> Any:
    """
    Varsayılan yapılandırma ile agent grafiğini oluşturur
    
    Returns:
        Compiled: Derlenmiş iş akışı
    """
    try:
        # Graf oluştur
        graph = create_graph()
        
        # Grafiği derle
        workflow = compile_workflow(graph)
        
        return workflow
    except Exception as e:
        logger.error(f"Graph oluşturma hatası: {str(e)}")
        # Hatayı tekrar fırlat
        raise

