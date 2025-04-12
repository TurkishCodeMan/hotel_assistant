#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Otel Rezervasyon Asistanı - Konsol Arayüzü
-----------------------------------------
Basit konsol arayüzü ile otel rezervasyon asistanı.
"""

import os
import json
import logging
from typing import Dict, Any

# Özel modülleri içe aktar
from agent_graph.graph import create_graph, compile_workflow
from states.state import get_agent_graph_state,state
# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Model ayarları
server = 'gemini'
model = 'gemini-2.0-flash'
model_endpoint = None
iterations = 40

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
                print(f"Eval hatası: {str(e)}")
                return {}
    except Exception as e:
        print(f"Mesaj ayrıştırma hatası: {str(e)}")
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
            
            # ÖNCELİK 1: Rezervasyon ekleme sonuçlarını kontrol et (Sadece bu işlem yapıldığında)
            if "add_reservation_result" in end_data and end_data["add_reservation_result"]:
                add_result = end_data["add_reservation_result"][-1]  # Son yanıtı al
                
                # Eğer yeni bir mesaj geldiyse ve bu verisi yoksa
                if "reservation_response" in end_data and end_data["reservation_response"] and add_result.get("_shown", False):
                    # Bu veri daha önce gösterilmiş, artık gösterilmemeli
                    # Reservation yanıtına ilerle
                    pass
                elif hasattr(add_result, 'content'):
                    try:
                        print(f"DEBUG - Reservasyon ekleme ham içerik: {add_result.content[:200]}...")
                        result_dict = safe_parse_message(add_result.content)
                        print(f"DEBUG - Ayrıştırılmış rezervasyon: {result_dict}")
                        
                        # Bu rezervasyon sonucu gösterildi olarak işaretle
                        if hasattr(add_result, '_shown'):
                            add_result._shown = True
                        else:
                            setattr(add_result, '_shown', True)
                        
                        if result_dict.get("success"):
                            # Başarılı rezervasyon ekleme
                            reservation = result_dict.get("reservation", {})
                            
                            # Rezervasyon bilgilerini kontrol et
                            if not reservation:
                                print("DEBUG - Rezervasyon bilgileri boş, alternatif çözüm deneniyor...")
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
                                    print(f"DEBUG - Alternatif rezervasyon verileri oluşturuldu: {reservation}")
                            
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
                        print(f"Rezervasyon ekleme sonuç işleme hatası: {str(e)}")
                        return "Rezervasyon işlemi tamamlandı, ancak sonuç işlenirken bir hata oluştu."

            # ÖNCELİK 2: Reservation yanıtını kontrol et (Normal sohbet akışı için)
            if "reservation_response" in end_data and end_data["reservation_response"]:
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
            
            # ÖNCELİK 3: Diğer yanıt türlerini kontrol et
            # Rezervasyon sonuçlarını kontrol et
            if "reservations_result" in end_data and end_data["reservations_result"]:
                res_result = end_data["reservations_result"][-1]  # Son yanıtı al
                
                # Eğer yeni bir mesaj geldiyse ve bu verisi daha önce gösterildiyse atla
                if "reservation_response" in end_data and end_data["reservation_response"] and res_result.get("_shown", False):
                    # Bu veri daha önce gösterilmiş, artık gösterilmemeli
                    # Reservation yanıtına ilerle
                    pass
                elif hasattr(res_result, 'content'):
                    try:
                        print(f"DEBUG - Rezervasyon listeleme ham içerik: {res_result.content[:200]}...")
                        raw_content = res_result.content
                        
                        # İçerik bir string olabilir
                        if isinstance(raw_content, str):
                            result_dict = safe_parse_message(raw_content)
                        # Veya doğrudan bir dict olabilir
                        elif isinstance(raw_content, dict):
                            result_dict = raw_content
                        else:
                            # Son çare olarak stringify edip parse etmeyi dene
                            result_dict = safe_parse_message(str(raw_content))
                        
                        print(f"DEBUG - Ayrıştırılmış rezervasyon listesi: {result_dict}")
                        
                        # Bu rezervasyon sonucu gösterildi olarak işaretle
                        if hasattr(res_result, '_shown'):
                            res_result._shown = True
                        else:
                            setattr(res_result, '_shown', True)
                        
                        # Eğer rezervasyonlar varsa, onları güzel bir şekilde formatlayarak göster
                        if isinstance(result_dict, dict) and result_dict.get("success") and result_dict.get("count", 0) > 0:
                            reservations = result_dict.get("reservations", [])
                            formatted_response = f"📋 {result_dict.get('count')} adet rezervasyon bulundu:\n\n"
                            print('RESERVATIONS',reservations)
                            for i, res in enumerate(reservations, 1):
                                formatted_response += f"{i}. 🏨 Rezervasyon ID: {res.get('reservation_id', 'N/A')}\n"
                                formatted_response += f"   👤 Müşteri: {res.get('customer_name', 'Misafir')}\n"
                                formatted_response += f"   📅 Tarih: {res.get('check_in_date', 'N/A')} → {res.get('check_out_date', 'N/A')}\n"
                                formatted_response += f"   🛏️ Oda Tipi: {res.get('room_type', 'N/A')}\n"
                                formatted_response += f"   👪 Kişi: {res.get('adults', '1')} yetişkin, {res.get('children', '0')} çocuk\n"
                                formatted_response += f"   🔖 Durum: {res.get('status', 'N/A')}\n\n"
                            
                            return formatted_response
                        elif isinstance(result_dict, dict) and result_dict.get("success") and result_dict.get("count", 0) == 0:
                            return "Aradığınız kriterlere uygun rezervasyon bulunamadı."
                        # Alternatif veri yapısı - API doğrudan rezervasyon listesi döndürüyorsa
                        elif isinstance(result_dict, list) and len(result_dict) > 0:
                            # API doğrudan liste döndürmüş olabilir
                            reservations = result_dict
                            formatted_response = f"📋 {len(reservations)} adet rezervasyon bulundu:\n\n"
                            
                            for i, res in enumerate(reservations, 1):
                                formatted_response += f"{i}. 🏨 Rezervasyon ID: {res.get('reservation_id', 'N/A')}\n"
                                formatted_response += f"   👤 Müşteri: {res.get('customer_name', 'Misafir')}\n"
                                formatted_response += f"   📅 Tarih: {res.get('check_in_date', 'N/A')} → {res.get('check_out_date', 'N/A')}\n"
                                formatted_response += f"   🛏️ Oda Tipi: {res.get('room_type', 'N/A')}\n"
                                formatted_response += f"   👪 Kişi: {res.get('adults', '1')} yetişkin, {res.get('children', '0')} çocuk\n"
                                formatted_response += f"   🔖 Durum: {res.get('status', 'N/A')}\n\n"
                            
                            return formatted_response
                        elif isinstance(result_dict, list) and len(result_dict) == 0:
                            return "Aradığınız kriterlere uygun rezervasyon bulunamadı."
                        else:
                            # Rezervasyon bilgileri uygun formatta değil
                            error_msg = "Rezervasyon bilgileri uygun formatta değil"
                            if isinstance(result_dict, dict):
                                error_msg = result_dict.get("error", error_msg)
                            return f"❌ Rezervasyon listesi görüntülenemedi: {error_msg}"
                    except Exception as e:
                        print(f"Rezervasyon listeleme sonuç işleme hatası: {str(e)}")
                        # Son çare: Ham veriyi direkt dönmeyi dene
                        try:
                            if isinstance(raw_content, dict) and "reservations" in raw_content:
                                reservations = raw_content.get("reservations", [])
                                formatted_response = f"📋 {len(reservations)} adet rezervasyon bulundu:\n\n"
                                
                                for i, res in enumerate(reservations, 1):
                                    formatted_response += f"{i}. 🏨 Rezervasyon: {res}\n\n"
                                
                                return formatted_response
                        except:
                            pass
                        
                        return "Rezervasyon listesi alınırken bir hata oluştu: {str(e)}"
                else:
                    print(f"DEBUG - reservations_result içeriği yok: {res_result}")
                    return "Rezervasyon listesi alınamadı: İçerik bulunamadı."
            
            # Rezervasyon güncelleme sonuçlarını kontrol et
            if "update_reservation_result" in end_data and end_data["update_reservation_result"]:
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
                        print(f"Rezervasyon güncelleme sonuç işleme hatası: {str(e)}")
            
            # Rezervasyon silme sonuçlarını kontrol et
            if "delete_reservation_result" in end_data and end_data["delete_reservation_result"]:
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
                        print(f"Rezervasyon silme sonuç işleme hatası: {str(e)}")
            
            # Oda müsaitliği kontrolü sonuçlarını kontrol et
            if "availability_result" in end_data and end_data["availability_result"]:
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
                        print(f"Müsaitlik kontrol sonuç işleme hatası: {str(e)}")
            
            # Support yanıtını kontrol et
            if "support_response" in end_data and end_data["support_response"]:
                support_resp = end_data["support_response"][-1]  # Son yanıtı al
                if hasattr(support_resp, 'content'):
                    content = support_resp.content
                    
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

            # Understanding yanıtını kontrol et
            if "understanding_response" in end_data and end_data["understanding_response"]:
                und_resp = end_data["understanding_response"][-1]  # Son yanıtı al
                if hasattr(und_resp, 'content'):
                    content = und_resp.content
                    
                    # 1. Eğer JSON formatında bir yanıt ve clarification_question içeriyorsa
                    if content.startswith('{') and '"clarification_question"' in content:
                        try:
                            import re
                            match = re.search(r'"clarification_question":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON clarification_question çıkarma hatası: {str(e)}")
                    
                    # 2. Response alanını kontrol et
                    if content.startswith('{') and '"response"' in content:
                        try:
                            import re
                            match = re.search(r'"response":\s*"([^"]*)"', content)
                            if match:
                                return clean_json_text(match.group(1))
                        except Exception as e:
                            logger.error(f"JSON response çıkarma hatası: {str(e)}")
                    
                    # 3. Normal JSON parsing dene
                    try:
                        result_dict = safe_parse_message(content)
                        if result_dict and "clarification_question" in result_dict:
                            return clean_json_text(result_dict["clarification_question"])
                        elif result_dict and "response" in result_dict:
                            return clean_json_text(result_dict["response"])
                    except Exception as e:
                        logger.error(f"JSON parse hatası: {str(e)}")
                    
                    # 4. Yukarıdaki yöntemler başarısız olursa, temizlenmiş ham içeriği döndür
                    return clean_json_text(content)

        return "Üzgünüm, yanıt işlenirken bir sorun oluştu."
    except Exception as e:
        logger.error(f"Yanıt işleme hatası: {str(e)}")
        return "Üzgünüm, yanıt işlenirken bir hata oluştu."

def main():
    """Ana uygulama fonksiyonu"""
    print("🏨 Otel Rezervasyon Asistanı")
    print("-" * 30)
    
    try:
        print("Graf ve iş akışı oluşturuluyor...")
        graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
        workflow = compile_workflow(graph)
        print("Graf ve iş akışı başarıyla oluşturuldu.")
        
        verbose = False
        
        # Konuşma geçmişi ve state yönetimi
        conversation_history = []
        session_state = state
        
        # Yanıt kontrolü için
        last_add_reservation_id = None
        
        while True:
            query = input("\nSorunuzu yazın (çıkmak için 'exit'): ")
            if query.lower() == "exit":
                break
            
            # Konuşma geçmişine ekle
            conversation_history.append(query)
            
            # research_question alanına konuşma geçmişini ekle
            # Önceki state'i koru, sadece research_question güncelleniyor
            dict_inputs = session_state.copy() if session_state else {}
            dict_inputs["research_question"] = conversation_history
            
            limit = {"recursion_limit": iterations}
            
            print("\nYanıt bekleniyor...\n")
            
            last_event = None
            for event in workflow.stream(dict_inputs, limit):
                if verbose:
                    print("\nDurum Sözlüğü:", event)
                last_event = event
            
            if last_event:
                # Son event'i session_state olarak sakla
                if "end" in last_event:
                    session_state = last_event["end"]
                
                # Debug bilgisi - Reservation yanıtını doğrudan alalım ve gösterelim
                if "end" in last_event and "reservation_response" in last_event["end"] and last_event["end"]["reservation_response"]:
                    last_res = last_event["end"]["reservation_response"][-1]
                    if hasattr(last_res, 'content'):
                        print(f"DEBUG - Son rezervasyon yanıtı: {last_res.content[:100]}...")
                
                # Yanıt kontrolü - add_reservation_result ile reservation_response arasındaki ilişkiyi yönet
                has_new_add_result = False
                if "end" in last_event and "add_reservation_result" in last_event["end"] and last_event["end"]["add_reservation_result"]:
                    add_result = last_event["end"]["add_reservation_result"][-1]
                    
                    # Kontrolü kolaylaştırmak için, sonucu bir ID gibi kullanabiliriz
                    add_result_content = ""
                    if hasattr(add_result, 'content'):
                        add_result_content = str(add_result.content)
                        
                    # Eğer bu yeni bir rezervasyon sonucuysa
                    if add_result_content != last_add_reservation_id:
                        has_new_add_result = True
                        last_add_reservation_id = add_result_content
                
                # Yanıtı al - eğer yeni bir rezervasyon sonucu varsa, o gösterilsin
                final_response = ""
                if has_new_add_result:
                    # Yeni rezervasyon sonucu varsa, bunu göster
                    temp_event = {"end": {"add_reservation_result": last_event["end"]["add_reservation_result"]}}
                    final_response = get_last_response(temp_event)
                else:
                    # Yoksa, normal yanıt akışını izle ama add_reservation_result'ı dikkate alma
                    if "end" in last_event and "add_reservation_result" in last_event["end"]:
                        # Geçici bir kopya oluştur ve add_reservation_result'ı çıkar
                        temp_event = last_event.copy()
                        temp_event["end"] = last_event["end"].copy()
                        temp_event["end"].pop("add_reservation_result", None)
                        final_response = get_last_response(temp_event)
                    else:
                        # Normal akış
                        final_response = get_last_response(last_event)
                
                if verbose:
                    print('---', last_event)
                
                # Acil durum JSON temizleme - yanıt JSON formatında gelirse temizle
                if final_response and isinstance(final_response, str):
                    # JSON yapısı kontrolü
                    if final_response.startswith('{') and final_response.endswith('}'):
                        try:
                            # JSON yanıtından sadece response değerini çıkarmaya çalış
                            import re
                            match = re.search(r'"response":\s*"([^"]+)"', final_response)
                            if match:
                                # response değerini alıp temizle
                                final_response = clean_json_text(match.group(1))
                                print(f"JSON formatı düzeltildi: {final_response}")
                        except Exception as e:
                            print(f"JSON temizleme hatası: {str(e)}")
                
                if final_response:
                    print(f"🤖 Asistan: {final_response}\n")
                else:
                    print("❌ Yanıt alınamadı.")
    
    except Exception as e:
        logger.error(f"Uygulama hatası: {str(e)}")
        print(f"\n❌ Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
