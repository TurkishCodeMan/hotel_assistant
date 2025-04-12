"""
Ajanlar
------
Sistemin farklı görevleri yerine getiren ajan tanımları.
LangGraph kullanarak modüler ve akış halinde tasarlanmıştır.
"""

import json
import logging
from typing import Dict, Any

from models.llm import GeminiJSONModel, GeminiModel
from prompts.prompts import (
    UNDERSTANDING_SYSTEM_PROMPT,
    RESERVATION_SYSTEM_PROMPT,
    SUPPORT_SYSTEM_PROMPT,

)
from states.state import AgentGraphState
from utils.utils import get_current_utc_datetime, check_for_content

# Logger ayarları
logger = logging.getLogger(__name__)

# Temel Ajan Sınıfı
class Agent:
    """
    Temel ajan sınıfı. Tüm ajanlar bu sınıftan türetilir.
    """
    def __init__(self, state=AgentGraphState,model=None,server=None, model_endpoint=None, stop=None, guided_json=None,temperature=0.0):
        """
        Args:
            state: Ajan durumu
            temperature: LLM sıcaklık değeri
        """
        self.state = state
        self.temperature = temperature
        self.model =model
        self.server = server
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json
        
    def update_state(self, key, value):
        self.state = {**self.state, key: value}
    
    def get_llm(self,json_model=True):
       if self.server == 'gemini':
            return GeminiJSONModel(
                model=self.model, 
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=self.model,
                temperature=self.temperature
            )
       # Server belirtilmediğinde varsayılan olarak 'gemini' kullan
       elif self.server is None:
            # Model belirtilmemişse varsayılan model kullan
            model = self.model if self.model else "gemini-2.0-flash"
            logger.warning(f"Server belirtilmemiş, varsayılan 'gemini' kullanılıyor. Model: {model}")
            return GeminiJSONModel(
                model=model, 
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=model,
                temperature=self.temperature
            )
       else:
            logger.error(f"Desteklenmeyen LLM sunucusu: {self.server}")
            # Hata mesajı ver ama yine de çalışması için varsayılan model döndür
            return GeminiJSONModel(
                model="gemini-2.0-flash", 
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model="gemini-2.0-flash",
                temperature=self.temperature
            )

# Understanding Agent
class UnderstandingAgent(Agent):
    """
    Karşılama ve Anlama Ajanı.
    Müşteri taleplerini analiz eder ve sınıflandırır.
    """
    def invoke(self,research_question, conversation_state, prompt=UNDERSTANDING_SYSTEM_PROMPT, feedback=None):
        """
        Anlama ajanını çağırır
        """
        logger.info(f"UnderstandingAgent invoked with question: {research_question}...")
        
        # Geri bildirim değerini kontrol et
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        # İnsan mesajını hazırla
        prompt = UNDERSTANDING_SYSTEM_PROMPT.format(
            chat_history=feedback_value,
        )
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": research_question}
        ]
        
        # LLM'i çağır
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        self.update_state("understanding_response", response)
        
        return self.state

# Reservation Agent
class ReservationAgent(Agent):
    """
    Rezervasyon Ajanı.
    Rezervasyon sorgulamaları ve işlemleriyle ilgilenir.
    """
    def invoke(self,research_question, conversation_state, prompt=RESERVATION_SYSTEM_PROMPT, feedback=None):
        """
        Rezervasyon ajanını çağırır
        """
        logger.info(f"ReservationAgent invoked with question: {research_question}...")
        
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        

        # Rezervasyon bilgilerini içeren prompt hazırla
        prompt = RESERVATION_SYSTEM_PROMPT.format(
            reservations_result=conversation_state['reservations_result'] if 'reservations_result' in conversation_state else [],
            add_reservation_result=conversation_state['add_reservation_result'] if 'add_reservation_result' in conversation_state else [],
            update_reservation_result=conversation_state['update_reservation_result'] if 'update_reservation_result' in conversation_state else [],
            delete_reservation_result=conversation_state['delete_reservation_result'] if 'delete_reservation_result' in conversation_state else [],
            chat_history=feedback_value,

        )
     
   
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": research_question}
        ]
        
        # LLM'i çağır
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        logger.info(f"ReservationAgent yanıtı: {response[:100]}...")
        
        # Response'u doğru formatta hazırla
        message_object = {"role": "assistant", "content": response}
        
        # Durum nesnesini güncelle
        self.update_state("reservation_response", message_object)
        
        # Otomatik olarak messages bölümü eklediğimizden emin olalım
        if "messages" not in self.state:
            self.state["messages"] = []
            
        self.state["messages"].append(message_object)
        
        return self.state

# Support Agent 
class SupportAgent(Agent):
    """
    Destek Ajanı.
    Müşteri destek sorularını yanıtlar.
    """
    def invoke(self,research_question, conversation_state, prompt=SUPPORT_SYSTEM_PROMPT, feedback=None):
        """
        Destek ajanını çağırır
        """
        logger.info(f"SupportAgent invoked with question: {research_question}...")
        
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
      
        # Destek bilgilerini içeren prompt hazırla
        prompt = SUPPORT_SYSTEM_PROMPT.format(
            chat_history=feedback_value
            ##TOOL DÖNÜŞÜ EKLENECEK serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),

        )
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": research_question}
        ]
        
        # LLM'i çağır
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        logger.info(f"SupportAgent yanıtı: {response[:100]}...")
        
        # Response'u doğru formatta hazırla
        message_object = {"role": "assistant", "content": response}
        
        # Durum nesnesini güncelle
        self.update_state("support_response", message_object)
        
        # Otomatik olarak messages bölümü eklediğimizden emin olalım
        if "messages" not in self.state:
            self.state["messages"] = []
            
        self.state["messages"].append(message_object)
        
        return self.state
