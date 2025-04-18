#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import asyncio
import streamlit as st
from contextlib import AsyncExitStack, asynccontextmanager
import anyio
import functools
import time
import traceback

# MCP modüllerini yükle
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

# TCP modülünü yüklemeyi dene, yoksa sadece stdio modunu kullan
try:
    from mcp.client.tcp import tcp_client
    HAS_TCP_CLIENT = True
except ImportError:
    logging.warning("TCP istemci modülü bulunamadı, sadece stdio modu kullanılacak")
    HAS_TCP_CLIENT = False

# UI
from ui import (
    clean_json_text,
    safe_parse_message,
    create_state_display,
    render_header,
    render_conversation,
    render_sidebar_state,
    render_message_form
)

# LangGraph
from agent_graph.graph import create_graph, compile_workflow
from states.state import state

server = "gemini"
model = "gemini-2.0-flash"
model_endpoint = None
iterations = 40

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Streamlit oturum durumunu başlat veya sıfırla"""
    if "initialized" not in st.session_state:
        # İlk kez başlatılıyorsa, tüm durum değişkenlerini ayarla
        st.session_state.conversation = []
        st.session_state.form_submitted = False
        st.session_state.initialized = False
        st.session_state.is_loading = False  # Yükleme durumu başlangıçta kapalı
        st.session_state.session_state = state.copy()
        st.session_state.workflow = None
        st.session_state.session = None
        # MCP yolunu çevresel değişkenlerden al, yoksa varsayılan olarak göreli yolu kullan
        st.session_state.mcp_path = os.environ.get("MCP_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "google-sheets-mcp/sheet.py"))
        # Uzak MCP sunucu desteği ekle
        st.session_state.mcp_host = os.environ.get("MCP_HOST", None)  # "host:port" formatında, ör. "localhost:8000"
        st.session_state.use_remote_mcp = st.session_state.mcp_host is not None
        st.session_state.connection_id = None  # Bağlantı takibi için benzersiz ID
        st.session_state.connection_timestamp = 0  # Son bağlantı zamanı
        st.session_state.connection_active = False
        st.session_state.connection_attempts = 0
        st.session_state.max_connection_attempts = 3
        st.session_state.connection_timeout = 30  # Saniye cinsinden
        st.session_state.last_reset_time = time.time()

@asynccontextmanager
async def managed_mcp_connection(mcp_path):
    """Yeni, daha güvenilir MCP bağlantı yöneticisi"""
    connection_id = int(time.time() * 1000)  # Milisaniye cinsinden timestamp
    st.session_state.connection_id = connection_id
    st.session_state.connection_timestamp = time.time()
    st.session_state.connection_attempts += 1
    
    logger.info(f"MCP bağlantısı başlatılıyor (ID: {connection_id})")
    
    stack = AsyncExitStack()
    session = None
    tools = []
    
    try:
        # Uzak MCP sunucusu veya yerel sunucu kullanımını kontrol et
        if st.session_state.use_remote_mcp and HAS_TCP_CLIENT:
            logger.info(f"Uzak MCP kullanılacak: {st.session_state.mcp_host}")
            try:
                # Host:port formatını parçala
                host_parts = st.session_state.mcp_host.split(":")
                host = host_parts[0]
                port = int(host_parts[1]) if len(host_parts) > 1 else 8000
                
                logger.info(f"TCP MCP sunucusuna bağlanılıyor: {host}:{port}")
                
                # TCP bağlantısını oluştur - TCP istemcisi olduğundan emin olduğumuz için ImportError kontrolü yapmıyoruz
                try:
                    # Daha uzun bir zaman aşımı süresi ekle
                    logger.info(f"TCP bağlantısı oluşturuluyor, zaman aşımı: 120 saniye")
                    client_stream = tcp_client(host, port, timeout=120.0)
                    logger.info(f"TCP istemci başarıyla oluşturuldu")
                except Exception as e:
                    logger.error(f"TCP bağlantısı kurulurken hata oluştu: {e}")
                    st.error(f"TCP sunucuya bağlanırken hata: {e}")
                    st.session_state.mcp_connection = None
                    yield [], None, None
                    return

                # Oturum başlatma denemesi
                try:
                    logger.info("MCP oturumu başlatılıyor...")
                    session = ClientSession(client_stream)
                    logger.info("MCP oturumu başarıyla başlatıldı")
                    st.session_state.mcp_connection = session
                    # Burada MCP bağlantısı başarılı
                    logger.info("MCP bağlantısı kuruldu, arayüz hazırlanıyor...")
                    
                    # Asenkron kaynak yönetimi için stack kullanımı
                    await stack.__aenter__()
                    
                    # Araçları yüklemeyi dene
                    try:
                        logger.info(f"MCP araçları yükleniyor...")
                        tools_response = await session.list_tools()
                        tools = tools_response.tools
                        logger.info(f"MCP araçları yüklendi: {len(tools)} araç bulundu")
                        
                        # Bağlantı durumunu güncelle
                        st.session_state.connection_active = True
                        st.session_state.connection_attempts = 0  # Başarılı bağlantı olduğu için sıfırla
                        
                        # Graf ve iş akışını oluştur
                        try:
                            logger.info(f"Araçlar kullanılarak graf ve iş akışı oluşturuluyor...")
                            graph = create_graph(server=server, model=model, model_endpoint=model_endpoint, 
                                            tools=tools, session=session)
                            workflow = compile_workflow(graph)
                            logger.info(f"Graf ve iş akışı başarıyla oluşturuldu")
                            
                            # Session state'e kaydet
                            st.session_state.session = session
                            st.session_state.workflow = workflow
                            
                            # Context manager değerlerini döndür
                            yield tools, session, workflow
                            return
                        except Exception as e:
                            logger.error(f"Graf ve iş akışı oluşturulurken hata: {e}")
                            st.error(f"Graf ve iş akışı oluşturulamadı: {e}")
                            raise
                    except Exception as e:
                        logger.error(f"MCP araçları yüklenirken hata: {e}")
                        st.error(f"MCP araçları yüklenemedi: {e}")
                        raise
                    
                except Exception as e:
                    logger.error(f"MCP oturumu başlatılamadı: {e}")
                    st.error(f"MCP oturumu başlatılamadı: {e}")
                    st.session_state.mcp_connection = None
                    yield [], None, None
                    return
            except Exception as e:
                logger.error(f"Uzak MCP bağlantısı oluşturulurken hata: {e}")
                st.error(f"MCP sunucuya bağlanılamadı: {e}")
                st.session_state.mcp_connection = None
                yield [], None, None
                return
        else:
            # TCP bağlantısı mümkün değilse uzak MCP kullanılmak istense bile stdio moduna geç
            if st.session_state.use_remote_mcp and not HAS_TCP_CLIENT:
                logger.warning(f"TCP istemci modülü olmadığı için uzak MCP sunucusuna bağlanılamıyor. Yerel MCP kullanılacak: {mcp_path}")
                st.warning(f"TCP modülü bulunamadığı için uzak sunucuya bağlanılamıyor. Yerel MCP kullanılıyor.")
            else:
                logger.info(f"Yerel MCP kullanılacak: {mcp_path}")
                
            # Yerel Python dosyası kullanımı (mevcut kod)
            command = "python"
            server_params = StdioServerParameters(command=command, args=[mcp_path])
            client_stream = stdio_client(server_params)
        
            # Asenkron kaynak yönetimi için stack kullanımı
            await stack.__aenter__()
            
            # MCP istemci akışını oluştur
            try:
                logger.info(f"MCP istemci akışı oluşturuluyor...")
                stdio, write = await stack.enter_async_context(client_stream)
                logger.info(f"MCP istemci akışı başarıyla oluşturuldu")
            except Exception as e:
                logger.error(f"MCP istemci akışı oluşturulurken hata: {e}")
                st.error(f"MCP bağlantısı kurulamadı: {e}")
                raise
            
            # ClientSession oluştur ve başlat
            try:
                logger.info(f"MCP oturumu başlatılıyor...")
                session = ClientSession(stdio, write)
                await stack.enter_async_context(session)
                await session.initialize()
                logger.info(f"MCP oturumu başlatıldı (ID: {connection_id})")
            except Exception as e:
                logger.error(f"MCP oturumu başlatılırken hata: {e}")
                st.error(f"MCP oturumu başlatılamadı: {e}")
                raise
            
            # Kullanılabilir araçları al
            try:
                logger.info(f"MCP araçları yükleniyor...")
                tools_response = await session.list_tools()
                tools = tools_response.tools
                logger.info(f"MCP araçları yüklendi: {len(tools)} araç bulundu")
            except Exception as e:
                logger.error(f"MCP araçları yüklenirken hata: {e}")
                st.error(f"MCP araçları yüklenemedi: {e}")
                raise
            
            # Bağlantı durumunu güncelle
            st.session_state.connection_active = True
            st.session_state.connection_attempts = 0  # Başarılı bağlantı olduğu için sıfırla
            
            # Graf ve iş akışını oluştur
            try:
                logger.info(f"Araçlar kullanılarak graf ve iş akışı oluşturuluyor...")
                graph = create_graph(server=server, model=model, model_endpoint=model_endpoint, 
                                    tools=tools, session=session)
                workflow = compile_workflow(graph)
                logger.info(f"Graf ve iş akışı başarıyla oluşturuldu")
            except Exception as e:
                logger.error(f"Graf ve iş akışı oluşturulurken hata: {e}")
                st.error(f"Graf ve iş akışı oluşturulamadı: {e}")
                raise
            
            # Session state'e kaydet
            st.session_state.session = session
            st.session_state.workflow = workflow
            
            # Context manager değerlerini döndür
            yield tools, session, workflow
        
    except Exception as e:
        # Bağlantı başarısız olduğunda oturum durumunu güncelle
        logger.exception(f"MCP bağlantı hatası (ID: {connection_id}): {e}")
        st.session_state.connection_active = False
        yield [], None, None
        
    finally:
        # Context çıkışında kaynakları temizle
        if connection_id == st.session_state.connection_id:  # Hala aynı bağlantı ID ise
            try:
                logger.info(f"MCP bağlantısı kapatılıyor (ID: {connection_id})")
                await stack.__aexit__(None, None, None)
                st.session_state.connection_active = False
                logger.info(f"MCP bağlantısı başarıyla kapatıldı (ID: {connection_id})")
            except Exception as e:
                logger.error(f"MCP bağlantısını kapatırken hata (ID: {connection_id}): {e}")
                # Bağlantı zaten kapalı olabilir, durumu güncelle
                st.session_state.connection_active = False

async def reset_connection_if_needed():
    """Gerekirse bağlantıyı sıfırla"""
    current_time = time.time()
    
    # Bağlantı çok eskiyse veya aktif değilse sıfırla
    connection_age = current_time - st.session_state.connection_timestamp
    needs_reset = (
        not st.session_state.connection_active or
        connection_age > st.session_state.connection_timeout or
        current_time - st.session_state.last_reset_time > 300  # Her 5 dakikada bir sıfırla
    )
    
    if needs_reset and st.session_state.connection_attempts < st.session_state.max_connection_attempts:
        logger.info(f"Bağlantı sıfırlanıyor. Yaş: {connection_age}s, Aktif: {st.session_state.connection_active}")
        st.session_state.last_reset_time = current_time
        
        try:
            # Eğer önceki oturumlar varsa, bunları güvenli bir şekilde kapat
            if hasattr(st.session_state, "session") and st.session_state.session:
                try:
                    # Mevcut oturumu kullanmaya çalışma, sadece referansını temizle
                    st.session_state.session = None
                    st.session_state.workflow = None
                except Exception as e:
                    logger.warning(f"Önceki oturumu temizlerken hata: {e}")
            
            # Yeni bağlantı kur - ancak bu kodu kullanma, bunun yerine alttaki UI fonksiyonunda managed_mcp_connection kullanılacak
            return True
            
        except Exception as e:
            logger.exception(f"Bağlantı sıfırlama hatası: {e}")
            return False
    
    return st.session_state.connection_active

async def display_main_ui(state):
    """Ana UI'ı göster ve kullanıcı etkileşimlerini işle"""
    render_header()
    
    # Sistem durumu göstergesi
    if st.session_state.use_remote_mcp:
        st.info(f"💻 Uzak MCP sunucusu kullanılıyor: {st.session_state.mcp_host}")
    else:
        st.info(f"💻 Yerel MCP sunucusu kullanılıyor")
    
    # Mesaj yükleme göstergesi
    if hasattr(st.session_state, "is_loading") and st.session_state.is_loading:
        with st.status("İşlem devam ediyor...", expanded=True) as status:
            st.write("Yanıt hazırlanıyor, lütfen bekleyin...")
    
    render_conversation(st.session_state.conversation)
    render_sidebar_state(state)
    user_input = render_message_form()

    if st.session_state.form_submitted and user_input:
        st.session_state.conversation.append(("user", user_input))
        st.session_state.form_submitted = False
        
        # Yükleme durumunu aktif et
        st.session_state.is_loading = True
        st.rerun()  # UI'ı güncelle (yükleme göstergesi görünür olacak)

    # Eğer yükleme durumu aktifse ve işlem yapılmamışsa
    if hasattr(st.session_state, "is_loading") and st.session_state.is_loading:
        dict_inputs = state.copy()
        dict_inputs["research_question"] = [msg for role, msg in st.session_state.conversation if role == "user"]

        with st.spinner("Yanıt hazırlanıyor..."):
            # Yeni bağlantı yönetimi yaklaşımı kullanılıyor
            async with managed_mcp_connection(st.session_state.mcp_path) as (tools, session, workflow):
                if not session or not workflow:
                    st.error("MCP sunucusuna bağlanılamadı. Lütfen sayfayı yenileyip tekrar deneyin.")
                    st.session_state.conversation.append(("assistant", "Bağlantı hatası. Lütfen sayfayı yenileyip tekrar deneyin."))
                    # Yükleme durumu kapat
                    st.session_state.is_loading = False
                    st.rerun()
                    return
                
                try:
                    # İş akışını çalıştır
                    last_event = None
                    async for event in workflow.astream(dict_inputs, {"recursion_limit": iterations}):
                        last_event = event

                    if last_event and "end" in last_event:
                        st.session_state.session_state = last_event["end"]
                        final_response = ""

                        if "reservation_response" in last_event["end"]:
                            res = last_event["end"]["reservation_response"]
                            if isinstance(res, list) and res:
                                res = res[-1]  # Son yanıtı al
                                
                            # İki farklı yanıt formatını kontrol et
                            if hasattr(res, "content"):
                                content = res.content
                            elif isinstance(res, dict) and "content" in res:
                                content = res["content"]
                            else:
                                content = str(res)
                                
                            # İki olası durumu değerlendir:
                            # 1. İçerik zaten JSON formatında olabilir
                            # 2. İçerik düz metin olabilir
                            try:
                                if isinstance(content, str):
                                    # Eğer JSON-benzeri bir string ise, parse et
                                    if content.strip().startswith('{') and content.strip().endswith('}'):
                                        parsed = safe_parse_message(content)
                                        if "response" in parsed:
                                            final_response = clean_json_text(parsed["response"])
                                        else:
                                            # JSON var ama response alanı yok - ayrıştırma sorunu olabilir
                                            # ham içeriği göster
                                            final_response = clean_json_text(content)
                                    else:
                                        # Düz metin yanıtı - doğrudan göster
                                        final_response = clean_json_text(content)
                                else:
                                    # String olmayan veri tipi - metne dönüştür
                                    final_response = clean_json_text(str(content))
                            except Exception as e:
                                logger.error(f"Yanıt ayrıştırma hatası: {str(e)}")
                                logger.error(traceback.format_exc())
                                # Hata durumunda ham içeriği göster
                                final_response = clean_json_text(str(content))

                        st.session_state.conversation.append(("assistant", final_response or "Anlayamadım ama yardımcı olmaya çalışırım."))
                        # Yükleme durumunu kapat
                        st.session_state.is_loading = False
                        st.rerun()
                except anyio.ClosedResourceError:
                    logger.error(f"ClosedResourceError: Bağlantı kaynak hatası")
                    st.session_state.connection_active = False
                    st.session_state.conversation.append(("assistant", "Bağlantı hatası oluştu. Lütfen sorunuzu tekrar sorun."))
                    # Yükleme durumunu kapat
                    st.session_state.is_loading = False
                    st.rerun()
                except Exception as e:
                    logger.exception(f"İşlem sırasında hata: {e}")
                    st.session_state.conversation.append(("assistant", f"Üzgünüm, bir hata oluştu: {str(e)}"))
                    # Yükleme durumunu kapat
                    st.session_state.is_loading = False
                    st.rerun()

async def main():
    """Ana uygulama akışı"""
    # Sayfayı ayarla
    st.set_page_config(page_title="Altıkulaç Otel Asistanı", page_icon="🏨", layout="wide")
    
    # Oturum durumunu başlat
    initialize_session_state()
    
    # Ana UI'ı göster ve etkileşimleri işle
    await display_main_ui(state=st.session_state.session_state)
    
    # Uygulama ilk defa başlatılıyorsa, başlatıldı olarak işaretle
    if not st.session_state.initialized:
        st.session_state.initialized = True

if __name__ == "__main__":
    try:
        # Ana uygulamayı çalıştır
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Ana döngüde hata: {e}")
