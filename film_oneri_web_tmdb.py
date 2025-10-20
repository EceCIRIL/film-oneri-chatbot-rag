# 🎬 Film Öneri Chatbot (v14.10 yorumlu)
# ---------------------------------------------------------------
# Bu sürüm:
# - Chatbot arayüzüyle yazışarak film önerir
# - Türkçe arayüz
# - Komedi filtresi düzeltildi
# - Önceden önerilen filmler tekrar gelmez
# - Arka plan renksiz
# - Bol yorum satırı ile açıklamalar eklendi

import streamlit as st  # Streamlit arayüzü için
import requests          # TMDB API çağrıları için
import time              # API çağrıları arasında bekleme için
import random            # Alternatif tür seçmek için

# ---------------------------------------------------------------
# 🔧 TMDB API AYARLARI
# ---------------------------------------------------------------
try:
    from config import TMDB_API_KEY  # config.py içinden anahtarı al
except ImportError:
    TMDB_API_KEY = None
    raise ValueError("⚠️ config.py dosyasında TMDB_API_KEY tanımlı değil!")

API_KEY = TMDB_API_KEY  # TMDB API anahtarı
BASE_URL = "https://api.themoviedb.org/3"  # TMDB temel URL
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"  # Poster görselleri için URL

# ---------------------------------------------------------------
# 🔑 Tür kelime -> TMDB ID eşlemesi
# ---------------------------------------------------------------
GENRE_KEYWORDS = {
    "romantik": 10749,
    "komedi": 35,
    "fantastik": 14,
    "aksiyon": 28,
    "dram": 18,
    "gerilim": 53,
    "bilim kurgu": 878,
    "animasyon": 16,
    "korku": 27,
    "suç": 80,
    "macera": 12
}

# Komedi overview anahtar kelimeleri (opsiyonel, öncelik için)
COMEDY_KEYWORDS = ["funny", "humor", "hilarious", "laugh", "comedy"]

# ---------------------------------------------------------------
# 🎨 SAYFA TASARIMI (Renksiz arka plan)
# ---------------------------------------------------------------
def add_page_style():
    """
    Streamlit sayfasının stilini ayarlar.
    - Arka plan renksiz
    - Başlık ve yazı renkleri
    - Input ve button tasarımı
    - Sohbet balonları tasarımı
    - Film kart tasarımı
    """
    st.markdown("""
    <style>
    .stApp { background: none; color: #222; font-family: 'Trebuchet MS', sans-serif; }
    h1,h2,h3 { color: #800000; }
    .stTextInput>div>div>input { color: #222 !important; background-color: #fff !important; }
    .stTextInput>div>div>input::placeholder { color: #888 !important; }
    .stButton>button { background-color: #FFD700; color: #111; border-radius: 10px; border: none; padding: 0.6rem 1rem; font-weight: bold; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #ffcc00; transform: scale(1.05); }
    .chat-bubble-user { background: #fff8dc; color: #111; padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 10px; max-width: 80%; align-self: flex-end; border: 1px solid #FFD700; }
    .chat-bubble-bot { background: #fffaf0; color: #111; padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 10px; max-width: 80%; align-self: flex-start; border: 1px solid #800000; }
    .movie-card { background: #fff; border: 1px solid #FFD700; border-radius: 12px; padding: 1rem; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin-top: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------
# 🔍 TMDB API'DEN FİLM GETİRME
# ---------------------------------------------------------------
def tmdb_get(endpoint, params=None):
    """
    TMDB API'den JSON verisi döndürür.
    - endpoint: API uç noktası
    - params: parametreler dict olarak
    """
    if params is None:
        params = {}
    params["api_key"] = API_KEY
    response = requests.get(BASE_URL + endpoint, params=params, timeout=10)
    response.raise_for_status()  # Hata varsa exception fırlat
    return response.json()

def fetch_movies_by_genre(genre_id, count=5, exclude_ids=[]):
    """
    Belirli türde popüler filmleri getirir ve önceden gösterilenleri atlar.
    - genre_id: TMDB tür ID
    - count: döndürülecek film sayısı
    - exclude_ids: daha önce gösterilen film ID'leri
    """
    movies = []
    page = 1
    while len(movies) < count and page <= 3:
        params = {
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "language": "en-US",
            "page": page
        }
        data = tmdb_get("/discover/movie", params)
        results = data.get("results", [])
        for r in results:
            if not r.get("poster_path") or r["id"] in exclude_ids:
                continue

            # Komedi için ana tür kontrolü
            if genre_id == 35:
                # Eğer ana tür 35 değilse atla
                if r.get("genre_ids", [])[0] != 35:
                    continue

            movies.append({
                "id": r["id"],
                "title": r.get("title", "Bilinmeyen Başlık"),
                "overview": r.get("overview", "Açıklama mevcut değil."),
                "poster": IMAGE_BASE + r["poster_path"],
                "rating": r.get("vote_average", 0),
                "year": r.get("release_date", "-")[:4]
            })
            if len(movies) >= count:
                break
        page += 1
        time.sleep(0.1)  # API limitleri için küçük bekleme
    return movies

# ---------------------------------------------------------------
# 💬 CHATBOT MANTIĞI
# ---------------------------------------------------------------
def chatbot_reply(user_text, exclude_ids=[]):
    """
    Kullanıcının yazısına göre film önerir.
    - user_text: kullanıcı mesajı
    - exclude_ids: daha önce gösterilen film ID'leri
    """
    text = user_text.lower()
    selected_genre = None
    for k in GENRE_KEYWORDS:
        if k in text:
            selected_genre = k
            break
    if not selected_genre:
        return ("Türü anlayamadım 😕 Örneğin: 'komedi filmi öner', 'korku filmi istiyorum' gibi yazabilirsin.", None)

    genre_id = GENRE_KEYWORDS[selected_genre]
    movies = fetch_movies_by_genre(genre_id, exclude_ids=exclude_ids)

    # Eğer hiçbir film bulunmazsa rastgele alternatif tür göster
    if not movies:
        alt_genre = random.choice(list(GENRE_KEYWORDS.keys()))
        alt_id = GENRE_KEYWORDS[alt_genre]
        movies = fetch_movies_by_genre(alt_id, exclude_ids=exclude_ids)
        return (f"'{selected_genre}' türünde uygun film bulamadım 😢 Ama {alt_genre} türünde birkaç önerim var:", movies)

    return (f"İşte sana bazı {selected_genre} film önerilerim 🎬", movies)

# ---------------------------------------------------------------
# 🚀 UYGULAMA
# ---------------------------------------------------------------
def main():
    st.set_page_config(page_title="🎬 Film Öneri Chatbot", page_icon="🎥", layout="centered")
    add_page_style()
    st.title("🎥 Film Öneri Chatbot")
    st.write("🍿 Chatbot’a yaz, türü anlayıp sana uygun filmler önersin.")
    st.write("Örneğin: *'komedi filmi öner'*, *'romantik film izlemek istiyorum'*...")

    # Session state başlat
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "watched_list" not in st.session_state:
        st.session_state["watched_list"] = []

    # Önceden gösterilen film ID'lerini listele
    exclude_ids = [m["id"] for m in st.session_state.get("watched_list",[])]
    for _, _, movies in st.session_state.get("chat_history", []):
        if movies:
            for m in movies:
                exclude_ids.append(m["id"])

    # Kullanıcıdan mesaj al
    user_text = st.text_input("💬 Mesajını yaz:", key="user_input")
    if user_text:
        st.session_state["chat_history"].append(("user", user_text, None))
        bot_reply, movies = chatbot_reply(user_text, exclude_ids=exclude_ids)
        st.session_state["chat_history"].append(("bot", bot_reply, movies))

    # Sohbet balonlarını göster
    for sender, msg, movies in st.session_state["chat_history"]:
        if sender == "user":
            st.markdown(f"<div class='chat-bubble-user'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-bot'>{msg}</div>", unsafe_allow_html=True)
            if movies:
                for m in movies:
                    st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                    st.image(m["poster"], width=180)
                    st.markdown(f"### {m['title']} ({m['year']})")
                    st.write(f"⭐ {m['rating']}")
                    st.write(m["overview"])
                    if st.button(f"✅ İzledim: {m['title']}"):
                        if m not in st.session_state["watched_list"]:
                            st.session_state["watched_list"].append(m)
                    st.markdown("</div>", unsafe_allow_html=True)

    # İzlenen filmleri göster
    st.subheader("📜 İzlediğim Filmler")
    if not st.session_state["watched_list"]:
        st.info("Henüz film izlemedin 🍿")
    else:
        for m in st.session_state["watched_list"]:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
            st.markdown(f"### {m['title']} ({m['year']})")
            st.write(f"⭐ {m['rating']}")
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()



#python -m streamlit run film_oneri_web_tmdb.py ÇALIŞTIRMAK İÇİN