import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(
    page_title="Sanrio Gacha v2.3 (Polished UI)",
    page_icon="🌸", # New Icon
    layout="centered"
)

# --- 角色数据 ---
CHARACTERS_DATA = [
    {"id": "hk", "name_cn": "凯蒂猫", "display_name_cn": "凯蒂猫 (经典偶像 Ver.)", "rarity": "SSR", "rarity_color": "#FFBF00",
     "image_id_cn": 1, "image_url_fallback": "https://img.sanrio.co.jp/characters/hellokitty/main_L.png",
     "celebration_toast": "💖超级明星登场！是凯蒂猫！💖", "flavor_text_cn": "用我的蝴蝶结，为你带来一整天的好心情！"},
    {"id": "km", "name_cn": "酷洛米", "display_name_cn": "酷洛米 (暗黑甜心 Ver.)", "rarity": "SSR", "rarity_color": "#FFBF00",
     "image_id_cn": 2, "image_url_fallback": "https://img.sanrio.co.jp/characters/kuromi/main_L.png",
     "celebration_toast": "🖤魅力无法挡！是酷洛米！🖤", "flavor_text_cn": "别看我有点小叛逆，我也是有可爱一面的哦！"},
    {"id": "mm", "name_cn": "美乐蒂", "display_name_cn": "美乐蒂 (温柔粉梦 Ver.)", "rarity": "SR", "rarity_color": "#E066FF",
     "image_id_cn": 3, "image_url_fallback": "https://img.sanrio.co.jp/characters/mymelody/main_L.png",
     "flavor_text_cn": "愿我的粉色头巾，为你编织最甜美的梦境~"},
    {"id": "cn", "name_cn": "大耳狗", "display_name_cn": "大耳狗 (天空乐园 Ver.)", "rarity": "SR", "rarity_color": "#E066FF",
     "image_id_cn": 4, "image_url_fallback": "https://img.sanrio.co.jp/characters/cinnamoroll/main_L.png",
     "flavor_text_cn": "和我一起扇动大耳朵，在云端自由自在地飞翔吧！"},
    {"id": "bm", "name_cn": "酷企鹅", "display_name_cn": "酷企鹅 (摇摆巨星 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 5, "image_url_fallback": "https://img.sanrio.co.jp/characters/badtzmaru/main_L.png",
     "flavor_text_cn": "哼！我就是这么有型，不服来战！"},
    {"id": "pp", "name_cn": "布丁狗", "display_name_cn": "布丁狗 (帽子戏法 Ver.)", "rarity": "SR", "rarity_color": "#E066FF",
     "image_id_cn": 6, "image_url_fallback": "https://img.sanrio.co.jp/characters/pompompurin/main_L.png",
     "flavor_text_cn": "圆滚滚的身体，最爱我的贝雷帽和美味布丁！"},
    {"id": "pc", "name_cn": "帕恰狗", "display_name_cn": "帕恰狗 (活力四射 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 7, "image_url_fallback": "https://img.sanrio.co.jp/characters/pochacco/main_L.png",
     "flavor_text_cn": "今天也要和好朋友一起，开心地去冒险！"},
    {"id": "ck", "name_cn": "可洛比", "display_name_cn": "可洛比 (温暖依偎 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 8, "image_url_fallback": "https://img.sanrio.co.jp/characters/corocorokuririn/main_L.png",
     "flavor_text_cn": "裹在柔软的毛毯里，感觉最安心啦~ (我是可洛比哦!)"},
    {"id": "gd", "name_cn": "蛋黄哥", "display_name_cn": "蛋黄哥 (懒洋洋日常 Ver.)", "rarity": "SR", "rarity_color": "#E066FF",
     "image_id_cn": 9, "image_url_fallback": "https://img.sanrio.co.jp/characters/gudetama/main_L.png",
     "flavor_text_cn": "啊……好麻烦……让我再瘫一会儿……"},
    {"id": "wm", "name_cn": "许愿兔", "display_name_cn": "许愿兔 (心愿传递 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 10, "image_url_fallback": "https://img.sanrio.co.jp/characters/wishmemell/main_L.png",
     "flavor_text_cn": "悄悄告诉我你的愿望，我会努力为你实现哦！"},
    {"id": "hg", "name_cn": "半鱼人", "display_name_cn": "半鱼人 (奇妙海洋 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 11, "image_url_fallback": "https://img.sanrio.co.jp/characters/hangyodon/main_L.png",
     "flavor_text_cn": "别看我样子有点怪，海洋里的故事我都知道！"},
    {"id": "lts","name_cn": "双子星", "display_name_cn": "双子星 (梦幻夜空 Ver.)", "rarity": "R", "rarity_color": "#79BAEC",
     "image_id_cn": 12, "image_url_fallback": "https://img.sanrio.co.jp/characters/littletwinstars/main_L.png",
     "flavor_text_cn": "Kiki和Lala在闪亮的星空中，向你眨眼睛~"},
]
TOTAL_CHARACTERS_COUNT = len(set(c['id'] for c in CHARACTERS_DATA))
WEIGHTS_MAP = {"SSR": 2.5, "SR": 5, "R": 12.5}
BASE_CHARACTER_WEIGHTS = [WEIGHTS_MAP[char["rarity"]] for char in CHARACTERS_DATA]
SUMMON_SPOT_IMAGE_URL = "https://www.transparentpng.com/thumb/hearts/hearts-love-png-image-yrNABP.png"
PITY_THRESHOLD_SSR = 7

# --- Session State 初始化 ---
if 'drawing_stage' not in st.session_state: st.session_state.drawing_stage = "idle"
if 'drawn_character' not in st.session_state: st.session_state.drawn_character = None
if 'session_collection' not in st.session_state: st.session_state.session_collection = []
if 'draw_count' not in st.session_state: st.session_state.draw_count = 0
if 'draw_count_since_sr_or_ssr' not in st.session_state: st.session_state.draw_count_since_sr_or_ssr = 0
if 'pity_sr_ssr_active' not in st.session_state: st.session_state.pity_sr_ssr_active = False
if 'first_draw_today_bonus_claimed' not in st.session_state: st.session_state.first_draw_today_bonus_claimed = False
if 'ten_pull_results_list' not in st.session_state: st.session_state.ten_pull_results_list = None
if 'is_ten_pull' not in st.session_state: st.session_state.is_ten_pull = False
if 'show_rarity_flash' not in st.session_state: st.session_state.show_rarity_flash = False
if 'flash_rarity_info' not in st.session_state: st.session_state.flash_rarity_info = None

# --- 辅助函数 ---
def get_character_image_url(character_data):
    if character_data.get("image_id_cn") is not None:
        return f"https://sanrio.com.cn/images/family/{character_data['image_id_cn']}/l1.png"
    elif character_data.get("image_url_fallback") and character_data["image_url_fallback"].startswith("http"):
        return character_data["image_url_fallback"]
    return "ERROR" # Special flag for cute error placeholder

def add_to_collection(character):
    if not any(c["id"] == character["id"] for c in st.session_state.session_collection):
        st.session_state.session_collection.append(character)
        st.session_state.session_collection.sort(key=lambda x: ({"SSR":0, "SR":1, "R":2}[x["rarity"]], x["name_cn"]))

def get_current_weights(force_sr_or_ssr=False):
    current_weights = list(BASE_CHARACTER_WEIGHTS)
    st.session_state.pity_sr_ssr_active = False

    if force_sr_or_ssr:
        sr_ssr_chars_data = [char for char in CHARACTERS_DATA if char["rarity"] in ["SR", "SSR"]]
        sr_ssr_weights_map = {char['id']: WEIGHTS_MAP[char["rarity"]] for char in sr_ssr_chars_data}
        forced_weights = [sr_ssr_weights_map.get(char['id'], 0) if char["rarity"] in ["SR", "SSR"] else 0 for char in CHARACTERS_DATA]
        if not any(w > 0 for w in forced_weights):
             return [1 if char['rarity'] in ["SR", "SSR"] else 0 for char in CHARACTERS_DATA]
        return forced_weights

    if st.session_state.draw_count_since_sr_or_ssr >= PITY_THRESHOLD_SSR:
        st.session_state.pity_sr_ssr_active = True
        for i, char_data in enumerate(CHARACTERS_DATA):
            if char_data["rarity"] == "SR": current_weights[i] *= 12
            elif char_data["rarity"] == "SSR": current_weights[i] *= 18
            elif char_data["rarity"] == "R": current_weights[i] /= 6
    return current_weights

# --- UI 样式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&display=swap');
    /* --- Global Styles --- */
    body {
        font-family: 'Mochiy Pop One', sans-serif !important;
        background: linear-gradient(180deg, #fff0f5 0%, #ffe6f0 100%) !important; /* Softer pink gradient for whole page */
    }
    /* Apply Mochiy Pop One more broadly */
    .stTextInput, .stTextArea, .stButton > button, .stSelectbox, 
    .stDateInput, .stTimeInput, .stNumberInput, .stFileUploader, 
    .stRadio > label > div:nth-child(2), .stCheckbox > label > div:nth-child(2),
    .stTabs [data-baseweb="tab-list"] button, .stTabs [data-baseweb="tab"],
    .stToast > div > div { /* Target toast text */
        font-family: 'Mochiy Pop One', sans-serif !important;
    }

    /* --- App Title Area --- */
    .app-title-container {
        background-color: #FFC0CB; padding: 25px 20px 30px 20px; border-radius: 30px;
        text-align: center; margin-bottom: 30px; 
        box-shadow: 0px 8px 25px rgba(255, 105, 180, 0.4);
        border: 2px solid white;
    }
    .app-title-container h1 {
        color: #FFFFFF; font-weight: bold; font-size: 42px !important; 
        text-shadow: 3px 3px 0px #FF69B4, 5px 5px 0px rgba(255,105,180,0.3);
        margin-bottom: 10px !important;
    }
    .app-title-container .hearts { 
        font-size: 32px; color: #FF69B4; margin-top: -5px; letter-spacing: 5px;
        animation: heartBeat 1.5s infinite ease-in-out;
    }
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); }
    }

    /* --- Tab Styling --- */
    .stTabs [data-baseweb="tab-list"] { /* Tab bar container */
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 20px !important;
        padding: 8px !important;
        box-shadow: 0 4px 12px rgba(255,105,180,0.25);
        margin-bottom: 30px !important;
        border: 1px solid rgba(255,192,203,0.5);
    }
    .stTabs [data-baseweb="tab-list"] button { /* Individual tab buttons */
        font-size: 17px !important;
        color: #FF69B4 !important; 
        border-radius: 15px !important;
        padding: 12px 22px !important;
        transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        transform: translateY(-2px);
        background-color: rgba(255,105,180,0.1) !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { /* Active tab button */
        background-color: #FF69B4 !important; 
        color: white !important; 
        box-shadow: 0 3px 10px rgba(199,21,133,0.5);
    }
    .stTabs [data-baseweb="tab-highlight"] { /* Hide default highlight line */
        background-color: transparent !important; 
    }

    /* --- Summon Area & Content --- */
    .summon-area {
        text-align: center; padding: 20px; border-radius: 25px;
        background: transparent; margin: 20px auto; min-height: 300px; /* Adjusted min-height */
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        border: 2px dashed #FFDAE9; position: relative; overflow: hidden;
    }
    .summon-spot-image { /* General class for summon heart image */
        width: 130px; height: 130px; 
        filter: drop-shadow(0 0 18px #FF69B4); 
        animation: pulseDeluxeEnhanced 2.5s infinite ease-in-out;
    }
    .summon-spot-image.idle-summon-spot { /* Larger, softer for idle state */
        width: 160px; height: 160px; opacity: 0.6; margin-bottom: 15px;
        filter: drop-shadow(0 0 25px #FFC0CB);
        animation: pulseDeluxeEnhanced 3.5s infinite ease-in-out; /* Slower pulse for idle */
    }
    @keyframes pulseDeluxeEnhanced {
        0%, 100% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 18px #FF69B4) brightness(1); }
        50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 28px #FF1493) brightness(1.3); }
    }
    .summon-spot-image.active-summon { animation: summonSpotActive 0.8s ease-in-out 1; }
    @keyframes summonSpotActive {
        0% { transform: scale(1) rotate(0deg); } 30% { transform: scale(1.3) rotate(10deg); }
        60% { transform: scale(0.9) rotate(-5deg); } 100% { transform: scale(1.1); }
    }
    
    /* Rarity Flash & SSR Background (mostly unchanged) */
    .rarity-flash-overlay { position: absolute; top:0; left:0; width:100%; height:100%; opacity: 0; z-index: 100; pointer-events: none; }
    .rarity-flash-overlay.active { animation: flashAnim 0.7s ease-out; }
    .rarity-flash-overlay.ssr { background: radial-gradient(ellipse at center, rgba(255,223,0,0.85) 0%, rgba(255,191,0,0.55) 70%, rgba(255,165,0,0) 100%); }
    .rarity-flash-overlay.sr { background: radial-gradient(ellipse at center, rgba(224,102,255,0.8) 0%, rgba(208,66,255,0.5) 70%, rgba(176,30,255,0) 100%); }
    .rarity-flash-overlay.r { background: radial-gradient(ellipse at center, rgba(121,186,236,0.7) 0%, rgba(100,160,220,0.4) 70%, rgba(80,140,200,0) 100%); }
    @keyframes flashAnim { 0% { opacity: 1; transform: scale(1.3); } 90% { opacity: 0.8; transform: scale(1.05); } 100% { opacity: 0; transform: scale(1); } }
    .ssr-background-flash { position: absolute; top:0; left:0; width:100%; height:100%; z-index: -1; background: radial-gradient(ellipse at center, rgba(255,223,186,0.9) 0%, rgba(255,165,0,0.7) 30%, rgba(255,105,180,0.5) 100%); animation: ssrFlashDeluxe 0.8s 2; }
    @keyframes ssrFlashDeluxe { 0%, 100% { opacity: 0; transform: scale(1.2); } 50% { opacity: 0.9; transform: scale(1); } }

    /* Character Text & Image Styling (mostly unchanged) */
    .rarity-text-reveal { font-size: 66px !important; font-weight: bold; text-shadow: 3px 3px 10px rgba(0,0,0,0.4); animation: fadeInScaleUpDeluxe 0.7s ease-out; }
    @keyframes fadeInScaleUpDeluxe { from { opacity:0; transform: scale(0.3) rotate(-15deg); } to { opacity:1; transform: scale(1) rotate(0deg); } }
    .rarity-text-reveal.ssr { font-size: 70px !important; animation: fadeInScaleUpDeluxe 0.7s ease-out, ssrShine 1.8s ease-in-out infinite alternate; }
    @keyframes ssrShine { 0% { text-shadow: 0 0 8px #FFF, 0 0 15px #FFF, 0 0 25px #FFD700, 0 0 35px #FFD700, 0 0 45px #FF8C00; } 100% { text-shadow: 0 0 12px #FFF, 0 0 22px #FFEDA0, 0 0 35px #FFD700, 0 0 45px #FFB84D, 0 0 55px #FFD700; } }
    .character-flavor-text { font-size: 17px !important; color: #C13C8A; margin-top: 15px; font-style: italic; max-width: 90%; line-height:1.5; text-shadow: 1px 1px 2px #FFECF5;}
    .character-name { text-align: center; margin-top: 12px; font-size: 30px !important; color: #D63384; font-weight: bold; text-shadow: 1px 1px 2px #FFECF5;}
    .congrats-text { text-align: center; color: #FF1493; font-size: 32px !important; font-weight: bold; margin-bottom: 20px; }
    .character-image { border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.25); background-color: rgba(255,255,255,0.7); padding: 10px; max-width: 240px; margin-top: 10px; margin-bottom: 10px; border: 3px solid #FFDAE9; }
    .character-image.ssr-reveal { animation: ssrImageAppear 1s ease-out 0.3s forwards; opacity: 0; }
    @keyframes ssrImageAppear { 0% { opacity: 0; transform: scale(0.4) rotate(-15deg) translateY(20px); } 60% { opacity: 1; transform: scale(1.15) rotate(5deg) translateY(0px); } 100% { opacity: 1; transform: scale(1) rotate(0deg) translateY(0px); } }

    /* --- Summon Buttons (already styled globally) --- */
    
    /* --- Pity Info Text (Summon Tab) --- */
    .pity-info-text { 
        text-align:center; font-size: 16px !important; color: #C13C8A; /* Darker pink */
        margin-top: 25px; padding: 12px 15px; 
        background-color: rgba(255, 228, 235, 0.85); /* Slightly more opaque */
        border-radius:15px; 
        border: 1px solid rgba(255,192,203,0.7);
        box-shadow: 0 2px 5px rgba(255,105,180,0.15);
    }

    /* --- Album Tab Styling --- */
    .collection-log-title { color: #FF1493; text-align: center; font-size: 28px !important; margin-top: 10px; margin-bottom: 20px; }
    .collection-item { 
        display: flex; flex-direction: column; align-items: center; justify-content: space-between; 
        margin: 10px; padding: 15px; 
        border: 2px solid #FFDAE9; border-radius: 20px; 
        text-align: center; background-color: #fff; 
        box-shadow: 0 5px 15px rgba(255,182,193,0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease; 
        min-height: 170px; /* Increased height slightly */
    }
    .collection-item:hover { 
        transform: translateY(-10px) scale(1.07); 
        box-shadow: 0 10px 20px rgba(255,105,180,0.6);
        border-color: #FFB6C1;
    }
    .collection-item img { 
        width: 80px; height: 80px; object-fit: contain; margin-bottom: 10px; 
        border-radius: 12px; background-color: #FFF5FA; padding: 5px;
    }
    .collection-item .char-name { font-size: 15px !important; color: #505050; margin-top: auto; line-height: 1.3; font-weight:600; padding-top: 5px;}
    .collection-item .char-rarity { font-size: 14px !important; font-weight: bold; }
    .image-placeholder-collection { /* Cute image placeholder */
        width: 80px; height: 80px; display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        background-color: #FFF5FA; border-radius: 12px;
        color: #FFB6C1; text-align:center; margin-bottom: 10px; padding:5px;
    }
    .image-placeholder-collection .image-placeholder-icon { font-size: 30px; }
    .image-placeholder-collection small { font-size: 10px; line-height: 1.2;}


    /* --- Multi-Pull Results (Summon Tab) --- */
    .multi-pull-results-container { width: 100%; max-height: 400px; overflow-y: auto; padding: 10px; margin-top:10px;}
    .multi-pull-results-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 12px; }
    .multi-pull-item {
        border: 2px solid #FFC0CB; border-radius: 12px; padding: 8px; text-align: center;
        background-color: rgba(255,255,255,0.9); box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        opacity: 0; transform: scale(0.8); animation: revealItem 0.5s ease-out forwards;
    }
    @keyframes revealItem { to { opacity: 1; transform: scale(1); } }
    .multi-pull-item:hover { transform: scale(1.07) !important; }
    .multi-pull-item img { width: 60px; height: 60px; object-fit: contain; margin-bottom: 4px; border-radius: 8px; background-color: #FFF9FB; padding:3px;}
    .multi-pull-item-name { font-size: 12px !important; font-weight: 600; color: #666; line-height:1.2; margin-bottom:2px; }
    .multi-pull-item-rarity { font-size: 11px !important; font-weight: bold; }
    .multi-pull-item.rarity-R { border-color: #A7D8F0; background-color: #F0F8FF; } /* AliceBlue */
    .multi-pull-item.rarity-SR { border: 3px solid #E066FF; box-shadow: 0 0 10px #E066FF, 0 0 5px #E066FF inset; background-color: #FAF0FF; } /* Lighter Lavender */
    .multi-pull-item.rarity-SSR { border: 3px solid #FFBF00; box-shadow: 0 0 12px #FFBF00, 0 0 6px #FFBF00 inset; background-color: #FFF8E1; animation: revealItem 0.5s ease-out forwards, pulseSSRItem 1.5s infinite alternate 0.5s; }
    @keyframes pulseSSRItem { from { box-shadow: 0 0 12px #FFBF00, 0 0 6px #FFBF00 inset; } to   { box-shadow: 0 0 20px #FFD700, 0 0 10px #FFD700 inset, 0 0 5px #FFF; } }
    .multi-results-title { font-size: 26px; color: #FF1493; font-weight: bold; margin-bottom: 18px; text-shadow: 1px 1px 2px #FFECF5;}

    /* --- Details Tab Styling --- */
    hr.tab-separator { border-top: 3px dotted #FFC0CB; margin-top: 30px; margin-bottom: 30px; }
    .details-content { 
        font-family: 'Mochiy Pop One', sans-serif; font-size:16px; color: #583c4a; /* Darker shade for readability */
        line-height: 1.8; background-color: rgba(255,255,255,0.7); padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255,192,203,0.5);
    }
    .details-content h2 { text-align:center; color: #FF69B4; margin-bottom:25px; font-size: 28px !important; }
    .details-content h3 { 
        color: #D63384; margin-top:20px; margin-bottom:10px; font-size:20px !important;
        border-bottom: 2px solid #FFDAE9; padding-bottom: 8px;
    }
    .details-content ul { list-style-type: "🎀 "; padding-left: 25px; margin-bottom: 15px;}
    .details-content li { margin-bottom: 10px; }
    .details-content strong { color: #C71585; } 
    .details-content em { color: #775965; } 
    .details-content p { margin-bottom:15px; }
    
    /* --- Footer --- */
    .footer-text { text-align:center; margin-top: 40px; margin-bottom: 25px; font-size:13px !important; color:#ad8594; }

</style>
""", unsafe_allow_html=True)

# --- 标题区域 ---
st.markdown("""
<div class="app-title-container">
    <h1>Sanrio Gacha Deluxe</h1>
    <div class="hearts">💖✨🌸✨💖</div>
</div>
""", unsafe_allow_html=True)

# --- Tabbed Layout ---
tab_summon, tab_album, tab_details = st.tabs([
    "💖 星愿召唤 (Summon)",
    "🎀 星愿相册 (Album)",
    "📜 星愿详情 (Details)"
])

# --- TAB 1: 星愿召唤 (Summon) ---
with tab_summon:
    summon_area_placeholder = st.empty()
    summon_buttons_placeholder = st.empty()
    pity_info_placeholder = st.empty()

    def display_summon_area_content():
        with summon_area_placeholder.container():
            st.markdown("<div class='summon-area'>", unsafe_allow_html=True)

            if st.session_state.show_rarity_flash and st.session_state.flash_rarity_info:
                rarity_short = st.session_state.flash_rarity_info["rarity_short"]
                st.markdown(f"<div class='rarity-flash-overlay active {rarity_short}'></div>", unsafe_allow_html=True)

            summon_spot_img_class = "summon-spot-image"
            if st.session_state.drawing_stage == "gathering_stars":
                summon_spot_img_class += " active-summon"
            elif st.session_state.drawing_stage in ["idle", "done", None]:
                 summon_spot_img_class += " idle-summon-spot"


            if st.session_state.drawing_stage == "gathering_stars":
                spinner_text = "💖 星光汇聚中...请稍候... 💖"
                if st.session_state.is_ten_pull: spinner_text = "💖✨ 十连星光加速汇聚！请期待！ ✨💖"
                elif st.session_state.pity_sr_ssr_active: spinner_text = "🌟✨ 感受到超强星愿能量！ ✨🌟"

                st.markdown(f"<img src='{SUMMON_SPOT_IMAGE_URL}' alt='Summoning Spot' class='{summon_spot_img_class}'>", unsafe_allow_html=True)
                with st.spinner(spinner_text):
                    if st.session_state.show_rarity_flash:
                         time.sleep(0.7)
                         st.session_state.show_rarity_flash = False
                    time.sleep(1.8 if st.session_state.is_ten_pull else 2.0)

                if st.session_state.is_ten_pull: st.session_state.drawing_stage = "multi_results_display"
                else: st.session_state.drawing_stage = "rarity_reveal"
                st.rerun()

            elif st.session_state.drawing_stage == "pre_rarity_flash":
                if not st.session_state.is_ten_pull and st.session_state.drawn_character:
                    char_rarity = st.session_state.drawn_character['rarity']
                    st.session_state.flash_rarity_info = {"rarity_short": char_rarity.lower(), "color": st.session_state.drawn_character['rarity_color']}
                    st.session_state.show_rarity_flash = True
                st.session_state.drawing_stage = "gathering_stars"
                st.rerun()

            elif st.session_state.drawing_stage == "rarity_reveal":
                character = st.session_state.drawn_character
                if character:
                    rarity_class = "ssr" if character['rarity'] == 'SSR' else ""
                    st.markdown(f"<p class='rarity-text-reveal {rarity_class}' style='color:{character['rarity_color']};'>{character['rarity']} !!!</p>", unsafe_allow_html=True)
                    if character['rarity'] == 'SSR':
                        st.markdown("<div class='ssr-background-flash'></div>", unsafe_allow_html=True)
                        time.sleep(1.8)
                    else: time.sleep(1.0)
                    st.session_state.drawing_stage = "character_reveal"; st.rerun()
                else: st.session_state.drawing_stage = "idle"; st.rerun()

            elif st.session_state.drawing_stage == "character_reveal":
                character = st.session_state.drawn_character
                if character:
                    st.markdown(f"<p class='congrats-text'>💖 伙伴现身！💖</p>", unsafe_allow_html=True)
                    current_char_image_url = get_character_image_url(character)
                    img_class = "character-image ssr-reveal" if character['rarity'] == 'SSR' else "character-image"
                    if current_char_image_url == "ERROR":
                        st.warning(f"图片寻觅失败！但你抽到了：{character['display_name_cn']} ({character['rarity']})")
                    else:
                        st.markdown(f"<div style='text-align:center;'><img src='{current_char_image_url}' class='{img_class}' alt='{character['display_name_cn']}'></div>", unsafe_allow_html=True)
                    st.markdown(f"<p class='character-name'>{character['display_name_cn']}</p>", unsafe_allow_html=True)
                    if character.get("flavor_text_cn"): st.markdown(f"<p class='character-flavor-text'>「 {character['flavor_text_cn']} 」</p>", unsafe_allow_html=True)
                    if character["rarity"] == "SSR":
                        st.balloons(); time.sleep(0.05); st.balloons()
                        if "celebration_toast" in character: st.toast(f"{character['celebration_toast']} {character['display_name_cn']}", icon="👑")
                    elif character["rarity"] == "SR":
                        st.balloons(); st.toast(f"恭喜获得SR伙伴：{character['display_name_cn']}！", icon="⭐")
                    else: st.toast(f"遇见了可爱的伙伴：{character['display_name_cn']}！", icon="💌")
                    st.session_state.drawing_stage = "done"
                else: st.session_state.drawing_stage = "idle"; st.rerun()

            elif st.session_state.drawing_stage == "multi_results_display":
                st.markdown("<p class='multi-results-title'>✨ 十连星愿结果 ✨</p>", unsafe_allow_html=True)
                st.markdown("<div class='multi-pull-results-container'><div class='multi-pull-results-grid'>", unsafe_allow_html=True)
                if st.session_state.ten_pull_results_list:
                    for idx, char_item_data in enumerate(st.session_state.ten_pull_results_list):
                        img_url_for_multi = get_character_image_url(char_item_data)
                        if img_url_for_multi == "ERROR":
                            img_html_multi = f"<div class='image-placeholder-collection' style='width:60px; height:60px; margin-bottom:4px;'><span class='image-placeholder-icon' style='font-size:24px;'>🍥</span><small style='font-size:9px;'>图坏<br>了呀</small></div>"
                        else:
                            img_html_multi = f"<img src='{img_url_for_multi}' alt='{char_item_data['name_cn']}'>"
                        item_rarity_class = f"rarity-{char_item_data['rarity']}"
                        anim_delay_style = f"animation-delay: {idx * 0.12}s;"
                        st.markdown(f"""
                        <div class='multi-pull-item {item_rarity_class}' style='{anim_delay_style}'>
                            {img_html_multi}
                            <p class='multi-pull-item-rarity' style='color:{char_item_data['rarity_color']};'>{char_item_data['rarity']}</p>
                            <p class='multi-pull-item-name'>{char_item_data['display_name_cn'].split(' (')[0]}</p>
                        </div>""", unsafe_allow_html=True)
                else: st.markdown("<p>没有获取到结果...</p>", unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)
                if st.session_state.ten_pull_results_list and any(c['rarity'] == 'SSR' for c in st.session_state.ten_pull_results_list):
                    st.balloons(); time.sleep(0.1); st.balloons()
                    ssr_names = [c['display_name_cn'] for c in st.session_state.ten_pull_results_list if c['rarity'] == 'SSR']
                    if ssr_names: st.toast(f"🎉 太棒了！十连中获得了闪耀巨星: {', '.join(ssr_names)}！ 🎉", icon="👑")
                st.session_state.drawing_stage = "done"; st.session_state.is_ten_pull = False

            elif st.session_state.drawing_stage in ["idle", "done", None]:
                st.markdown(f"<img src='{SUMMON_SPOT_IMAGE_URL}' alt='Summoning Spot' class='{summon_spot_img_class}'>", unsafe_allow_html=True)
                idle_message = "准备好邂逅你的三丽鸥伙伴了吗？"
                if not st.session_state.first_draw_today_bonus_claimed and st.session_state.draw_count == 0:
                    idle_message = "✨ 首次星愿有特别祝福哦！✨"
                st.markdown(f"<p style='font-size: 20px; color: #FF69B4; text-align:center; text-shadow: 1px 1px 2px #FFECF5;'>{idle_message}</p>", unsafe_allow_html=True)
                if st.session_state.draw_count > 0:
                    st.markdown(f"<p style='font-size: 15px; color: #FDA0C1; text-align:center; margin-top:10px;'>已进行 {st.session_state.draw_count} 次星愿召唤</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    display_summon_area_content()

    with summon_buttons_placeholder.container():
        if st.session_state.drawing_stage in ["idle", "done", None]:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💖✨ 许下星愿！ ✨💖", use_container_width=True, key="single_pull_btn"):
                    st.session_state.is_ten_pull = False; st.session_state.draw_count += 1
                    st.session_state.draw_count_since_sr_or_ssr += 1
                    actual_weights = get_current_weights()
                    drawn_character = random.choices(CHARACTERS_DATA, weights=actual_weights, k=1)[0]
                    st.session_state.drawn_character = drawn_character
                    add_to_collection(drawn_character)
                    if drawn_character["rarity"] in ["SR", "SSR"]:
                        st.session_state.draw_count_since_sr_or_ssr = 0; st.session_state.pity_sr_ssr_active = False
                    if not st.session_state.first_draw_today_bonus_claimed:
                        st.toast("今日首次星愿，好运加倍哦！💖", icon="🎉"); st.session_state.first_draw_today_bonus_claimed = True
                    st.session_state.drawing_stage = "pre_rarity_flash"; st.rerun()
            with col2:
                if st.button("🌟✨ 许下十连星愿！ ✨🌟", type="primary", use_container_width=True, key="ten_pull_btn"):
                    st.session_state.is_ten_pull = True; st.session_state.ten_pull_results_list = []
                    st.session_state.show_rarity_flash = False
                    sr_or_better_in_batch = False
                    for i in range(10):
                        st.session_state.draw_count += 1; st.session_state.draw_count_since_sr_or_ssr += 1
                        force_sr_ssr_for_this_pull = (i == 9 and not sr_or_better_in_batch)
                        current_pull_weights = get_current_weights(force_sr_or_ssr=force_sr_ssr_for_this_pull)
                        drawn_char_multi = random.choices(CHARACTERS_DATA, weights=current_pull_weights, k=1)[0]
                        st.session_state.ten_pull_results_list.append(drawn_char_multi)
                        add_to_collection(drawn_char_multi)
                        if drawn_char_multi["rarity"] in ["SR", "SSR"]:
                            sr_or_better_in_batch = True; st.session_state.draw_count_since_sr_or_ssr = 0
                            st.session_state.pity_sr_ssr_active = False
                    if not st.session_state.first_draw_today_bonus_claimed:
                        st.toast("今日首次星愿(十连)，好运加倍哦！💖", icon="🎉"); st.session_state.first_draw_today_bonus_claimed = True
                    st.session_state.drawing_stage = "gathering_stars"; st.rerun()

    with pity_info_placeholder.container():
        if st.session_state.drawing_stage in ["idle", "done", None]:
            pity_countdown_display = max(0, PITY_THRESHOLD_SSR - st.session_state.draw_count_since_sr_or_ssr)
            pity_message_html = ""
            if st.session_state.draw_count_since_sr_or_ssr >= PITY_THRESHOLD_SSR : pity_message_html = f"<b>✨星愿能量已满 ({st.session_state.draw_count_since_sr_or_ssr}/{PITY_THRESHOLD_SSR})！下次召唤SSR/SR伙伴几率大幅提升！✨</b>"
            elif pity_countdown_display == 0 : pity_message_html = f"<b>✨星愿能量即将爆发 ({st.session_state.draw_count_since_sr_or_ssr}/{PITY_THRESHOLD_SSR})！下次召唤SSR/SR伙伴几率将大幅提升！✨</b>"
            else: pity_message_html = f"下一次星愿能量爆发还需 <b>{pity_countdown_display}</b> 次召唤 ({st.session_state.draw_count_since_sr_or_ssr}/{PITY_THRESHOLD_SSR})"
            st.markdown(f"<div class='pity-info-text'>{pity_message_html}</div>", unsafe_allow_html=True)

# --- TAB 2: 星愿相册 (Album) ---
with tab_album:
    st.markdown(f"<p class='collection-log-title'>🎀 本次星愿相册 ({len(st.session_state.session_collection)}/{TOTAL_CHARACTERS_COUNT} 种) 🎀</p>", unsafe_allow_html=True)
    if not st.session_state.session_collection:
        st.markdown("<p style='text-align:center; color:grey; font-style:italic; margin-top:25px;'>你的星愿相册还是空的呢，快去召唤第一个伙伴吧！</p>", unsafe_allow_html=True)
    else:
        st.caption("（关闭页面或刷新后记录将清空哦～）")
        chars_per_row = 4
        rows = [st.session_state.session_collection[i:i + chars_per_row] for i in range(0, len(st.session_state.session_collection), chars_per_row)]
        for row_chars in rows:
            cols = st.columns(chars_per_row)
            for i, char_item_data in enumerate(row_chars):
                with cols[i]:
                    img_url_for_collection = get_character_image_url(char_item_data)
                    if img_url_for_collection == "ERROR":
                        img_html = f"<div class='image-placeholder-collection'><span class='image-placeholder-icon'>🍥</span><small>图片<br>加载中</small></div>"
                    else:
                        img_html = f"<img src='{img_url_for_collection}' alt='{char_item_data['name_cn']}'>"
                    collection_display_name = char_item_data['display_name_cn'].split(' (')[0]
                    st.markdown(f"""
                    <div class='collection-item'>
                        {img_html}
                        <div>
                            <p class='char-rarity' style='color:{char_item_data['rarity_color']};'>{char_item_data['rarity']}</p>
                            <p class='char-name' title='{char_item_data['display_name_cn']}'>{collection_display_name}</p>
                        </div>
                    </div>""", unsafe_allow_html=True)
    st.markdown("<hr class='tab-separator'>", unsafe_allow_html=True)

# --- TAB 3: 星愿详情 (Details) ---
with tab_details:
    st.markdown("<div class='details-content'>", unsafe_allow_html=True) # Apply container class
    st.markdown("<h2>✨ 星愿机制详解 ✨</h2>", unsafe_allow_html=True)
    total_base_weight = sum(BASE_CHARACTER_WEIGHTS)
    ssr_prob_display = sum(w for char, w in zip(CHARACTERS_DATA, BASE_CHARACTER_WEIGHTS) if char['rarity'] == 'SSR') / total_base_weight * 100
    sr_prob_display = sum(w for char, w in zip(CHARACTERS_DATA, BASE_CHARACTER_WEIGHTS) if char['rarity'] == 'SR') / total_base_weight * 100
    r_prob_display = sum(w for char, w in zip(CHARACTERS_DATA, BASE_CHARACTER_WEIGHTS) if char['rarity'] == 'R') / total_base_weight * 100
    details_md = f"""
        <h3>基础概率:</h3>
        <ul>
            <li><strong>SSR (闪耀巨星)</strong>: 基础约 {ssr_prob_display:.1f}%</li>
            <li><strong>SR (人气明星)</strong>: 基础约 {sr_prob_display:.1f}%</li>
            <li><strong>R (可爱伙伴)</strong>: 基础约 {r_prob_display:.1f}%</li>
        </ul>
        <h3>✨ 星愿能量 (SSR/SR伙伴保底机制)</h3>
        <p>当您连续 <strong>{PITY_THRESHOLD_SSR}</strong> 次未召唤到SR或更高级别的伙伴时，下一次进行“许下星愿”或“许下十连星愿”时，获得SR/SSR伙伴的几率将会<b>大幅提升</b>！</p>
        <p><em>当前星愿能量计数会在获得任一SR或SSR伙伴后重置。</em></p>
        <h3>🌟 十连星愿特别祝福</h3>
        <p>每次进行“许下十连星愿”，必定获得至少一位SR或更高级别的伙伴！这个祝福独立于星愿能量机制。</p>
        <h3>温馨提示:</h3>
        <p><em>每次星愿召唤都是独立的随机事件（上述能量机制与十连祝福除外）。祝您好运，邂逅心仪的三丽鸥伙伴！</em></p>
    """
    st.markdown(details_md, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # Close details-content
    st.markdown("<hr class='tab-separator'>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div class='footer-text'>© 2025 Sanrio Gacha v2.3 Polished UI. Images © Sanrio CO., LTD.</div>", unsafe_allow_html=True)