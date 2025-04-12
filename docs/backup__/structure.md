# Proje Mimarisi

Bu belge, projenin güncel dizin yapısını ve içerdiği dosyaları açıklar.

## Dizin Yapısı

```
/
├── agent_graph/                # Ajan graf modülü
│   ├── __init__.py
│   └── graph.py                # Ana graf tanımları ve akış yönetimi
│
├── agents/                     # Ajanlar ve ilgili sınıflar
│   ├── __init__.py
│   ├── agents.py               # Farklı ajan tanımları
│   └── base_agent.py           # Temel ajan sınıfları
│
├── config/                     # Yapılandırma dosyaları
│   └── config.yaml             # Genel yapılandırma ayarları
│
├── database/                   # Veritabanı işlemleri
│   └── schema.py               # Veritabanı şeması ve modelleri
│
├── docs/                       # Dokümantasyon klasörü
│   └── structure.md            # Bu belge - proje yapısı açıklaması
│
├── models/                     # Model tanımları
│   ├── __init__.py
│   ├── deepseek_models.py      # DeepSeek model entegrasyonu
│   └── llm.py                  # Dil modeli yapılandırmaları
│
├── prompts/                    # Komut şablonları
│   ├── __init__.py
│   └── prompts.py              # Farklı LLM komut şablonları
│
├── services/                   # Servis entegrasyonları
│   └── __init__.py
│
├── states/                     # Durum yönetimi
│   ├── __init__.py
│   └── state.py                # Durum sınıfları ve yardımcıları
│
├── tests/                      # Test dizini
│   ├── __init__.py
│   └── test_flow.py            # Akış testleri
│
├── tools/                      # Araçlar
│   ├── __init__.py
│   ├── basic_scraper.py        # Temel web kazıma araçları
│   └── tools.py                # Yardımcı araçlar
│
├── utils/                      # Yardımcı fonksiyonlar
│   ├── __init__.py
│   └── utils.py                # Genel yardımcı işlevler
│
├── venv/                       # Sanal ortam (versiyon kontrolüne dahil değil)
│
├── .env                        # Ortam değişkenleri
├── README.md                   # Proje açıklaması
├── app.py                      # Ana uygulama / başlangıç noktası
└── requirements.txt            # Bağımlılıklar
```

## Bileşen Açıklamaları

### Ajanlar ve Graf
- **agent_graph/**: Agent ve akış grafiği yönetimi
- **agents/**: Farklı ajanların tanımı ve davranışları

### Temel Altyapı
- **config/**: Yapılandırma dosyaları ve ayarlar
- **database/**: Veritabanı şeması ve etkileşimleri
- **models/**: Dil modeli entegrasyonları ve yapılandırmaları

### Yardımcı Modüller
- **prompts/**: Dil modelleri için komut şablonları
- **services/**: Dış servislerle entegrasyonlar
- **states/**: Uygulama durum yönetimi sınıfları
- **tools/**: Web kazıma ve diğer yardımcı araçlar
- **utils/**: Genel yardımcı fonksiyonlar

### Diğer
- **docs/**: Proje dokümantasyonu
- **tests/**: Test betikleri ve senaryoları

## Bağımlılıklar
Aşağıdaki temel kütüphaneler kullanılmaktadır:
- langchain ve langgraph (Ajan ve graf yönetimi)
- openai (API entegrasyonu)
- streamlit (Kullanıcı arayüzü)
- flask (API hizmetleri)
- python-dotenv (Ortam değişkenleri)
- sqlalchemy (Veritabanı etkileşimleri)
- ve diğerleri (requirements.txt dosyasına bakın) 