import base64
from datetime import date
from html import escape
from urllib.parse import quote_plus
import joblib
import pandas as pd
import streamlit as st


# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="AI Travel Recommender",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Load Model
# =========================================================
@st.cache_resource
def load_model_files():
    model = joblib.load("travel_country_model.pkl")
    label_enc = joblib.load("label_encoder.pkl")
    model_columns = joblib.load("model_columns.pkl")
    return model, label_enc, model_columns


try:
    model, label_enc, model_columns = load_model_files()
except Exception as e:
    st.error("The model files could not be loaded.")
    st.exception(e)
    st.stop()


# =========================================================
# Background Video
# =========================================================
def add_video_background(video_file):
    try:
        with open(video_file, "rb") as video:
            encoded_video = base64.b64encode(video.read()).decode()

        st.markdown(
            f"""
            <video autoplay muted loop playsinline id="bg-video">
                <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        pass


# =========================================================
# Global CSS
# =========================================================
def app_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --paper: #fcfcfb;
            --paper-strong: #ffffff;
            --ink: #0f3d3e;
            --muted: #6b7b8c;
            --teal: #2c9a8a;
            --teal-dark: #168b82;
            --coral: #f19783;
            --amber: #f8c76f;
            --sky: #a3d3e4;
            --mint: #e7fbf4;
            --line: rgba(72, 90, 107, 0.12);
            --glass: rgba(255, 255, 255, 0.84);
            --glass-strong: rgba(255, 255, 255, 0.96);
            --shadow: 0 24px 70px rgba(71, 88, 106, 0.12);
            --shadow-soft: 0 16px 38px rgba(71, 88, 106, 0.07);
        }

        * {
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0 !important;
        }

        .stApp,
        [data-testid="stAppViewContainer"] {
            background:
                linear-gradient(120deg, rgba(15, 118, 110, 0.18), rgba(124, 198, 216, 0.10) 42%, rgba(239, 111, 97, 0.13)),
                repeating-linear-gradient(90deg, rgba(23, 33, 43, 0.035) 0 1px, transparent 1px 58px),
                linear-gradient(180deg, #fffdfa 0%, #f6efe3 100%) !important;
            color: var(--ink) !important;
        }

        #bg-video {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -2;
            opacity: 0.18;
            filter: saturate(1.12) contrast(1.04);
            pointer-events: none;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background:
                linear-gradient(135deg, rgba(255,253,250,0.86), rgba(251,248,242,0.64) 48%, rgba(223,247,239,0.72)),
                linear-gradient(180deg, rgba(255,253,250,0.55), rgba(255,253,250,0.86));
            z-index: -1;
            pointer-events: none;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        .main,
        section.main,
        .block-container {
            position: relative;
            z-index: 1;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3.5rem;
        }

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(22px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes shine {
            from {
                background-position: 0% 50%;
            }
            to {
                background-position: 100% 50%;
            }
        }

        h1, h2, h3 {
            color: var(--ink) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 900 !important;
        }

        p, label, span, div {
            color: var(--ink);
        }

        .travel-brand {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 9px 14px;
            border: 1px solid rgba(15, 118, 110, 0.22);
            border-radius: 999px;
            background: rgba(255, 253, 250, 0.72);
            color: var(--teal-dark);
            font-size: 13px;
            font-weight: 900;
            text-transform: uppercase;
            box-shadow: var(--shadow-soft);
        }

        .travel-brand::before {
            content: "";
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: linear-gradient(135deg, var(--teal), var(--coral));
            box-shadow: 0 0 0 5px rgba(15, 118, 110, 0.10);
        }

        .step-kicker {
            color: var(--teal-dark);
            font-size: 13px;
            font-weight: 900;
            text-transform: uppercase;
        }

        .step-title {
            margin: 10px 0 6px;
            color: var(--ink);
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 34px;
            line-height: 1.05;
            font-weight: 900;
        }

        .step-copy {
            margin: 0 0 18px;
            color: var(--muted);
            font-size: 16px;
            font-weight: 650;
        }

        .st-key-home_box {
            text-align: center;
            min-height: 58vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 28px;
            animation: fadeUp 0.9s ease both;
        }

        .st-key-home_box h1 {
            max-width: 900px;
            font-size: 84px !important;
            line-height: 0.9 !important;
            margin: 22px auto 0.75rem !important;
        }

        .st-key-home_box p {
            max-width: 690px;
            font-size: 22px !important;
            line-height: 1.45 !important;
            font-weight: 750 !important;
            color: var(--muted) !important;
        }

        .hero-stat-row {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 22px;
        }

        .hero-stat {
            min-width: 150px;
            padding: 14px 18px;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(255, 253, 250, 0.70);
            box-shadow: var(--shadow-soft);
            backdrop-filter: blur(16px);
        }

        .hero-stat strong {
            display: block;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 22px;
            line-height: 1;
        }

        .hero-stat span {
            color: var(--muted);
            font-size: 12px;
            font-weight: 850;
            text-transform: uppercase;
        }

        .st-key-home_button_box {
            display: flex;
            justify-content: center;
            margin-top: -58px;
            animation: fadeUp 1.1s ease both;
        }

        div[data-testid="stFormSubmitButton"] button,
        .st-key-home_button_box button,
        .st-key-start_over_box button {
            border-radius: 999px !important;
            border: 1px solid rgba(23, 33, 43, 0.16) !important;
            background: linear-gradient(135deg, var(--teal), #168b82, var(--coral)) !important;
            background-size: 180% 180% !important;
            color: var(--paper-strong) !important;
            font-weight: 900 !important;
            transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease, background 0.22s ease !important;
            box-shadow: 0 16px 34px rgba(15, 118, 110, 0.22);
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        .st-key-home_button_box button:hover,
        .st-key-start_over_box button:hover {
            background: linear-gradient(135deg, var(--coral), var(--teal), var(--teal-dark)) !important;
            color: white !important;
            filter: brightness(1.03) saturate(1.08);
            transform: translateY(-3px);
            box-shadow: 0 22px 48px rgba(15, 118, 110, 0.28);
            animation: shine 1.2s ease both;
        }

        .st-key-home_button_box button {
            width: 320px !important;
            height: 72px !important;
            font-size: 21px !important;
        }

        .st-key-home_button_box button p,
        div[data-testid="stFormSubmitButton"] button p {
            color: inherit !important;
            font-weight: 900 !important;
        }

        .st-key-wide_form_card div[data-testid="stForm"] {
            background: var(--glass) !important;
            border: 1px solid var(--line) !important;
            border-radius: 28px !important;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: var(--shadow);
            animation: fadeUp 0.62s ease both;
            width: min(980px, 96vw);
            margin: 48px auto 0 auto;
            padding: 34px 38px 38px 38px;
        }

        label p {
            color: var(--ink) !important;
            font-size: 22px !important;
            line-height: 1.2 !important;
            font-weight: 900 !important;
            margin-bottom: 0.35rem !important;
        }

        input,
        div[data-baseweb="input"] input {
            background: rgba(255, 253, 250, 0.94) !important;
            color: var(--ink) !important;
            border: 1.5px solid rgba(23, 33, 43, 0.16) !important;
            border-radius: 18px !important;
            min-height: 52px !important;
            font-size: 17px !important;
            font-weight: 750 !important;
            box-shadow: 0 10px 24px rgba(23, 33, 43, 0.06);
        }

        input:focus {
            border-color: var(--teal) !important;
            box-shadow: 0 0 0 4px rgba(44, 154, 138, 0.18), 0 14px 28px rgba(71, 88, 106, 0.08) !important;
        }

        div[data-testid="stFormSubmitButton"] button {
            margin-top: 32px !important;
            height: 60px !important;
            font-size: 18px !important;
        }

        div[role="radiogroup"] {
            margin-top: 24px !important;
            gap: 12px !important;
        }

        div[role="radiogroup"] label {
            min-width: 74px;
            justify-content: center;
            background: rgba(255, 253, 250, 0.78) !important;
            border: 1px solid var(--line) !important;
            border-radius: 18px !important;
            padding: 12px 16px !important;
            box-shadow: 0 10px 22px rgba(23, 33, 43, 0.07);
            transition: all 0.22s ease !important;
        }

        div[role="radiogroup"] label:hover {
            background: var(--mint) !important;
            border-color: rgba(15, 118, 110, 0.35) !important;
            transform: translateY(-3px);
        }

        input[type="radio"] {
            accent-color: var(--teal);
            transform: scale(1.25);
        }

        div[role="radiogroup"] label p {
            font-size: 17px !important;
            font-weight: 900 !important;
            color: var(--ink) !important;
        }

        div[data-baseweb="slider"] {
            margin-top: 42px !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
        }

        div[data-baseweb="slider"] p {
            color: var(--ink) !important;
            font-size: 18px !important;
            font-weight: 900 !important;
        }

        .st-key-wide_form_card button {
            background: rgba(255, 253, 250, 0.86) !important;
            color: var(--ink) !important;
            border: 1px solid var(--line) !important;
            border-radius: 999px !important;
            margin: 5px !important;
            padding: 8px 15px !important;
            box-shadow: 0 8px 18px rgba(23, 33, 43, 0.07);
            transition: all 0.22s ease !important;
        }

        .st-key-wide_form_card button:hover {
            background: var(--mint) !important;
            color: var(--teal-dark) !important;
            border-color: rgba(15, 118, 110, 0.45) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 14px 28px rgba(15, 118, 110, 0.16) !important;
        }

        .st-key-wide_form_card button p {
            color: inherit !important;
            font-weight: 900 !important;
            font-size: 15px !important;
        }


        .st-key-activity_pills button,
        div[data-testid="stPills"] button,
        div[data-testid="stBaseButton-pills"],
        button[data-testid="stBaseButton-pills"],
        div[data-testid="stBaseButton-pillsActive"],
        button[data-testid="stBaseButton-pillsActive"] {
            background: rgba(255, 253, 250, 0.92) !important;
            color: var(--ink) !important;
            border: 1px solid var(--line) !important;
            border-radius: 999px !important;
            box-shadow: 0 8px 18px rgba(23, 33, 43, 0.07) !important;
            transition: all 0.22s ease !important;
        }

        .st-key-activity_pills button *,
        div[data-testid="stPills"] button *,
        div[data-testid="stBaseButton-pills"] *,
        button[data-testid="stBaseButton-pills"] *,
        div[data-testid="stBaseButton-pillsActive"] *,
        button[data-testid="stBaseButton-pillsActive"] * {
            color: inherit !important;
        }

        .st-key-activity_pills button:hover,
        div[data-testid="stPills"] button:hover,
        div[data-testid="stBaseButton-pills"]:hover,
        button[data-testid="stBaseButton-pills"]:hover {
            background: var(--mint) !important;
            color: var(--teal-dark) !important;
            border-color: rgba(15, 118, 110, 0.45) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 14px 28px rgba(15, 118, 110, 0.16) !important;
        }

        .st-key-activity_pills button:hover *,
        div[data-testid="stPills"] button:hover *,
        div[data-testid="stBaseButton-pills"]:hover *,
        button[data-testid="stBaseButton-pills"]:hover * {
            color: var(--teal-dark) !important;
        }

        .st-key-activity_pills button[aria-pressed="true"],
        .st-key-activity_pills button[aria-selected="true"],
        .st-key-activity_pills button[aria-checked="true"],
        .st-key-activity_pills button[data-selected="true"],
        div[data-testid="stPills"] button[aria-pressed="true"],
        div[data-testid="stPills"] button[aria-selected="true"],
        div[data-testid="stPills"] button[aria-checked="true"],
        div[data-testid="stPills"] button[data-selected="true"],
        div[data-testid="stBaseButton-pillsActive"],
        div[data-testid="stBaseButton-pillsActive"] button,
        button[data-testid="stBaseButton-pillsActive"] {
            background: linear-gradient(135deg, var(--teal), var(--coral)) !important;
            color: white !important;
            border-color: rgba(23, 33, 43, 0.18) !important;
            box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.14),
                        0 14px 30px rgba(23, 33, 43, 0.14) !important;
        }

        .st-key-activity_pills button[aria-pressed="true"] *,
        .st-key-activity_pills button[aria-selected="true"] *,
        .st-key-activity_pills button[aria-checked="true"] *,
        .st-key-activity_pills button[data-selected="true"] *,
        div[data-testid="stPills"] button[aria-pressed="true"] *,
        div[data-testid="stPills"] button[aria-selected="true"] *,
        div[data-testid="stPills"] button[aria-checked="true"] *,
        div[data-testid="stPills"] button[data-selected="true"] *,
        div[data-testid="stBaseButton-pillsActive"] *,
        div[data-testid="stBaseButton-pillsActive"] button *,
        button[data-testid="stBaseButton-pillsActive"] * {
            color: white !important;
        }

        .st-key-dashboard_box {
            animation: fadeUp 0.7s ease both;
        }

        .st-key-dashboard_box h1 {
            font-size: 52px !important;
            margin-bottom: 0 !important;
        }

        .match-hero {
            margin: 18px 0 22px;
            padding: 26px;
            border: 1px solid var(--line);
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(15, 118, 110, 0.13), rgba(124, 198, 216, 0.12) 45%, rgba(239, 111, 97, 0.13)),
                rgba(255, 253, 250, 0.76);
            box-shadow: var(--shadow);
            backdrop-filter: blur(22px);
        }

        .match-hero small {
            color: var(--teal-dark);
            font-size: 13px;
            font-weight: 900;
            text-transform: uppercase;
        }

        .match-hero h2 {
            margin: 8px 0 6px;
            font-size: 44px;
            line-height: 1;
        }

        .match-hero p {
            margin: 0;
            color: var(--muted);
            font-size: 16px;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: var(--glass-strong) !important;
            border: 1px solid var(--line) !important;
            border-radius: 22px !important;
            padding: 20px 22px !important;
            box-shadow: var(--shadow-soft);
        }

        div[data-testid="stMetric"] * {
            color: var(--ink) !important;
            font-weight: 900 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(255, 253, 250, 0.72);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 6px;
        }

        .stTabs button,
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border: 0 !important;
            border-radius: 14px !important;
            box-shadow: none !important;
            color: var(--muted) !important;
            font-weight: 900 !important;
            padding: 10px 16px !important;
        }

        .stTabs button:hover {
            background: var(--mint) !important;
            color: var(--ink) !important;
            transform: none !important;
        }

        .stTabs [aria-selected="true"],
        .stTabs [aria-selected="true"] p {
            background: var(--teal) !important;
            color: var(--paper-strong) !important;
        }

        .match-list {
            display: grid;
            gap: 14px;
            margin-top: 12px;
        }

        .match-card {
            padding: 16px 18px;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(255, 253, 250, 0.86);
            box-shadow: var(--shadow-soft);
        }

        .match-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            margin-bottom: 10px;
        }

        .match-country {
            display: flex;
            align-items: center;
            gap: 11px;
            min-width: 0;
            font-size: 18px;
            font-weight: 900;
        }

        .match-rank {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            flex: 0 0 34px;
            border-radius: 999px;
            background: var(--ink);
            color: var(--paper-strong);
            font-size: 14px;
            font-weight: 900;
        }

        .match-score {
            color: var(--teal-dark);
            font-size: 20px;
            font-weight: 900;
            white-space: nowrap;
        }

        .profile-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin-top: 12px;
        }

        .profile-card {
            position: relative;
            overflow: hidden;
            min-height: 94px;
            padding: 16px 18px;
            border: 1px solid var(--line);
            border-radius: 20px;
            background:
                linear-gradient(135deg, rgba(255, 253, 250, 0.92), rgba(223, 247, 239, 0.78)),
                rgba(255, 253, 250, 0.88);
            box-shadow: var(--shadow-soft);
            animation: fadeUp 0.55s ease both;
        }

        .profile-label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 900;
            text-transform: uppercase;
        }

        .profile-value {
            margin-top: 8px;
            color: var(--ink);
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 24px;
            line-height: 1.12;
            font-weight: 900;
            overflow-wrap: anywhere;
        }

        .profile-card-wide {
            grid-column: 1 / -1;
        }

        .profile-card-wide .profile-value {
            font-family: 'Inter', sans-serif !important;
            font-size: 17px;
            line-height: 1.5;
        }

        .activity-card {
            padding: 8px;
            border-radius: 20px;
            background: rgba(255, 253, 250, 0.92);
            border: 1px solid var(--line);
            box-shadow: var(--shadow-soft);
            transition: all 0.22s ease;
            overflow: hidden;
            margin-bottom: 18px;
        }

        .activity-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 46px rgba(23, 33, 43, 0.14);
            border-color: rgba(15, 118, 110, 0.30);
        }

        .activity-card img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-radius: 18px;
            display: block;
        }

        .activity-card-title {
            margin-top: 12px;
            font-weight: 900;
            color: var(--ink);
            text-align: center;
            font-size: 18px;
        }

        .site-city {
            text-align: center;
            font-weight: 900;
            color: var(--teal-dark);
            margin: 6px 0;
            font-size: 14px;
        }

        .site-description {
            text-align: center;
            color: var(--muted);
            font-weight: 650;
            padding: 0 10px 10px;
            font-size: 14px;
            line-height: 1.45;
        }

        div[data-testid="stAlert"] {
            border-radius: 18px !important;
            border: 1px solid rgba(23, 33, 43, 0.12) !important;
        }

        div[data-testid="stProgress"] > div {
            background: rgba(23, 33, 43, 0.10) !important;
            border-radius: 999px !important;
        }

        div[data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, var(--teal), var(--sky), var(--coral), var(--amber)) !important;
            border-radius: 999px !important;
        }

        .st-key-start_over_box button {
            margin-top: 20px !important;
            height: 54px !important;
            padding-left: 28px !important;
            padding-right: 28px !important;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1rem;
            }

            .st-key-home_box h1 {
                font-size: 52px !important;
            }

            .st-key-home_box p {
                font-size: 18px !important;
            }

            .st-key-home_button_box {
                margin-top: -20px;
            }

            .st-key-home_button_box button {
                width: 92vw !important;
            }

            .st-key-wide_form_card div[data-testid="stForm"] {
                width: 94vw !important;
                margin-top: 36px !important;
                padding: 26px !important;
            }

            .step-title {
                font-size: 28px;
            }

            div[role="radiogroup"] {
                align-items: stretch !important;
            }

            .match-hero h2 {
                font-size: 34px;
            }

            .profile-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Run background and style
add_video_background("video1.mp4")
app_style()


# =========================================================
# Session State
# =========================================================
if "step" not in st.session_state:
    st.session_state.step = "home"


# =========================================================
# Options
# =========================================================
activities_options = [
    "adventure",
    "anime",
    "beaches",
    "city",
    "culture",
    "desert",
    "eco-tourism",
    "family",
    "food",
    "football",
    "hiking",
    "history",
    "honeymoon",
    "islands",
    "landscapes",
    "luxury",
    "mountains",
    "museums",
    "nature",
    "nightlife",
    "northern lights",
    "relaxation",
    "road trips",
    "romance",
    "safari",
    "shopping",
    "skiing",
    "snorkeling",
    "temples",
    "waterfalls",
    "wildlife",
]

STEP_DETAILS = {
    1: ("Your name", "Give the trip a personal starting point."),
    2: ("Date of birth", "We use your age to tune the travel match."),
    3: ("Safety comfort", "Tell the model how much calm and security matter."),
    4: ("Food priority", "Some trips are built around the next great meal."),
    5: ("Nightlife energy", "Choose whether evenings should be quiet or electric."),
    6: ("Nature pull", "Rate how strongly landscapes and fresh air call you."),
    7: ("Family fit", "Set how family-friendly the destination should feel."),
    8: ("Budget range", "Pick the spending style that feels right."),
    9: ("Weather mood", "Choose the climate you would actually enjoy."),
    10: ("Trip personality", "Select the activities that make the journey yours."),
}


def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def oldest_allowed_birthdate(minimum_age=7):
    today = date.today()
    try:
        return today.replace(year=today.year - minimum_age)
    except ValueError:
        return today.replace(year=today.year - minimum_age, day=28)


def go_to(step):
    st.session_state.step = step
    st.rerun()


def render_brand():
    st.markdown(
        '<div class="travel-brand">AI Travel Recommender</div>',
        unsafe_allow_html=True,
    )


def render_step_intro(step_number, total_steps=10):
    title, copy = STEP_DETAILS[step_number]
    st.markdown(
        f"""
        <div class="step-kicker">Step {step_number} of {total_steps}</div>
        <div class="step-title">{title}</div>
        <p class="step-copy">{copy}</p>
        """,
        unsafe_allow_html=True,
    )
    st.progress(step_number / total_steps)


def rating_label(value):
    labels = {
        1: "1 - Low",
        2: "2 - Mild",
        3: "3 - Balanced",
        4: "4 - Strong",
        5: "5 - Essential",
    }
    return labels[int(value)]


def make_user_dataframe(
    name,
    birth_date,
    age_value,
    safety_value,
    food_value,
    nightlife_value,
    nature_value,
    family_value,
    budget_value,
    weather_value,
    activities_value,
):
    return pd.DataFrame(
        {
            "Category": [
                "Name",
                "Date of Birth",
                "Age",
                "Safety",
                "Food",
                "Nightlife",
                "Nature",
                "Family Friendly",
                "Budget",
                "Weather",
                "Activities",
            ],
            "Selection": [
                name,
                birth_date,
                age_value,
                f"{safety_value}/5",
                f"{food_value}/5",
                f"{nightlife_value}/5",
                f"{nature_value}/5",
                f"{family_value}/5",
                budget_value,
                weather_value,
                ", ".join(activities_value),
            ],
        }
    )


def get_recommendations(user_data):
    user_df = pd.DataFrame([user_data])
    user_df_encoded = pd.get_dummies(user_df)

    for col in model_columns:
        if col not in user_df_encoded.columns:
            user_df_encoded[col] = 0

    user_df_encoded = user_df_encoded[model_columns]
    prediction_probs = model.predict_proba(user_df_encoded)

    top_5_indexes = prediction_probs[0].argsort()[-5:][::-1]
    top_5_countries = label_enc.inverse_transform(top_5_indexes)
    top_5_scores = prediction_probs[0][top_5_indexes]

    return pd.DataFrame(
        {
            "Rank": [1, 2, 3, 4, 5],
            "Country": top_5_countries,
            "Match %": [round(score * 100, 1) for score in top_5_scores],
        }
    )


def render_match_cards(recommendations_df):
    cards = ""

    for _, row in recommendations_df.iterrows():
        rank = int(row["Rank"])
        country = escape(str(row["Country"]))
        score = escape(str(row["Match %"]))

        cards += f"""
<div class="match-card">
    <div class="match-card-top">
        <div class="match-country">
            <span class="match-rank">{rank}</span>
            <span>{country}</span>
        </div>
        <div class="match-score">{score}%</div>
    </div>
</div>
"""

    st.markdown(
        f"""
<div class="match-list">
{cards}
</div>
""",
        unsafe_allow_html=True,
    )

def render_profile_cards(user_inputs_df):
    cards = []

    for index, row in user_inputs_df.iterrows():
        label = escape(str(row["Category"]))
        value = escape(str(row["Selection"]))
        wide_class = " profile-card-wide" if label == "Activities" else ""

        cards.append(
            f'<div class="profile-card{wide_class}" style="animation-delay: {index * 0.035:.2f}s">'
            f'<div class="profile-label">{label}</div>'
            f'<div class="profile-value">{value}</div>'
            "</div>"
        )

    st.markdown(
        '<div class="profile-grid">' + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )



@st.cache_data
def load_tourism_sites():
    tourism_df = pd.read_csv("sites_for_all_countries.csv")
    tourism_df.columns = tourism_df.columns.str.strip().str.lower()
    return tourism_df


def get_tourism_sites(country):
    tourism_df = load_tourism_sites()

    required_columns = ["country", "name", "city", "description"]
    missing_columns = [
        col for col in required_columns if col not in tourism_df.columns
    ]

    if missing_columns:
        st.error(
            "Your sites_for_all_countries.csv file is missing these columns: "
            + ", ".join(missing_columns)
        )
        return []

    country_sites = tourism_df[
        tourism_df["country"].astype(str).str.lower().str.strip()
        == str(country).lower().strip()
    ]

    return country_sites.to_dict("records")


def make_tourism_image_url(country, site_name, city, description, index, csv_image=""):
    image_url = str(csv_image).strip()

    if image_url and image_url.lower() != "nan" and "loremflickr.com" not in image_url:
        separator = "&" if "?" in image_url else "?"
        return f"{image_url}{separator}lock={index + 100}"

    query = quote_plus(
        " ".join(
            str(value).strip()
            for value in [site_name, city, country, "tourism landmark"]
            if str(value).strip()
        )
    )

    thumbnail_server = (index % 4) + 1
    return (
        f"https://tse{thumbnail_server}.mm.bing.net/th"
        f"?q={query}&w=600&h=400&c=7&rs=1&p=0"
    )

def render_tourism_sites(selected_country):
    st.subheader(f"Tourism sites in {selected_country}")

    try:
        sites = get_tourism_sites(selected_country)
    except FileNotFoundError:
        st.error(
            "The file sites_for_all_countries.csv was not found. "
            "Put it in the same folder as your app.py file."
        )
        return

    if not sites:
        st.warning(
            f"No tourism sites found for {selected_country}. "
            "Check that the country name in the CSV matches the model country name."
        )
        return

    cols = st.columns(3)

    for index, site in enumerate(sites):
        with cols[index % 3]:
            name = escape(str(site.get("name", "")))
            city = escape(str(site.get("city", "")))
            description = escape(str(site.get("description", "")))

            image = escape(
                make_tourism_image_url(
                    selected_country,
                    str(site.get("name", "")),
                    str(site.get("city", "")),
                    str(site.get("description", "")),
                    index,
                    site.get("image", ""),
                ),
                quote=True,
            )

            st.markdown(
                f"""
                <div class="activity-card">
                    <img src="{image}" alt="{name}" onerror="this.style.display='none';" />
                    <div class="activity-card-title">{name}</div>
                    <p class="site-city">{city}</p>
                    <p class="site-description">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.step = "home"
    st.rerun()


# =========================================================
# Pages
# =========================================================
def home():
    with st.container(key="home_box"):
        render_brand()
        st.title("Find The Country That Fits You")
        st.write(
            "A faster, warmer travel matcher that learns your style and turns it into "
            "country recommendations."
        )

        st.markdown(
            """
            <div class="hero-stat-row">
                <div class="hero-stat"><strong>10</strong><span>smart steps</span></div>
                <div class="hero-stat"><strong>5</strong><span>top matches</span></div>
                <div class="hero-stat"><strong>AI</strong><span>ranking model</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.container(key="home_button_box"):
        main_button = st.button("Start Journey")

    if main_button:
        go_to("name")


def name_form():
    with st.container(key="wide_form_card"):
        with st.form("name_form", border=False, enter_to_submit=True):
            render_step_intro(1)

            name_value = st.text_input(
                "What is your name, traveller?",
                placeholder="Example: Sara",
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                if name_value.strip() == "":
                    st.error("Please enter your name.")
                else:
                    st.session_state.name = name_value.strip()
                    go_to("age")

        if st.button("Back"):
            go_to("home")


def age():
    with st.container(key="wide_form_card"):
        with st.form("age_form", border=False):
            render_step_intro(2)
            max_birth_date = oldest_allowed_birthdate(7)

            birth_date = st.date_input(
                "Date of birth",
                value=None,
                min_value=date(1900, 1, 1),
                max_value=max_birth_date,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                if birth_date is None:
                    st.error("Please enter your date of birth.")
                elif calculate_age(birth_date) < 7:
                    st.error("Traveller age must be at least 7 years old.")
                else:
                    st.session_state.birth_date = birth_date
                    st.session_state.age = calculate_age(birth_date)
                    go_to("safety")

        if st.button("Back"):
            go_to("name")


def safety():
    with st.container(key="wide_form_card"):
        with st.form("safety_form", border=False):
            render_step_intro(3)

            safety_value = st.radio(
                "Expected safety level",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                format_func=rating_label,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.safety = safety_value
                go_to("food")

        if st.button("Back"):
            go_to("age")


def food():
    with st.container(key="wide_form_card"):
        with st.form("food_form", border=False):
            render_step_intro(4)

            food_value = st.radio(
                "How much do you care about food?",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                format_func=rating_label,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.food = food_value
                go_to("nightlife")

        if st.button("Back"):
            go_to("safety")


def nightlife():
    with st.container(key="wide_form_card"):
        with st.form("nightlife_form", border=False):
            render_step_intro(5)

            nightlife_value = st.radio(
                "How interested are you in nightlife?",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                format_func=rating_label,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.nightlife = nightlife_value
                go_to("nature")

        if st.button("Back"):
            go_to("food")


def nature():
    with st.container(key="wide_form_card"):
        with st.form("nature_form", border=False):
            render_step_intro(6)

            nature_value = st.radio(
                "How interested are you in nature?",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                format_func=rating_label,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.nature = nature_value
                go_to("family_friendly")

        if st.button("Back"):
            go_to("nightlife")


def family_friendly():
    with st.container(key="wide_form_card"):
        with st.form("family_form", border=False):
            render_step_intro(7)

            family_value = st.radio(
                "How family-friendly should the trip be?",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                format_func=rating_label,
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.family_friendly = family_value
                go_to("budget")

        if st.button("Back"):
            go_to("nature")


def budget():
    with st.container(key="wide_form_card"):
        with st.form("budget_form", border=False):
            render_step_intro(8)

            budget_value = st.select_slider(
                "Select your intended budget",
                options=["Low", "Medium", "High"],
                value="Medium",
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.budget = budget_value
                go_to("weather")

        if st.button("Back"):
            go_to("family_friendly")


def weather():
    with st.container(key="wide_form_card"):
        with st.form("weather_form", border=False):
            render_step_intro(9)

            weather_value = st.select_slider(
                "Choose your preferred weather",
                options=["cold", "warm", "hot"],
                value="warm",
            )

            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted:
                st.session_state.weather = weather_value
                go_to("activities")

        if st.button("Back"):
            go_to("budget")


def activities():
    with st.container(key="wide_form_card"):
        with st.form("activities_form", border=False):
            render_step_intro(10)

            activities_value = st.pills(
                "Choose activities you are interested in",
                activities_options,
                selection_mode="multi",
                key="activity_pills",
            )

            submitted = st.form_submit_button("Show Results", use_container_width=True)

            if submitted:
                if not activities_value:
                    st.error("Please choose at least one activity.")
                else:
                    st.session_state.activities = activities_value
                    go_to("exit")

        if st.button("Back"):
            go_to("weather")


def exit_page():
    name = st.session_state.get("name", "Traveller")
    birth_date = st.session_state.get("birth_date", "Not entered")
    age_value = st.session_state.get("age", 18)
    safety_value = st.session_state.get("safety", 1)
    food_value = st.session_state.get("food", 1)
    nightlife_value = st.session_state.get("nightlife", 1)
    nature_value = st.session_state.get("nature", 1)
    family_value = st.session_state.get("family_friendly", 1)
    budget_value = st.session_state.get("budget", "Medium")
    weather_value = st.session_state.get("weather", "warm")
    activities_value = st.session_state.get("activities", [])
    activities_list = list(activities_value)

    user_data = {
        "age": age_value,
        "safety": safety_value,
        "food": int(food_value),
        "nightlife": int(nightlife_value),
        "nature": int(nature_value),
        "family_friendly": int(family_value),
        "budget": budget_value,
        "weather": weather_value,
        "activities": ", ".join(activities_list),
    }

    user_inputs_df = make_user_dataframe(
        name=name,
        birth_date=birth_date,
        age_value=age_value,
        safety_value=safety_value,
        food_value=food_value,
        nightlife_value=nightlife_value,
        nature_value=nature_value,
        family_value=family_value,
        budget_value=budget_value,
        weather_value=weather_value,
        activities_value=activities_list,
    )

    recommendations_df = get_recommendations(user_data)
    best_match = recommendations_df.iloc[0]

    with st.container(key="dashboard_box"):
        render_brand()
        st.title("Your Travel Dashboard")
        st.write("Your profile and AI country recommendations")

        st.markdown(
            f"""
            <div class="match-hero">
                <small>Best match</small>
                <h2>{escape(str(best_match["Country"]))}</h2>
                <p>{escape(str(best_match["Match %"]))}% match based on your travel profile.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("Traveller", name)
        metric2.metric("Age", age_value)
        metric3.metric("Budget", budget_value)
        metric4.metric("Weather", weather_value)

        overview_tab, profile_tab, country_activities_tab = st.tabs(
            ["Recommendations", "Your Profile", "Country Activities"]
        )

        with overview_tab:
            st.subheader("Top 5 Countries")
            render_match_cards(recommendations_df)

        with profile_tab:
            left, right = st.columns([1, 1])

            with left:
                st.subheader("Your Inputs")
                render_profile_cards(user_inputs_df)

            with right:
                st.subheader("Your Selected Activities")

                if activities_list:
                    activity_cols = st.columns(3)

                    for index, activity in enumerate(activities_list):
                        with activity_cols[index % 3]:
                            st.info(activity)
                else:
                    st.warning("No activities selected.")

        with country_activities_tab:
            selected_country = st.selectbox(
                "Select a recommended country to explore",
                options=recommendations_df["Country"].tolist(),
                key="country_selector",
            )

            render_tourism_sites(selected_country)

        with st.container(key="start_over_box"):
            if st.button("Start Over"):
                reset_app()



pages = {
    "home": home,
    "name": name_form,
    "age": age,
    "safety": safety,
    "food": food,
    "nightlife": nightlife,
    "nature": nature,
    "family_friendly": family_friendly,
    "budget": budget,
    "weather": weather,
    "activities": activities,
    "exit": exit_page,
}

pages.get(st.session_state.step, home)()
