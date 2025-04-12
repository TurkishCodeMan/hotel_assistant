"""
Google Sheets Aracı (Tool)
-----------------------
Rezervasyon agent'ının Google Sheets ile etkileşimde bulunması için kullanılan araç.
"""

import logging
import json
from datetime import datetime

from langchain_core.messages import HumanMessage

from services.sheets_service import (
    get_all_reservations,
    add_reservation,
    update_reservation,
    delete_reservation,
    check_availability
)
from states.state import AgentGraphState

# Logger ayarları
logger = logging.getLogger(__name__)

# Varsayılan sayfa adı
DEFAULT_SPREADSHEET = "REZERVASYON"
DEFAULT_WORKSHEET = "Rezervasyonlar"

def fetch_reservations(state: AgentGraphState, params=None):
    """
    Rezervasyonları getiren fonksiyon.
    
    Args:
        state: Ajan durumu
        params: Parametreler (JSON formatında)
        
    Returns:
        Güncellenmiş durum
    """
    try:
        from services.sheets_service import get_all_reservations
        from agents.tools_agents import DEFAULT_SPREADSHEET, DEFAULT_WORKSHEET
        from langchain_core.messages import HumanMessage
        import json
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Debug: Gelen parametreleri göster
        print(f"DEBUG: fetch_reservations başladı. Parametre: {params}")
        
        # Parametre bilgilerini al
        params_data = None
        if params is not None:
            params_data = params
        
        # Spreadsheet ve worksheet başlangıç değerlerini ayarla
        spreadsheet_name = DEFAULT_SPREADSHEET
        worksheet_name = DEFAULT_WORKSHEET
        customer_name = None
        
        # Parametre varsa ve geçerli bir formattaysa kullan
        if params_data:
            print(f"DEBUG: Parametre mevcut: {params_data}")
            try:
                params_json = json.loads(params_data)
                customer_name = params_json.get("customer_name")
                spreadsheet_name = params_json.get("spreadsheet_name", DEFAULT_SPREADSHEET)
                worksheet_name = params_json.get("worksheet_name", DEFAULT_WORKSHEET)
                print(f"DEBUG: Çözümlenen müşteri adı: {customer_name}")
                print(f"DEBUG: Kullanılacak tablo: {spreadsheet_name}.{worksheet_name}")
            except json.JSONDecodeError:
                print(f"DEBUG: JSON ayrıştırma hatası: {params_data}")
        else:
            print("DEBUG: Parametre boş veya yok. Tüm rezervasyonlar listelenecek.")
        
        print(f"DEBUG: Şu parametrelerle rezervasyon sorgusu yapılıyor - Tablo: {spreadsheet_name}, Sayfa: {worksheet_name}, Müşteri: {customer_name}")
        
        # Rezervasyonları getir
        reservations = get_all_reservations(spreadsheet_name, worksheet_name)
        print(f"DEBUG: Toplam {len(reservations)} rezervasyon bulundu")
        
        # Eğer müşteri adı belirtilmişse, filtreleme yap
        if customer_name:
            filtered_reservations = [r for r in reservations if r.get('customer_name', '').lower() == customer_name.lower()]
            print(f"DEBUG: '{customer_name}' müşterisi için {len(filtered_reservations)} rezervasyon filtrelendi.")
            reservations = filtered_reservations
        
        # Sonucu hazırla
        if reservations:
            formatted_reservations = []
            for res in reservations:
                # Her bir rezervasyonu biçimlendir
                formatted = {
                    'id': res.get('reservation_id', 'N/A'),
                    'name': res.get('customer_name', 'N/A'),
                    'check_in': res.get('check_in_date', 'N/A'),
                    'check_out': res.get('check_out_date', 'N/A'),
                    'adults': res.get('adults', '0'),
                    'children': res.get('children', '0'),
                    'room_type': res.get('room_type', 'N/A'),
                    'price': res.get('price', '0'),
                    'status': res.get('status', 'N/A'),
                    'created_at': res.get('created_at', 'N/A')
                }
                formatted_reservations.append(formatted)
            
            result = {
                "success": True,
                "count": len(reservations),
                "reservations": formatted_reservations
            }
        else:
            result = {
                "success": True,
                "count": 0,
                "message": "Hiç rezervasyon bulunamadı."
            }
        
        print(f"DEBUG: Hazırlanan sonuç: {result}")
        
        # Durumu güncelle
        state["reservations_result"] = state.get("reservations_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        print("DEBUG: fetch_reservations işlemi tamamlandı.")
        return state
        
    except Exception as e:
        logger.error(f"Rezervasyonlar alınırken hata: {str(e)}")
        print(f"DEBUG HATA: Rezervasyonlar alınırken hata oluştu: {str(e)}")
        
        # Hata durumu
        result = {
            "success": False,
            "error": str(e),
            "message": "Rezervasyonları getirirken bir hata oluştu."
        }
        
        state["reservations_result"] = state.get("reservations_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state

def update_existing_reservation(state: AgentGraphState, params=None):
    """
    Mevcut bir rezervasyonu günceller.
    
    Args:
        state: Ajan durum nesnesi
        params: Güncelleme verileri (JSON formatında)
        
    Returns:
        Güncellenmiş durum
    """
    try:
        # Parametreleri al
        params_data = params() if callable(params) else params
        if hasattr(params_data, 'content'):
            params_data = params_data.content
            
        # JSON parametrelerini ayrıştır
        if not isinstance(params_data, str) or '{' not in params_data:
            result = {
                "success": False,
                "error": "Geçersiz parametre formatı",
                "message": "Güncelleme bilgileri JSON formatında gönderilmelidir."
            }
        else:
            try:
                params_json = json.loads(params_data)
                
                # Gerekli alanları kontrol et
                if 'reservation_id' not in params_json:
                    result = {
                        "success": False,
                        "error": "Rezervasyon ID'si eksik",
                        "message": "Güncellenecek rezervasyonun ID'si belirtilmelidir."
                    }
                else:
                    # Spreadsheet bilgileri
                    spreadsheet_name = params_json.pop('spreadsheet_name', DEFAULT_SPREADSHEET)
                    worksheet_name = params_json.pop('worksheet_name', DEFAULT_WORKSHEET)
                    
                    # Rezervasyon ID'sini al
                    reservation_id = params_json.pop('reservation_id')
                    
                    # Güncelleme verileri (ID hariç tüm bilgiler)
                    updated_data = params_json
                    
                    # Rezervasyonu güncelle
                    success = update_reservation(spreadsheet_name, reservation_id, updated_data, worksheet_name)
                    
                    if success:
                        result = {
                            "success": True,
                            "message": f"Rezervasyon (ID: {reservation_id}) başarıyla güncellendi.",
                            "updated_fields": list(updated_data.keys())
                        }
                    else:
                        result = {
                            "success": False,
                            "error": "Rezervasyon güncellenirken bir hata oluştu.",
                            "message": "Rezervasyon bulunamadı veya güncellenemedi."
                        }
            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "error": "Geçersiz JSON formatı",
                    "message": "Güncelleme verileri geçerli bir JSON formatında olmalıdır."
                }
        
        # Durumu güncelle
        state["update_reservation_result"] = state.get("update_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state
        
    except Exception as e:
        logger.error(f"Rezervasyon güncellenirken hata: {str(e)}")
        
        # Hata durumu
        result = {
            "success": False,
            "error": str(e),
            "message": "Rezervasyon güncellenirken bir hata oluştu."
        }
        
        state["update_reservation_result"] = state.get("update_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state

def delete_existing_reservation(state: AgentGraphState, params=None):
    """
    Bir rezervasyonu siler.
    
    Args:
        state: Ajan durum nesnesi
        params: Silme parametreleri (JSON formatında)
        
    Returns:
        Güncellenmiş durum
    """
    try:
        # Parametreleri al
        params_data = params() if callable(params) else params
        if hasattr(params_data, 'content'):
            params_data = params_data.content
            
        # JSON parametrelerini ayrıştır
        if not isinstance(params_data, str) or '{' not in params_data:
            result = {
                "success": False,
                "error": "Geçersiz parametre formatı",
                "message": "Silme parametreleri JSON formatında gönderilmelidir."
            }
        else:
            try:
                params_json = json.loads(params_data)
                
                # Gerekli alanları kontrol et
                if 'reservation_id' not in params_json:
                    result = {
                        "success": False,
                        "error": "Rezervasyon ID'si eksik",
                        "message": "Silinecek rezervasyonun ID'si belirtilmelidir."
                    }
                else:
                    # Spreadsheet bilgileri
                    spreadsheet_name = params_json.get('spreadsheet_name', DEFAULT_SPREADSHEET)
                    worksheet_name = params_json.get('worksheet_name', DEFAULT_WORKSHEET)
                    
                    # Rezervasyon ID'sini al
                    reservation_id = params_json.get('reservation_id')
                    
                    # Rezervasyonu sil
                    success = delete_reservation(spreadsheet_name, reservation_id, worksheet_name)
                    
                    if success:
                        result = {
                            "success": True,
                            "message": f"Rezervasyon (ID: {reservation_id}) başarıyla silindi."
                        }
                    else:
                        result = {
                            "success": False,
                            "error": "Rezervasyon silinirken bir hata oluştu.",
                            "message": "Rezervasyon bulunamadı veya silinemedi."
                        }
            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "error": "Geçersiz JSON formatı",
                    "message": "Silme parametreleri geçerli bir JSON formatında olmalıdır."
                }
        
        # Durumu güncelle
        state["delete_reservation_result"] = state.get("delete_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state
        
    except Exception as e:
        logger.error(f"Rezervasyon silinirken hata: {str(e)}")
        
        # Hata durumu
        result = {
            "success": False,
            "error": str(e),
            "message": "Rezervasyon silinirken bir hata oluştu."
        }
        
        state["delete_reservation_result"] = state.get("delete_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state

def check_room_availability(state: AgentGraphState, params=None):
    """
    Oda müsaitliğini kontrol eder.
    
    Args:
        state: Ajan durum nesnesi
        params: Kontrol parametreleri (JSON formatında)
        
    Returns:
        Güncellenmiş durum
    """
    try:
        # Parametreleri al
        params_data = params() if callable(params) else params
        if hasattr(params_data, 'content'):
            params_data = params_data.content
            
        # JSON parametrelerini ayrıştır
        if not isinstance(params_data, str) or '{' not in params_data:
            result = {
                "success": False,
                "error": "Geçersiz parametre formatı",
                "message": "Kontrol parametreleri JSON formatında gönderilmelidir."
            }
        else:
            try:
                params_json = json.loads(params_data)
                
                # Gerekli alanları kontrol et
                required_fields = ['check_in_date', 'check_out_date']
                missing_fields = [field for field in required_fields if field not in params_json]
                
                if missing_fields:
                    result = {
                        "success": False,
                        "error": f"Eksik alanlar: {', '.join(missing_fields)}",
                        "message": "Giriş ve çıkış tarihleri belirtilmelidir."
                    }
                else:
                    # Kontrol parametreleri
                    check_in_date = params_json.get('check_in_date')
                    check_out_date = params_json.get('check_out_date')
                    adults = int(params_json.get('adults', 2))
                    children = int(params_json.get('children', 0))
                    room_type = params_json.get('room_type')
                    
                    # Müsaitlik kontrolü yap
                    availability = check_availability(
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        adults=adults,
                        children=children,
                        room_type=room_type
                    )
                    
                    # Sonucu hazırla
                    result = {
                        "success": True,
                        "check_in_date": check_in_date,
                        "check_out_date": check_out_date,
                        "adults": adults,
                        "children": children,
                        "available_rooms": availability.get('available_rooms', [])
                    }
            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "error": "Geçersiz JSON formatı",
                    "message": "Kontrol parametreleri geçerli bir JSON formatında olmalıdır."
                }
            except ValueError:
                result = {
                    "success": False,
                    "error": "Geçersiz sayısal değer",
                    "message": "Yetişkin ve çocuk sayıları tam sayı olmalıdır."
                }
        
        # Durumu güncelle
        state["availability_result"] = state.get("availability_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state
        
    except Exception as e:
        logger.error(f"Müsaitlik kontrolü sırasında hata: {str(e)}")
        
        # Hata durumu
        result = {
            "success": False,
            "error": str(e),
            "message": "Müsaitlik kontrolü sırasında bir hata oluştu."
        }
        
        state["availability_result"] = state.get("availability_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        return state

def add_reservation_advanced_tool(state: AgentGraphState, params=None):
    """
    Yeni bir rezervasyon ekler ve sadece güncellenmiş "add_reservation_result" değerini döndürür.
    
    Args:
        state: Ajan durum nesnesi
        params: Rezervasyon verileri (JSON formatında)
        
    Returns:
        dict: Güncellenmiş "add_reservation_result" değeri
    """
    try:
        print('--------------------------ADVANCED RESERVATION TOOL STARTED')
        print(f"Gelen params değeri: {params}")
        print('STATE',state)
        
        # Lambda fonksiyonunu çağırma kontrolü
        params_data = params() if callable(params) else params
        print(f"İşlenmiş params değeri: {params_data}")
        
        # JSON params ayrıştırma
        param_json_data = None
        
        # Parametre tipine göre işleme
        if params_data is None:
            print("Parametre değeri boş")
            param_json_data = {}
        elif isinstance(params_data, list) and len(params_data) == 0:
            print("Parametre boş liste olarak geldi")
            param_json_data = {}
        elif isinstance(params_data, list) and len(params_data) > 0:
            print(f"Parametre liste olarak geldi, ilk eleman kullanılıyor: {params_data[0]}")
            if isinstance(params_data[0], str):
                try:
                    param_json_data = json.loads(params_data[0])
                except json.JSONDecodeError:
                    param_json_data = {"raw_data": params_data[0]}
            else:
                param_json_data = params_data[0]
        elif isinstance(params_data, str):
            try:
                if params_data.strip():  # Boş string değilse
                    param_json_data = json.loads(params_data)
                    print(f"JSON başarıyla ayrıştırıldı: {param_json_data}")
                else:
                    print("Boş JSON string alındı")
                    param_json_data = {}
            except json.JSONDecodeError as e:
                print(f"JSON ayrıştırma hatası: {e}")
                print(f"Ham veri: {params_data}")
        elif isinstance(params_data, dict):
            param_json_data = params_data
            print(f"Parametre zaten dictionary: {param_json_data}")
                
        # Eğer hala param_json_data None ise, hata döndür
        if param_json_data is None:
            result = {
                "success": False,
                "error": "Geçersiz parametre formatı",
                "message": "Rezervasyon bilgileri JSON formatında gönderilmelidir.",
                "debug_info": f"Alınan veri: {params}"
            }
        else:
            # Gerekli alanları kontrol et
            required_fields = ['customer_name', 'check_in_date', 'check_out_date', 'room_type']
            missing_fields = [field for field in required_fields if field not in param_json_data]
            
            if missing_fields:
                result = {
                    "success": False,
                    "error": f"Eksik alanlar: {', '.join(missing_fields)}",
                    "message": "Gerekli tüm rezervasyon bilgilerini giriniz."
                }
            else:
                # Rezervasyon verileri
                reservation_data = {
                    'customer_name': param_json_data.get('customer_name'),
                    'check_in_date': param_json_data.get('check_in_date'),
                    'check_out_date': param_json_data.get('check_out_date'),
                    'adults': param_json_data.get('adults', 2),
                    'children': param_json_data.get('children', 0),
                    'room_type': param_json_data.get('room_type'),
                    'price': param_json_data.get('price', 0),
                    'status': param_json_data.get('status', 'Confirmed')
                }
                
                # Oda tipini standardize et
                room_type = reservation_data['room_type']
                if room_type and isinstance(room_type, str):
                    if room_type.lower() in ["suit", "suıt", "süit"]:
                        reservation_data['room_type'] = "Suite"
                        # Fiyatı güncelle
                        reservation_data['price'] = 250
                    elif room_type.lower() == "standard":
                        reservation_data['price'] = 100
                    elif room_type.lower() == "deluxe":
                        reservation_data['price'] = 150
                
                # Spreadsheet bilgileri
                spreadsheet_name = param_json_data.get('spreadsheet_name', DEFAULT_SPREADSHEET)
                worksheet_name = param_json_data.get('worksheet_name', DEFAULT_WORKSHEET)
                
                # Rezervasyonu ekle
                print(f'CALLING ADD_RESERVATION WITH: {reservation_data}')
                success = add_reservation(spreadsheet_name, reservation_data, worksheet_name)
                print('ADVANCED RESERVATION SUCCESS:', success)
                if success:
                    result = {
                        "success": True,
                        "message": "Rezervasyon başarıyla eklendi.",
                        "reservation": reservation_data
                    }
                else:
                    result = {
                        "success": False,
                        "error": "Rezervasyon eklenirken bir hata oluştu.",
                        "message": "Lütfen daha sonra tekrar deneyin."
                    }
        
        # Durumu güncelle
        state["add_reservation_result"] = state.get("add_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        print(result,'RESULT')
        print('--------------------------ADVANCED RESERVATION TOOL COMPLETED')
        # Sadece güncellenmiş add_reservation_result değerini döndür
        return state
        
    except Exception as e:
        logger.error(f"Rezervasyon eklenirken hata: {str(e)}")
        
        # Hata durumu
        result = {
            "success": False,
            "error": str(e),
            "message": "Rezervasyon eklenirken bir hata oluştu."
        }
        
        state["add_reservation_result"] = state.get("add_reservation_result", []) + [
            HumanMessage(role="system", content=str(result))
        ]
        
        print('--------------------------ADVANCED RESERVATION TOOL ERROR')
        # Sadece güncellenmiş add_reservation_result değerini döndür
        return state 