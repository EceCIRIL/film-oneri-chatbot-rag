# Akbank GenAI Bootcamp Projesi: RAG Tabanlı Film Öneri Chatbotu



## 1. Projenin Amacı 

Bu proje, Retrieval-Augmented Generation (RAG) mimarisine benzer bir yaklaşımla geliştirilmiş, kullanıcıya anlık film önerileri sunan bir chatbot'tur. Temel amaç, kullanıcı girdiğine göre (örneğin: "Korku filmi öner", "Fantastik bir film izlemek isterim") The Movie Database (TMDB) API'sından alakalı veriyi çekmek ve bir web arayüzü üzerinden interaktif bir deneyim sunmaktır.

## 2. Veri Seti Hakkında Bilgi 

Bu projede harici bir veri seti kullanılmamış, bunun yerine **TMDB (The Movie Database) API**'si anlık veri kaynağı olarak kullanılmıştır.

* **Veri Kaynağı:** TMDB API.
* **Veri İçeriği:** Gerçek zamanlı olarak popüler filmler, tür bilgileri, özetler ve görsel bağlantıları.
* **Hazırlık Metodolojisi:** Veri, API üzerinden JSON formatında çekilmekte, Python (Requests kütüphanesi) ile işlenmekte ve kullanıcıya özel filtreler uygulanarak öneri sunulmaktadır.

## 3. Kullanılan Yöntemler ve Çözüm Mimarisi 

Proje, temel olarak bir RAG mimarisini taklit etmektedir:

1.  **Retrieval (Veri Çekme):** Kullanıcının isteği, TMDB API'sine sorgu (request) olarak gönderilir.
2.  **Augmentation (Zenginleştirme):** API'den dönen sonuçlar (film adları, özetler) alınır.
3.  **Generation (Yanıt Üretme):** Çekilen bu veriler, kullanıcıya öneri listesi olarak Streamlit arayüzünde gösterilir.

* **Teknolojiler:**
    * **Web Arayüzü & RAG Pipeline Framework:** `streamlit`
    * **Veri Çekme:** `requests`
    * **Veri Kaynağı:** TMDB API
* **Çözülen Problem:** Kullanıcının spesifik ve anlık film isteğine, büyük bir veritabanı (TMDB) üzerinden hızlı ve interaktif bir çözüm sunmak.

## 4. Elde Edilen Sonuçlar Özeti 

Geliştirilen chatbot:

* Kullanıcıdan gelen metin tabanlı isteklere anlık film önerileri sunabilmektedir.
* Önerilen filmleri kullanıcı arayüzünde bir liste olarak gösterir.
* **"İzledim" butonu** sayesinde kullanıcı deneyimini kişiselleştirir ve aynı filmi tekrar önermez (Session State kullanarak).
* Kolayca web’e dağıtılabilir (Streamlit Cloud).

## 5. Çalışma Kılavuzu (Lokal Kurulum) 

Aşağıdaki adımlar, projenin yerel bilgisayarınızda çalıştırılması için gereklidir:

1.  **Gereklilikler:** `requirements.txt` dosyasındaki kütüphanelerin kurulması gerekmektedir.
2.  **Sanal Ortam Kurulumu:**
    ```bash
    # Sanal ortam oluşturma ve etkinleştirme (Linux/macOS)
    python3 -m venv venv
    source venv/bin/activate 
    ```
    *(Windows için: `venv\Scripts\activate`)*
3.  **Bağımlılık Kurulumu:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **API Anahtarı Ayarı:** `config.py` dosyasını oluşturup TMDB API anahtarınızı içine ekleyin.
5.  **Çalıştırma:** Sanal ortam aktifken ana kodu çalıştırın.
    ```bash
    streamlit run film_oneri_web_tmdb.py
    ```
    Proje, tarayıcınızda otomatik olarak açılacaktır.

---
## 6. Web Arayüzü ve Product Kılavuzu (Deploy Linki) 

**DEPLOY LİNKİ (Canlı Uygulama):**

 https://film-oneri-chatbot-rag-bnhnh4dr2bvwzphgk5qcxg.streamlit.app/ 



### Test Etme Kılavuzu: 

1.  Yukarıdaki linki tıklayın.
2.  Arayüzdeki metin kutusuna bir istek yazın (Örn: **"En iyi bilim kurgu filmlerini öner"**).
3.  Chatbot size 3-5 adet film önerisi sunacaktır.
4.  Önerilen filmlerin altındaki **✅ İzledim** butonuna basın. Bu filmin artık size önerilmeyeceğini kontrol edin.
5.  Farklı bir sorgu yapın ve chatbot'un yeni filtrelere uygun öneri getirdiğini doğrulayın.
6.  Yeni bir sorgu yapıldığında eski sorgunuz silinmeyecektir, sayfanın en altına gittiğinizde yeni sorgunuzun da cevabını aynı sayfada görmeniz mümkündür.
7.  Sayfanın sonunda eğer izedime bastıysanız izlediğiniz filmler gözükür.


