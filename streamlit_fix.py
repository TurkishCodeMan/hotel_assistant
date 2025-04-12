#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Özkaya Otel Rezervasyon Asistanı - Streamlit Arayüzü
--------------------------------------------
Streamlit ile interaktif otel rezervasyon asistanı.
"""

import os
import json
import logging
import streamlit as st
import re
from typing import Dict, Any
import pandas as pd

# Özel modülleri içe aktar
from agent_graph.graph import create_graph, compile_workflow
from states.state import get_agent_graph_state, state

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/streamlit_app.log", mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Model ayarları
server = 'gemini'
model = 'gemini-2.0-flash'
model_endpoint = None
iterations = 40

# Yardımcı fonksiyonlar
def safe_parse_message(message_content):
    """
    Mesaj içeriğini güvenli bir şekilde ayrıştırır (JSON veya dict olarak)
    
    Args:
        message_content: Ayrıştırılacak mesaj içeriği
        
    Returns:
        dict: Ayrıştırılmış mesaj dict'i veya boş dict
    """
    if not message_content:
        return {}
        
    try:
        # JSON'daki null değeri Python'da tanımlı değil, önce None ile değiştirelim
        content = message_content.replace("'", '"').replace("null", "None")
        
        try:
            # JSON olarak çözmeyi dene
            return json.loads(content.replace("null", "None"))
        except json.JSONDecodeError:
            # JSON olarak çözülemezse, özel bir işlem yap
            try:
                # Eğer bu tipik yanıt yapısına benziyorsa, sadece response kısmını çıkar
                import re
                match = re.search(r'"response":"([^"]+)"', content)
                if match:
                    return {"response": match.group(1)}
                
                # Değilse standart eval kullan
                result = eval(content)
                if isinstance(result, dict):
                    return result
                return {}
            except Exception as e:
                logger.error(f"Eval hatası: {str(e)}")
                return {}
    except Exception as e:
        logger.error(f"Mesaj ayrıştırma hatası: {str(e)}")
        return {}

def clean_json_text(text):
    """
    JSON yanıtlarındaki kaçış karakterlerini temizler ve metin formatını düzeltir
    
    Args:
        text: Temizlenecek metin
        
    Returns:
        str: Temizlenmiş metin
    """
    if not text:
        return ""
    
    # Unicode kaçış karakterlerini düzelt
    text = text.replace("\\u00fc", "ü")
    text = text.replace("\\u00f6", "ö")
    text = text.replace("\\u00e7", "ç")
    text = text.replace("\\u011f", "ğ")
    text = text.replace("\\u0131", "ı")
    text = text.replace("\\u015f", "ş")
    text = text.replace("\\u00c7", "Ç")
    text = text.replace("\\u011e", "Ğ")
    text = text.replace("\\u0130", "İ")
    text = text.replace("\\u00d6", "Ö")
    text = text.replace("\\u015e", "Ş")
    text = text.replace("\\u00dc", "Ü")
    
    # Diğer genel kaçış karakterlerini düzelt
    text = text.replace("\\n", "\n")
    text = text.replace("\\\"", "\"")
    text = text.replace("\\'", "'")
    
    return text

def get_last_response(event: Dict) -> str:
    """Son yanıtı event'ten çıkarır"""
    try:
        # End içindeki yanıtları kontrol et
        if "end" in event:
            end_data = event["end"]
            
            # Öncelik sırası:
            # 1. Rezervasyon ekleme sonuçları
            # 2. Rezervasyon sorgulama sonuçları 
            # 3. Rezervasyon güncelleme sonuçları
            # 4. Rezervasyon silme sonuçları
            # 5. Oda müsaitliği kontrol sonuçları
            # 6. Genel rezervasyon yanıtları (Fallback)
            # 7. Destek ve anlama yanıtları
            
            # 1. Rezervasyon ekleme sonuçlarını kontrol et
            if "add_reservation_result" in end_data and end_data["add_reservation_result"] and len(end_data["add_reservation_result"]) > 0:
                add_result = end_data["add_reservation_result"][-1]  # Son yanıtı al
                if hasattr(add_result, 'content'):
                    try:
                        logger.debug(f"Reservasyon ekleme ham içerik: {add_result.content[:200]}...")
                        result_dict = safe_parse_message(add_result.content)
                        logger.debug(f"Ayrıştırılmış rezervasyon: {result_dict}")
                        
                        if result_dict.get("success"):
                            # Başarılı rezervasyon ekleme
                            reservation = result_dict.get("reservation", {})
                            
                            # Rezervasyon bilgilerini kontrol et
                            if not reservation:
                                logger.debug("Rezervasyon bilgileri boş, alternatif çözüm deneniyor...")
                                # Rezervasyon verisi bulunamadıysa, başka bir yerden çekmeye çalış
                                if "action_type" in result_dict and result_dict["action_type"] == "create_reservation":
                                    # LLM yanıtından rezervasyon bilgileri oluştur
                                    reservation = {
                                        "customer_name": result_dict.get("customer_name", "Misafir"),
                                        "check_in_date": result_dict.get("check_in_date", "N/A"),
                                        "check_out_date": result_dict.get("check_out_date", "N/A"),
                                        "room_type": result_dict.get("room_type", "Standard"),
                                        "adults": result_dict.get("adults", 1),
                                        "children": result_dict.get("children", 0),
                                        "status": "Onaylandı"
                                    }
                                    logger.debug(f"Alternatif rezervasyon verileri oluşturuldu: {reservation}")
                            
                            if reservation:
                                return f"""✅ Rezervasyonunuz başarıyla oluşturuldu!

📋 Rezervasyon Detayları:
👤 Müşteri: {reservation.get('customer_name', 'Misafir')}
🏨 Oda Tipi: {reservation.get('room_type', 'Standard')}
📅 Giriş Tarihi: {reservation.get('check_in_date', 'N/A')}
📅 Çıkış Tarihi: {reservation.get('check_out_date', 'N/A')}
👪 Kişi Sayısı: {reservation.get('adults', 1)} yetişkin, {reservation.get('children', 0)} çocuk
🔖 Durum: {reservation.get('status', 'Onaylandı')}"""
                            else:
                                # Rezervasyon detayları bulunamadı, basit bir başarı mesajı göster
                                return "✅ Rezervasyonunuz başarıyla oluşturuldu!"
                        else:
                            # Başarısız rezervasyon ekleme
                            error_msg = result_dict.get("error", "Bilinmeyen bir hata oluştu")
                            return f"❌ Rezervasyon oluşturulamadı: {result_dict.get('message', error_msg)}"
                    except Exception as e:
                        logger.error(f"Rezervasyon ekleme sonuç işleme hatası: {str(e)}")
                        return "Rezervasyon işlemi tamamlandı, ancak sonuç işlenirken bir hata oluştu."
            
            # 2. Rezervasyon sorgulama sonuçlarını kontrol et
            if "reservations_result" in end_data and end_data["reservations_result"] and len(end_data["reservations_result"]) > 0:
                res_result = end_data["reservations_result"][-1]  # Son yanıtı al
                if hasattr(res_result, 'content'):
                    try:
                        result_dict = safe_parse_message(res_result.content)
                        
                        # Eğer rezervasyonlar varsa, onları güzel bir şekilde formatlayarak göster
                        if result_dict.get("success") and result_dict.get("count", 0) > 0:
                            reservations = result_dict.get("reservations", [])
                            formatted_response = "📋 Bulunan Rezervasyonlar:\n\n"
                            
                            for i, res in enumerate(reservations, 1):
                                formatted_response += f"{i}. 📅 {res.get('name', 'Misafir')} - {res.get('check_in', 'N/A')} → {res.get('check_out', 'N/A')} - {res.get('room_type', 'N/A')} oda\n"
                            
                            return formatted_response
                        elif result_dict.get("success") and result_dict.get("count", 0) == 0:
                            return "Aradığınız kriterlere uygun rezervasyon bulunamadı."
                    except Exception as e:
                        logger.error(f"Rezervasyon sonuç işleme hatası: {str(e)}")
            
            # 3. Rezervasyon güncelleme sonuçlarını kontrol et
            if "update_reservation_result" in end_data and end_data["update_reservation_result"] and len(end_data["update_reservation_result"]) > 0:
                update_result = end_data["update_reservation_result"][-1]  # Son yanıtı al
                if hasattr(update_result, 'content'):
                    try:
                        result_dict = safe_parse_message(update_result.content)
                        
                        if result_dict.get("success"):
                            # Başarılı rezervasyon güncelleme
                            updated_fields = result_dict.get("updated_fields", [])
                            fields_str = ", ".join(updated_fields) if updated_fields else "Bilgiler"
                            return f"""✅ Rezervasyonunuz başarıyla güncellendi!

🔄 Güncellenen alanlar: {fields_str}
📝 {result_dict.get('message', 'İşlem tamamlandı.')}"""
                        else:
                            # Başarısız rezervasyon güncelleme
                            return f"❌ Rezervasyon güncellenemedi: {result_dict.get('message', 'Bilinmeyen hata')}"
                    except Exception as e:
                        logger.error(f"Rezervasyon güncelleme sonuç işleme hatası: {str(e)}")
            
            # 4. Rezervasyon silme sonuçlarını kontrol et
            if "delete_reservation_result" in end_data and end_data["delete_reservation_result"] and len(end_data["delete_reservation_result"]) > 0:
                delete_result = end_data["delete_reservation_result"][-1]  # Son yanıtı al
                if hasattr(delete_result, 'content'):
                    try:
                        result_dict = safe_parse_message(delete_result.content)
                        
                        if result_dict.get("success"):
                            # Başarılı rezervasyon silme
                            return f"""✅ {result_dict.get('message', 'Rezervasyon başarıyla silindi!')}"""
                        else:
                            # Başarısız rezervasyon silme
                            return f"❌ Rezervasyon silinemedi: {result_dict.get('message', 'Bilinmeyen hata')}"
                    except Exception as e:
                        logger.error(f"Rezervasyon silme sonuç işleme hatası: {str(e)}")
            
            # 5. Oda müsaitliği kontrolü sonuçlarını kontrol et
            if "availability_result" in end_data and end_data["availability_result"] and len(end_data["availability_result"]) > 0:
                avail_result = end_data["availability_result"][-1]  # Son yanıtı al
                if hasattr(avail_result, 'content'):
                    try:
                        result_dict = safe_parse_message(avail_result.content)
                        
                        if result_dict.get("success"):
                            # Başarılı müsaitlik kontrolü
                            available_rooms = result_dict.get("available_rooms", [])
                            formatted_response = f"""📆 {result_dict.get('check_in_date')} - {result_dict.get('check_out_date')} tarihleri arasında müsait odalar:

"""
                            for i, room in enumerate(available_rooms, 1):
                                room_type = room.get('room_type', '')
                                room_features = ""
                                # Oda özelliklerini ekle
                                if room_type == "Standard":
                                    room_features = "25m², çift kişilik yatak, klima, mini bar, TV"
                                elif room_type == "Deluxe":
                                    room_features = "35m², geniş yatak, oturma alanı, klima, mini bar, TV"
                                elif room_type == "Suite":
                                    room_features = "50m², yatak odası ve oturma odası, jakuzi, klima, mini bar, TV"
                                
                                formatted_response += f"{i}. 🏨 {room_type} - {room.get('price')}₺ - {'✅ Müsait' if room.get('available') else '❌ Dolu'}\n"
                                formatted_response += f"   📝 Özellikler: {room_features}\n\n"
                            
                            # Otel bilgilerini ekle
                            formatted_response += """ℹ️ Otel Bilgileri:
- Check-in: 14:00, Check-out: 12:00
- Kahvaltı dahil
- Ücretsiz Wi-Fi ve otopark"""
                            
                            return formatted_response
                        else:
                            # Başarısız müsaitlik kontrolü
                            return f"❌ Müsaitlik kontrolü yapılamadı: {result_dict.get('message', 'Bilinmeyen hata')}"
                    except Exception as e:
                        logger.error(f"Müsaitlik kontrol sonuç işleme hatası: {str(e)}")
            
            # 6. Genel rezervasyon yanıtları (Fallback)
            if "reservation_response" in end_data and end_data["reservation_response"] and len(end_data["reservation_response"]) > 0:
                res_resp = end_data["reservation_response"][-1]  # Son yanıtı al
                if hasattr(res_resp, 'content'):
                    content = res_resp.content
                    
                    # 1. Eğer JSON formatında bir yanıt ise regex ile response alanını çıkar
                    if content.startswith('{') and '"response"' in content:
                        try:
                            import re
                            match = re.search(r'"response":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON response çıkarma hatası: {str(e)}")
                    
                    # 2. Normal JSON parsing dene
                    try:
                        result_dict = safe_parse_message(content)
                        if result_dict and "response" in result_dict:
                            return clean_json_text(result_dict["response"])
                    except Exception as e:
                        logger.error(f"JSON parse hatası: {str(e)}")
                    
                    # 3. Yukarıdaki yöntemler başarısız olursa, temizlenmiş ham içeriği döndür
                    return clean_json_text(content)
            
            # 7. Destek ve anlama yanıtları
            if "support_response" in end_data and end_data["support_response"] and len(end_data["support_response"]) > 0:
                support_resp = end_data["support_response"][-1]  # Son yanıtı al
                if hasattr(support_resp, 'content'):
                    content = support_resp.content
                    
                    # JSON işleme aynı şekilde
                    if content.startswith('{') and '"response"' in content:
                        try:
                            import re
                            match = re.search(r'"response":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON response çıkarma hatası: {str(e)}")
                    
                    try:
                        result_dict = safe_parse_message(content)
                        if result_dict and "response" in result_dict:
                            return clean_json_text(result_dict["response"])
                    except Exception as e:
                        logger.error(f"JSON parse hatası: {str(e)}")
                    
                    return clean_json_text(content)
                    
            if "understanding_response" in end_data and end_data["understanding_response"] and len(end_data["understanding_response"]) > 0:
                und_resp = end_data["understanding_response"][-1]  # Son yanıtı al
                if hasattr(und_resp, 'content'):
                    content = und_resp.content
                    
                    # Soru netleştirme çıkarımı
                    if content.startswith('{') and '"clarification_question"' in content:
                        try:
                            import re
                            match = re.search(r'"clarification_question":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON clarification çıkarma hatası: {str(e)}")
                    
                    # JSON işleme aynı şekilde
                    if content.startswith('{') and '"response"' in content:
                        try:
                            import re
                            match = re.search(r'"response":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON response çıkarma hatası: {str(e)}")
                    
                    try:
                        result_dict = safe_parse_message(content)
                        if result_dict and "clarification_question" in result_dict:
                            return clean_json_text(result_dict["clarification_question"])
                        elif result_dict and "response" in result_dict:
                            return clean_json_text(result_dict["response"])
                    except Exception as e:
                        logger.error(f"JSON parse hatası: {str(e)}")
                    
                    return clean_json_text(content)

        # Eğer burada hala return edilmediyse, başlatma mesajı göster
        return "Merhaba! Size nasıl yardımcı olabilirim? Özkaya Otel'de rezervasyon yapmak, bilgi almak veya yardım için bana sorabilirsiniz."
    except Exception as e:
        logger.error(f"Yanıt işleme hatası: {str(e)}")
        return "Üzgünüm, yanıt işlenirken bir hata oluştu."

# Streamlit uygulama yapılandırması
def create_state_display(session_state):
    """
    State durumunu görselleştiren panel oluşturur
    
    Args:
        session_state: Güncel session state içeriği
    """
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏨</div>
        <div style="font-weight: 600; color: var(--primary-color); font-size: 1.2rem;">Özkaya Otel</div>
        <div style="font-size: 0.9rem; color: var(--text-secondary);">Sistem Durumu</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not session_state:
        st.sidebar.markdown("""
        <div class="sidebar-section">
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem; color: var(--text-secondary);">🔄</div>
                <div style="color: var(--text-secondary);">Henüz bir durum bilgisi yok</div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; color: var(--text-secondary);">Sistem başlatılıyor...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Temel state bilgilerini göster
    if "reservation_response" in session_state:
        # Reservation_response listesinin boş olup olmadığını kontrol et
        if session_state["reservation_response"] and len(session_state["reservation_response"]) > 0:
            with st.sidebar.expander("📝 Son Rezervasyon Yanıtı", expanded=True):
                last_resp = session_state["reservation_response"][-1]
                if hasattr(last_resp, 'content'):
                    content = last_resp.content
                    content_json = safe_parse_message(content)
                    
                    action_type = content_json.get("action_type", "Yok")
                    tool_action = content_json.get("tool_action", "Yok")
                    
                    st.sidebar.markdown("""
                    <div class="sidebar-section">
                        <div class="sidebar-header">🔄 İşlem Bilgileri</div>
                        <table style="width: 100%; font-size: 0.9rem;">
                            <tr>
                                <td style="padding: 0.3rem; color: var(--text-secondary);">İşlem Tipi:</td>
                                <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                            </tr>
                            <tr>
                                <td style="padding: 0.3rem; color: var(--text-secondary);">Araç İşlemi:</td>
                                <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                            </tr>
                        </table>
                    </div>
                    """.format(action_type, tool_action), unsafe_allow_html=True)
                    
                    # Rezervasyon detaylarını göster
                    if action_type == "create_reservation":
                        st.sidebar.markdown("""
                        <div class="sidebar-section">
                            <div class="sidebar-header">📋 Rezervasyon Bilgileri</div>
                            <table style="width: 100%; font-size: 0.9rem;">
                                <tr>
                                    <td style="padding: 0.3rem; color: var(--text-secondary);">Müşteri:</td>
                                    <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.3rem; color: var(--text-secondary);">Giriş Tarihi:</td>
                                    <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.3rem; color: var(--text-secondary);">Çıkış Tarihi:</td>
                                    <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.3rem; color: var(--text-secondary);">Oda Tipi:</td>
                                    <td style="padding: 0.3rem; font-weight: 500;">{}</td>
                                </tr>
                            </table>
                        </div>
                        """.format(
                            content_json.get('customer_name', 'Belirtilmemiş'),
                            content_json.get('check_in_date', 'Belirtilmemiş'),
                            content_json.get('check_out_date', 'Belirtilmemiş'),
                            content_json.get('room_type', 'Belirtilmemiş')
                        ), unsafe_allow_html=True)
        else:
            with st.sidebar.expander("📝 Son Rezervasyon Yanıtı", expanded=True):
                st.sidebar.markdown("""
                <div class="sidebar-section" style="text-align: center; padding: 1rem;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--text-secondary);">📭</div>
                    <div style="color: var(--text-secondary);">Henüz rezervasyon yanıtı yok</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Rezervasyon verilerini göster
    if "new_reservation" in session_state:
        with st.sidebar.expander("🏨 Yeni Rezervasyon", expanded=True):
            try:
                res_data = json.loads(session_state["new_reservation"])
                # Daha güzel formatlama için özel gösterim
                st.sidebar.markdown("""
                <div class="sidebar-section">
                    <div class="sidebar-header">📋 Rezervasyon Detayları</div>
                    <div style="background-color: rgba(30, 136, 229, 0.05); border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem; border-left: 3px solid var(--primary-color);">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span style="font-weight: 600; color: var(--text-color);">{}</span>
                            <span style="font-size: 0.8rem; background-color: {}; color: white; padding: 0.2rem 0.5rem; border-radius: 10px;">{}</span>
                        </div>
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem; color: var(--text-secondary);">
                            <span style="margin-right: 0.5rem;">📅</span> {} - {}
                        </div>
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem; color: var(--text-secondary);">
                            <span style="margin-right: 0.5rem;">🏨</span> {} Oda
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-secondary);">
                            <span style="margin-right: 0.5rem;">👪</span> {} yetişkin, {} çocuk
                        </div>
                    </div>
                </div>
                """.format(
                    res_data.get('customer_name', 'Misafir'),
                    '#4CAF50' if res_data.get('status') == 'Onaylandı' else '#FFA000',
                    res_data.get('status', 'Onay Bekliyor'),
                    res_data.get('check_in_date', 'N/A'),
                    res_data.get('check_out_date', 'N/A'),
                    res_data.get('room_type', 'Standard'),
                    res_data.get('adults', 0),
                    res_data.get('children', 0)
                ), unsafe_allow_html=True)
            except:
                st.sidebar.text(session_state["new_reservation"])
    
    # Rezervasyon sorgusu sonuçları
    if "reservations_result" in session_state and len(session_state["reservations_result"]) > 0:
        with st.sidebar.expander("📋 Bulunan Rezervasyonlar", expanded=True):
            try:
                last_result = session_state["reservations_result"][-1]
                if hasattr(last_result, 'content'):
                    result_dict = safe_parse_message(last_result.content)
                    if result_dict.get("success") and result_dict.get("count", 0) > 0:
                        reservations = result_dict.get("reservations", [])
                        st.sidebar.markdown(f"""
                        <div class="sidebar-section">
                            <div class="sidebar-header">🔍 {len(reservations)} Rezervasyon Bulundu</div>
                        """, unsafe_allow_html=True)
                        
                        for i, res in enumerate(reservations, 1):
                            st.sidebar.markdown(f"""
                            <div style="background-color: rgba(30, 136, 229, 0.05); border-radius: 8px; padding: 0.8rem; margin-bottom: 0.6rem; border-left: 3px solid var(--primary-color);">
                                <div style="font-weight: 600; color: var(--text-color); margin-bottom: 0.3rem;">{i}. {res.get('name', 'Misafir')}</div>
                                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.3rem;">
                                    <span style="color: var(--text-secondary);">📅 Giriş: {res.get('check_in', 'N/A')}</span>
                                    <span style="color: var(--text-secondary);">📅 Çıkış: {res.get('check_out', 'N/A')}</span>
                                </div>
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">🏨 Oda: {res.get('room_type', 'N/A')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.sidebar.markdown("</div>", unsafe_allow_html=True)
                    elif result_dict.get("success") and result_dict.get("count", 0) == 0:
                        st.sidebar.markdown("""
                        <div class="sidebar-section" style="text-align: center; padding: 1rem;">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--warning-color);">🔍</div>
                            <div style="color: var(--text-secondary);">Aradığınız kriterlere uygun rezervasyon bulunamadı.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.sidebar.markdown("""
                        <div class="sidebar-section" style="text-align: center; padding: 1rem;">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--error-color);">❌</div>
                            <div style="color: var(--text-secondary);">Rezervasyon sorgulanırken bir hata oluştu.</div>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.sidebar.markdown(f"""
                <div class="sidebar-section" style="text-align: center; padding: 1rem;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--error-color);">⚠️</div>
                    <div style="color: var(--text-secondary);">Rezervasyon sonuçları gösterilirken hata oluştu.</div>
                    <div style="font-size: 0.8rem; color: var(--error-color); margin-top: 0.5rem;">{str(e)}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Otel bilgileri
    st.sidebar.markdown("""
    <div class="sidebar-section" style="margin-top: 2rem;">
        <div class="sidebar-header">ℹ️ Otel Bilgileri</div>
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem; color: var(--text-secondary);">
            <span style="margin-right: 0.5rem;">📍</span> Özkaya Otel, İstanbul
        </div>
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem; color: var(--text-secondary);">
            <span style="margin-right: 0.5rem;">🕒</span> Check-in: 14:00, Check-out: 12:00
        </div>
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem; color: var(--text-secondary);">
            <span style="margin-right: 0.5rem;">🍳</span> Kahvaltı dahil
        </div>
        <div style="font-size: 0.9rem; color: var(--text-secondary);">
            <span style="margin-right: 0.5rem;">📱</span> +90 (212) 123 45 67
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mevcut diğer bilgileri göster
    with st.sidebar.expander("⚙️ Tüm Durum Verileri", expanded=False):
        filtered_state = {k: v for k, v in session_state.items() 
                         if k not in ["reservation_response", "new_reservation", "reservation_query"] 
                         and not isinstance(v, list) and not k.endswith("_result")}
        st.sidebar.json(filtered_state)

def initialize_session():
    """
    Streamlit oturumunu başlatır ve gerekli session state değişkenlerini ayarlar
    """
    # Streamlit session_state değişkenlerini ayarla
    if "conversation" not in st.session_state:
        st.session_state.conversation = []  # Konuşma geçmişi
    
    # LangGraph state'ini başlatma
    if "session_state" not in st.session_state:
        st.session_state.session_state = state.copy() if state else {}  # LangGraph state'i
        logger.info("Session state başlatıldı: %s", st.session_state.session_state)
    
    if "workflow" not in st.session_state:
        st.session_state.workflow = None  # LangGraph workflow
    
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    
    # Form gönderim durumu için
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    
    # State debug bilgisi
    logger.info("Session state durumu: %s", st.session_state)

def process_message():
    """Form gönderildiğinde çalışacak fonksiyon"""
    if st.session_state.user_message:  # user_message içeriği varsa
        # Form gönderildi durumunu true yap
        st.session_state.form_submitted = True

def main():
    """Ana uygulama fonksiyonu"""
    st.set_page_config(
        page_title="Özkaya Otel Rezervasyon Asistanı",
        page_icon="🏨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Genel CSS stilleri
    st.markdown("""
    <style>
        /* Genel Stil Ayarları */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Ana renk paleti */
        :root {
            --primary-color: #1E88E5;
            --secondary-color: #FFA000;
            --background-color: #FFFFFF;
            --card-bg-color: #F8F9FA;
            --success-color: #4CAF50;
            --warning-color: #FF9800;
            --error-color: #F44336;
            --text-color: #212121;
            --text-secondary: #757575;
            --border-color: #E0E0E0;
        }
        
        /* Streamlit bileşenlerini özelleştirme */
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #1976D2;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        /* Kart stili */
        .custom-card {
            background-color: var(--card-bg-color);
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border-color);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .custom-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        
        /* Sohbet mesajları için stiller */
        .chat-message-user {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
        }
        
        .chat-message-assistant {
            display: flex;
            margin-bottom: 1rem;
        }
        
        .chat-bubble-user {
            background-color: var(--primary-color);
            color: white;
            border-radius: 18px 18px 0 18px;
            padding: 0.8rem 1.2rem;
            max-width: 80%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            word-wrap: break-word;
        }
        
        .chat-bubble-assistant {
            background-color: var(--card-bg-color);
            color: var(--text-color);
            border-radius: 18px 18px 18px 0;
            padding: 0.8rem 1.2rem;
            max-width: 80%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: 1px solid var(--border-color);
            word-wrap: break-word;
        }
        
        .chat-header {
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.4rem;
        }
        
        /* Form stilleri */
        div[data-testid="stForm"] {
            background-color: var(--card-bg-color);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid var(--border-color);
            margin-top: 1rem;
        }
        
        input[type="text"], textarea {
            border-radius: 10px !important;
            border: 1px solid var(--border-color) !important;
            padding: 0.8rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus, textarea:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2) !important;
        }
        
        /* Özetler için stil */
        .sidebar-section {
            background-color: var(--card-bg-color);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border-color);
        }
        
        .sidebar-header {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.6rem;
            color: var(--primary-color);
        }
        
        /* Responsive tasarım için */
        @media (max-width: 768px) {
            .chat-bubble-user, .chat-bubble-assistant {
                max-width: 90%;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Oturumu başlat
    initialize_session()
    
    # Başlık ve açıklama
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #3498db, #1E88E5); color: white; border: none; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 3rem; margin-right: 15px;">🏨</span>
            <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 700;">Özkaya Otel</h1>
        </div>
        <h2 style="margin-top: 0; color: white; font-weight: 500; margin-bottom: 1.5rem;">Rezervasyon Asistanı</h2>
        <p style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.9); max-width: 800px; margin: 0 auto; line-height: 1.6;">
            Özkaya Otel'e hoş geldiniz! Oda rezervasyonu yapmak, mevcut rezervasyonunuzu yönetmek veya otel hakkında sorularınız için benimle sohbet edebilirsiniz.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Öne çıkan özellikler
    st.markdown("<h3 style='margin-bottom: 1.5rem; font-weight: 500; color: #FFFFFF; background-color: #1E88E5; padding: 0.8rem 1.2rem; border-radius: 10px;'>✨ Hizmetlerimiz</h3>", unsafe_allow_html=True)
    
    services_container = st.container()
    with services_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="custom-card" style="text-align: center; background-color: rgba(30, 136, 229, 0.05); border-left: 4px solid var(--primary-color);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--primary-color);">📅</div>
                <h3 style="margin-top: 0; color: var(--primary-color); font-weight: 600; font-size: 1.2rem;">Rezervasyon</h3>
                <p style="color: var(--text-secondary); font-size: 0.95rem;">
                    Oda müsaitliğini anında kontrol edin ve kolayca rezervasyon yapın.
                </p>
                <div style="background-color: rgba(30, 136, 229, 0.1); border-radius: 8px; padding: 0.5rem; margin-top: 1rem; font-size: 0.85rem; color: var(--primary-color);">
                    "3 Ağustos'ta 2 kişilik oda ayırtmak istiyorum"
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="custom-card" style="text-align: center; background-color: rgba(255, 160, 0, 0.05); border-left: 4px solid var(--secondary-color);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--secondary-color);">🔍</div>
                <h3 style="margin-top: 0; color: var(--secondary-color); font-weight: 600; font-size: 1.2rem;">Sorgulama</h3>
                <p style="color: var(--text-secondary); font-size: 0.95rem;">
                    Mevcut rezervasyonlarınızı görüntüleyin ve kolayca yönetin.
                </p>
                <div style="background-color: rgba(255, 160, 0, 0.1); border-radius: 8px; padding: 0.5rem; margin-top: 1rem; font-size: 0.85rem; color: var(--secondary-color);">
                    "Ahmet Yılmaz adına rezervasyonumu göster"
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="custom-card" style="text-align: center; background-color: rgba(76, 175, 80, 0.05); border-left: 4px solid var(--success-color);">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--success-color);">❓</div>
                <h3 style="margin-top: 0; color: var(--success-color); font-weight: 600; font-size: 1.2rem;">Bilgi</h3>
                <p style="color: var(--text-secondary); font-size: 0.95rem;">
                    Otel hizmetleri, fiyatlar ve olanaklar hakkında detaylı bilgi alın.
                </p>
                <div style="background-color: rgba(76, 175, 80, 0.1); border-radius: 8px; padding: 0.5rem; margin-top: 1rem; font-size: 0.85rem; color: var(--success-color);">
                    "Otelde havuz var mı? Kahvaltı dahil mi?"
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Yan panel - State görüntüleme
    # Debug için state durumunu yazdır
    st.sidebar.markdown("### 🔍 State Bilgileri (Debug)")
    st.sidebar.write("State içeriği (session_state):", st.session_state)
    
    # State görüntülemeyi güncelle
    if hasattr(st.session_state, 'session_state'):
        create_state_display(st.session_state.session_state)
    else:
        create_state_display(state) # global state değişkenini kullan
    
    # LangGraph workflow'u başlat
    if not st.session_state.initialized:
        with st.spinner("Sistem başlatılıyor..."):
            try:
                # Graf ve iş akışı oluştur
                graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
                workflow = compile_workflow(graph)
                st.session_state.workflow = workflow
                
                # State bilgisini doğrudan göster
                st.sidebar.markdown("### 🔄 Başlangıç State Bilgisi")
                st.sidebar.write(state)
                
                # State'i session_state'e aktar
                if state:
                    st.session_state.session_state = state.copy()
                
                st.session_state.initialized = True
                st.success("Sistem başarıyla başlatıldı!")
            except Exception as e:
                st.error(f"Sistem başlatılırken bir hata oluştu: {str(e)}")
                return
    
    # Sohbet gösterimi
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="display: flex; align-items: center; margin-bottom: 1.5rem; font-weight: 500; color: #FFFFFF; background-color: #1E88E5; padding: 0.8rem 1.2rem; border-radius: 10px;">
            <span style="margin-right: 10px; font-size: 1.4rem;">💬</span> Sohbet
        </h3>
        <div class="custom-card" style="padding: 0; overflow: hidden; max-height: 500px; overflow-y: auto;">
            <div style="padding: 1.5rem;">
                <div id="chat-container">
                    <!-- Sohbet mesajları buraya eklenecek -->
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    chat_container = st.container()
    with chat_container:
        # Konuşma boş ise karşılama mesajı göster
        if not st.session_state.conversation:
            st.markdown("""
            <div style="display: flex; margin-bottom: 1rem; justify-content: center;">
                <div style="background-color: rgba(30, 136, 229, 0.05); border-radius: 15px; padding: 1.5rem; text-align: center; max-width: 80%; border: 1px dashed var(--primary-color);">
                    <div style="font-size: 2rem; margin-bottom: 1rem; color: var(--primary-color);">👋</div>
                    <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--primary-color);">Merhaba, Özkaya Otel'e Hoş Geldiniz!</div>
                    <div style="color: var(--text-secondary); line-height: 1.6;">
                        Size nasıl yardımcı olabilirim? Rezervasyon yapmak, mevcut rezervasyonunuzu kontrol etmek veya otel hakkında bilgi almak için sorularınızı yazabilirsiniz.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        for i, (role, message) in enumerate(st.session_state.conversation):
            if role == "user":
                st.markdown(
                    f"""
                    <div class="chat-message-user">
                        <div class="chat-bubble-user">
                            <div class="chat-header">👤 Siz</div>
                            <div>{message}</div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-message-assistant">
                        <div class="chat-bubble-assistant">
                            <div class="chat-header">🤖 Asistan</div>
                            <div style="white-space: pre-wrap;">{message}</div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
    
    # Kullanıcı giriş formu
    with st.form(key="chat_form", clear_on_submit=True):
        st.markdown("""
        <style>
            div[data-testid="stForm"] {
                background-color: #212121;
                padding: 1.8rem;
                border-radius: 15px;
                border: 1px solid #424242;
                margin-top: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            div[data-testid="stForm"] label {
                color: #E0E0E0 !important;
            }
            
            div[data-testid="stForm"] input[type="text"] {
                background-color: #333333 !important;
                color: #FFFFFF !important;
                border: 1px solid #424242 !important;
                border-radius: 10px !important;
            }
            
            div[data-testid="stForm"] input[type="text"]:focus {
                border-color: #1E88E5 !important;
                box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2) !important;
            }
            
            div[data-testid="stForm"] button {
                background-color: #1E88E5 !important;
                color: white !important;
                border: none !important;
            }
            
            div[data-testid="stForm"] button:hover {
                background-color: #1976D2 !important;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            }
        </style>
        <div style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: #E0E0E0; font-weight: 500; font-size: 1rem;">
            Asistana mesajınız:
        </div>
        """, unsafe_allow_html=True)
        
        user_message = st.text_input(
            label="", 
            key="user_message", 
            placeholder="Nasıl yardımcı olabilirim? Rezervasyon yapmak, bilgi almak için yazın..."
        )
        
        cols = st.columns([3, 2, 2])
        with cols[1]:
            st.form_submit_button(
                "💬 Gönder", 
                on_click=process_message,
                use_container_width=True
            )
        with cols[2]:
            st.form_submit_button(
                "🔄 Yeni Sohbet", 
                on_click=lambda: st.session_state.update({"conversation": []}),
                use_container_width=True
            )
        
        # Örnek sorular önerisi
        if not st.session_state.conversation:
            st.markdown("""
            <div style="margin-top: 1rem; padding: 1rem; background-color: #333333; border-radius: 10px; border: 1px dashed #424242;">
                <div style="font-weight: 500; margin-bottom: 0.5rem; color: #E0E0E0;">✨ Örnek Sorular:</div>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="background-color: #424242; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid #616161; color: #E0E0E0;">10-15 Ağustos arası oda müsaitliği</div>
                    <div style="background-color: #424242; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid #616161; color: #E0E0E0;">2 kişilik oda fiyatları nedir?</div>
                    <div style="background-color: #424242; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid #616161; color: #E0E0E0;">Rezervasyonumu iptal etmek istiyorum</div>
                    <div style="background-color: #424242; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid #616161; color: #E0E0E0;">Otelin özellikleri nelerdir?</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Form gönderildiyse mesajı işle (form_submitted True ise)
    if st.session_state.form_submitted:
        # Kullanıcı mesajı
        user_input = st.session_state.user_message
        
        # Form durumunu sıfırla
        st.session_state.form_submitted = False
        
        # Kullanıcı mesajını konuşma geçmişine ekle
        st.session_state.conversation.append(("user", user_input))
        
        # Konuşma geçmişini hazırla - SADECE kullanıcı mesajlarını al
        conversation_history = []
        for role, msg in st.session_state.conversation:
            if role == "user":
                conversation_history.append(msg)
        
        # LangGraph için girdiyi hazırla
        dict_inputs = st.session_state.session_state.copy() if st.session_state.session_state else {}
        dict_inputs["research_question"] = conversation_history
        
        limit = {"recursion_limit": iterations}
        
        # İşleme göstergesi
        with st.spinner("Yanıt hazırlanıyor..."):
            last_event = None
            for event in st.session_state.workflow.stream(dict_inputs, limit):
                last_event = event
                # Her adımda debug çıktısı
                if "end" in event:
                    # State içeriğini yan panelde göster
                    keys = list(event["end"].keys())
                    st.sidebar.markdown("### 🔄 İşlem Adımı")
                    st.sidebar.write(f"State içeriğinde {len(keys)} anahtar var")
                    # Sadece önemli bilgileri göster
                    if "reservation_response" in event["end"]:
                        st.sidebar.info("Rezervasyon yanıtı alındı ✅")
                    if "new_reservation" in event["end"]:
                        st.sidebar.success("Yeni rezervasyon oluşturuldu ✅")
                    if "reservations_result" in event["end"]:
                        st.sidebar.success("Rezervasyon sonuçları alındı ✅")
            
            if last_event:
                # Session state'i güncelle ve debug bilgisi göster
                if "end" in last_event:
                    st.session_state.session_state = last_event["end"]
                    st.sidebar.success("State başarıyla güncellendi!")
                    
                # Debug - son rezervasyon yanıtını kontrol et
                if "end" in last_event and "reservation_response" in last_event["end"] and last_event["end"]["reservation_response"]:
                    last_res = last_event["end"]["reservation_response"][-1]
                    if hasattr(last_res, 'content'):
                        logger.info(f"Son rezervasyon yanıtı: {last_res.content[:100]}...")
                
                # Yanıtı işle
                final_response = get_last_response(last_event)
                
                # JSON formatı kontrolü ve temizleme
                if final_response and isinstance(final_response, str):
                    if final_response.startswith('{') and final_response.endswith('}'):
                        try:
                            match = re.search(r'"response":\s*"([^"]+)"', final_response)
                            if match:
                                final_response = clean_json_text(match.group(1))
                                logger.info(f"JSON formatı düzeltildi")
                        except Exception as e:
                            logger.error(f"JSON temizleme hatası: {str(e)}")
                
                # Yanıtı konuşma geçmişine ekle
                if final_response:
                    st.session_state.conversation.append(("assistant", final_response))
                else:
                    st.session_state.conversation.append(("assistant", "Üzgünüm, yanıt alınamadı."))
            
            # Sayfayı yenile
            st.rerun()
        
if __name__ == "__main__":
    main() 