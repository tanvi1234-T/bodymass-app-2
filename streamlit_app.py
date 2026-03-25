import streamlit as st
import json
import hashlib
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# User database file
USERS_DB = "users.json"

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if Path(USERS_DB).exists():
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_DB, 'w') as f:
        json.dump(users, f)

def is_input_valid(text, min_len=1, max_len=28):
    """Generic validation for text inputs: size, forbidden chars, no whitespace for username fields."""
    forbidden = set('=<>"\'')
    if not isinstance(text, str):
        return False, "Input must be text."
    if len(text) < min_len or len(text) > max_len:
        return False, f"Input length must be between {min_len} and {max_len} characters."
    if any(ch in forbidden for ch in text):
        return False, "Input may not contain any of these characters: = < > ' \""
    if any(ch.isspace() for ch in text):
        return False, "Input may not contain spaces."
    return True, ""


def is_password_strong(password):
    """Password restrictions: 12<x<28, uppercase, lowercase, special char, no forbidden chars."""
    if not isinstance(password, str):
        return False, "Password must be text."
    if len(password) <= 12 or len(password) >= 28:
        return False, "Password must be longer than 12 and shorter than 28 characters."
    forbidden = set('=<>"\'')
    if any(ch in forbidden for ch in password):
        return False, "Password cannot contain any of: = < > ' \""
    if any(ch.isspace() for ch in password):
        return False, "Password cannot contain spaces."
    if password.lower() == password or password.upper() == password:
        return False, "Password must include both uppercase and lowercase letters."
    if not any(not c.isalnum() for c in password):
        return False, "Password must include at least one special character."
    if not all(32 < ord(c) < 127 for c in password):
        return False, "Password contains unsupported characters."
    return True, ""


def signup(username, password, confirm_password):
    """Register a new user"""
    users = load_users()

    valid_username, message = is_input_valid(username, min_len=3, max_len=28)
    if not valid_username:
        return False, message
    if username in users:
        return False, "Username already exists"

    if password != confirm_password:
        return False, "Passwords do not match"

    valid_pw, message = is_password_strong(password)
    if not valid_pw:
        return False, message

    users[username] = hash_password(password)
    save_users(users)
    return True, "Account created successfully! Please login."

def login(username, password):
    """Authenticate user"""
    users = load_users()

    valid_username, message = is_input_valid(username, min_len=3, max_len=28)
    if not valid_username:
        return False, message

    if username not in users:
        return False, "Username not found"

    valid_pw, message = is_input_valid(password, min_len=1, max_len=28)
    if not valid_pw:
        return False, message

    if users[username] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful!"

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Custom CSS for matcha green background and minimalistic aesthetic
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', 'Poppins', sans-serif;
        }
        
        h1 {
            color: #2d5d4a;
            font-family: 'Poppins', sans-serif;
            text-align: center;
            margin-bottom: 20px;
            font-size: 52px;
            font-weight: 700;
            letter-spacing: -1px;
            text-shadow: 0 2px 4px rgba(45, 93, 74, 0.1);
        }
        
        h2 {
            color: #2d5d4a;
            font-family: 'Poppins', sans-serif;
            margin-top: 30px;
            margin-bottom: 20px;
            font-size: 36px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        h3 {
            color: #3d6d59;
            font-family: 'Poppins', sans-serif;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.2px;
        }
        
        p, span, label, div {
            color: #5a6d63;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }
        
        body {
            background: linear-gradient(135deg, #d8eddb 0%, #bcdeb4 50%, #c8ebd3 100%);
            background-attachment: fixed;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            color: #2d5d4a;
            overflow-x: hidden;
        }
        
        .block-container {
            padding: 0 15px 15px 15px !important;
            margin: 0 auto !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        
        .main {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        .element-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 3px solid #d4e9d8 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border-bottom: 3px solid transparent !important;
            padding: 12px 20px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: transparent !important;
            border-bottom: 3px solid #7fa893 !important;
            color: #2d5d4a !important;
        }
        
        .stTabs [aria-selected="false"] {
            color: #7fa893 !important;
        }
        
        .css-1r6slur {
            background-color: #f0f7f2 !important;
            border: 1.5px solid #d4e9d8 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(45, 93, 74, 0.08) !important;
        }
        
        .streamlit-expanderHeader {
            color: #2d5d4a !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            padding: 12px !important;
            border-radius: 8px !important;
        }
        
        /* Panels and cards */
        .stApp > div:first-child {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 15px 40px rgba(45, 93, 74, 0.12);
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }
        
        /* Metric styling */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #f5faf7 0%, #e8f4e8 100%);
            padding: 22px;
            border-radius: 16px;
            border: 2px solid #d4e9d8;
            border-left: 6px solid #7fa893;
            box-shadow: 0 8px 24px rgba(45, 93, 74, 0.1);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(45, 93, 74, 0.15);
        }
        
        /* Input styling */
        .stNumberInput input, .stSelectbox select {
            border-radius: 12px !important;
            border: 2px solid #d4e9d8 !important;
            background-color: rgba(245, 250, 247, 0.9) !important;
            color: #2d5d4a !important;
            padding: 12px 14px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        
        .stNumberInput input:focus, .stSelectbox select:focus {
            border-color: #7fa893 !important;
            box-shadow: 0 0 0 3px rgba(127, 168, 147, 0.15) !important;
            background-color: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #7fa893 0%, #6d9682 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-family: 'Poppins', sans-serif !important;
            padding: 14px 32px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            min-height: 48px !important;
            letter-spacing: 0.5px !important;
            cursor: pointer !important;
            box-shadow: 0 6px 20px rgba(127, 168, 147, 0.25) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #5a8671 0%, #4d7d69 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(45, 93, 74, 0.35) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Field containers spacing */
        .stSelectbox, .stNumberInput, .stTextInput {
            margin-bottom: 18px !important;
        }
        
        /* Text input styling */
        .stTextInput input {
            border-radius: 12px !important;
            border: 2px solid #d4e9d8 !important;
            background-color: rgba(245, 250, 247, 0.9) !important;
            color: #2d5d4a !important;
            font-family: 'Inter', sans-serif !important;
            padding: 12px 14px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: #7fa893 !important;
            box-shadow: 0 0 0 3px rgba(127, 168, 147, 0.15) !important;
            background-color: white !important;
        }
        
        .stTextInput input::placeholder {
            color: #7fa893 !important;
            opacity: 0.7 !important;
        }
        
        /* Success and info messages */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            padding: 16px 20px !important;
            border-left: 5px solid !important;
            backdrop-filter: blur(10px) !important;
        }
        
        div[data-testid="stAlert"][style*="success"] {
            background-color: rgba(168, 217, 168, 0.15) !important;
            border-left-color: #7fa893 !important;
            color: #2d5d4a !important;
        }
        
        div[data-testid="stAlert"][style*="error"] {
            background-color: rgba(217, 184, 184, 0.15) !important;
            border-left-color: #d9b8b8 !important;
            color: #6b4545 !important;
        }
        
        div[data-testid="stAlert"][style*="info"] {
            background-color: rgba(184, 224, 212, 0.15) !important;
            border-left-color: #7fa893 !important;
            color: #2d5d4a !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(232, 244, 232, 0.6) !important;
            border-right: 2px solid #d4e9d8 !important;
        }
        
        /* Image styling */
        img {
            border-radius: 14px !important;
            box-shadow: 0 8px 24px rgba(45, 93, 74, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        img:hover {
            transform: scale(1.02);
            box-shadow: 0 12px 32px rgba(45, 93, 74, 0.25) !important;
        }
        
        /* Polka dot decorations - extensive scattered pattern with matcha green and light blue */
        .stApp::before {
            content: '';
            position: fixed;
            top: 5%;
            right: 8%;
            width: 80px;
            height: 80px;
            background-color: #a8d9a8;
            border-radius: 50%;
            opacity: 0.4;
            pointer-events: none;
            z-index: 0;
            box-shadow: 
                150px 200px 0 60px rgba(168, 217, 168, 0.35),
                -100px 300px 0 70px rgba(139, 196, 151, 0.3),
                200px 500px 0 50px rgba(168, 217, 168, 0.38),
                -50px 600px 0 65px rgba(127, 168, 147, 0.32),
                250px 150px 0 55px rgba(139, 196, 151, 0.36),
                -200px 100px 0 75px rgba(168, 217, 168, 0.33),
                300px 400px 0 45px rgba(127, 168, 147, 0.34),
                -150px 450px 0 60px rgba(139, 196, 151, 0.35),
                100px 50px 0 70px rgba(168, 217, 168, 0.31),
                -300px 250px 0 55px rgba(127, 168, 147, 0.37),
                80px 400px 0 65px rgba(168, 197, 214, 0.34),
                -180px 200px 0 55px rgba(184, 212, 232, 0.32),
                280px 100px 0 50px rgba(162, 196, 220, 0.35),
                -220px 350px 0 60px rgba(184, 212, 232, 0.31),
                150px -50px 0 55px rgba(168, 197, 214, 0.36),
                -280px 500px 0 70px rgba(184, 212, 232, 0.30);
        }
        
        .stApp::after {
            content: '';
            position: fixed;
            bottom: 15%;
            left: 5%;
            width: 100px;
            height: 100px;
            background-color: #8bc497;
            border-radius: 50%;
            opacity: 0.35;
            pointer-events: none;
            z-index: 0;
            box-shadow: 
                180px -100px 0 65px rgba(139, 196, 151, 0.32),
                -120px -200px 0 55px rgba(168, 217, 168, 0.36),
                220px 150px 0 50px rgba(127, 168, 147, 0.34),
                -250px 100px 0 70px rgba(139, 196, 151, 0.33),
                150px -300px 0 60px rgba(168, 217, 168, 0.35),
                -180px 300px 0 45px rgba(127, 168, 147, 0.38),
                280px -50px 0 65px rgba(139, 196, 151, 0.31),
                -80px -100px 0 55px rgba(168, 217, 168, 0.37),
                200px 250px 0 50px rgba(127, 168, 147, 0.33),
                -300px -150px 0 70px rgba(139, 196, 151, 0.34),
                120px 80px 0 60px rgba(184, 212, 232, 0.33),
                -200px 50px 0 55px rgba(168, 197, 214, 0.32),
                250px -200px 0 65px rgba(184, 212, 232, 0.31),
                -150px 200px 0 50px rgba(162, 196, 220, 0.35),
                200px 50px 0 60px rgba(184, 212, 232, 0.30),
                -280px -100px 0 55px rgba(168, 197, 214, 0.34);
        }
        
        .stApp > div:first-child::before {
            content: '';
            position: absolute;
            top: 25%;
            right: -50px;
            width: 90px;
            height: 90px;
            background-color: #a8d9a8;
            border-radius: 50%;
            opacity: 0.3;
            pointer-events: none;
            box-shadow: 
                120px 150px 0 50px rgba(139, 196, 151, 0.32),
                -100px 250px 0 60px rgba(168, 217, 168, 0.28),
                180px -100px 0 55px rgba(127, 168, 147, 0.35),
                -150px -50px 0 65px rgba(139, 196, 151, 0.29),
                200px 200px 0 45px rgba(168, 217, 168, 0.33),
                80px 50px 0 55px rgba(184, 212, 232, 0.30),
                -200px 150px 0 60px rgba(168, 197, 214, 0.32),
                150px 280px 0 50px rgba(184, 212, 232, 0.28),
                -120px 100px 0 55px rgba(162, 196, 220, 0.31);
        }
        
        .stApp > div:first-child::after {
            content: '';
            position: absolute;
            bottom: 10%;
            left: -60px;
            width: 110px;
            height: 110px;
            background-color: #8bc497;
            border-radius: 50%;
            opacity: 0.25;
            pointer-events: none;
            box-shadow: 
                150px -150px 0 55px rgba(168, 217, 168, 0.31),
                -120px 180px 0 60px rgba(139, 196, 151, 0.30),
                200px 100px 0 50px rgba(127, 168, 147, 0.32),
                -200px -100px 0 65px rgba(168, 217, 168, 0.28),
                250px 250px 0 45px rgba(139, 196, 151, 0.34),
                100px 50px 0 60px rgba(184, 212, 232, 0.29),
                -180px -50px 0 55px rgba(168, 197, 214, 0.31),
                220px 200px 0 50px rgba(184, 212, 232, 0.27),
                -240px 150px 0 55px rgba(162, 196, 220, 0.30);
        }
        
        /* Additional polka dots on sidebar and containers */
        [data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            top: 15%;
            right: -50px;
            width: 75px;
            height: 75px;
            background-color: #a8d9a8;
            border-radius: 50%;
            opacity: 0.25;
            pointer-events: none;
            box-shadow: 
                150px 200px 0 55px rgba(139, 196, 151, 0.28),
                -100px 300px 0 60px rgba(168, 217, 168, 0.26),
                120px 50px 0 55px rgba(184, 212, 232, 0.27),
                -180px 150px 0 60px rgba(168, 197, 214, 0.25),
                200px 250px 0 50px rgba(184, 212, 232, 0.28);
        }
    </style>
    """, unsafe_allow_html=True)

# Authentication UI
if not st.session_state.logged_in:
    st.markdown("<h1 style='padding-top: 12px;'>⚖️ Body Mass Index Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #3d6d59; font-size: 16px;'>Create an account or login to get started</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown("<h3 style='text-align: center;'>Welcome Back</h3>", unsafe_allow_html=True)
        
        login_username = st.text_input("Username", key="login_username", placeholder="Enter your username", max_chars=28)
        login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password", max_chars=28)
        
        if st.button("Login", use_container_width=True, type="primary", key="login_button"):
            if login_username and login_password:
                success, message = login(login_username, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")
    
    with tab2:
        st.markdown("<h3 style='text-align: center;'>Create Account</h3>", unsafe_allow_html=True)
        
        signup_username = st.text_input("Create Username", key="signup_username", placeholder="Choose a username (min 3 characters)", max_chars=28)
        signup_password = st.text_input("Create Password", type="password", key="signup_password", placeholder="Create a password (13-27 chars, upper+lower+special)", max_chars=28)
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Confirm your password", max_chars=28)
        
        if st.button("Sign Up", use_container_width=True, type="primary", key="signup_button"):
            if signup_username and signup_password and signup_confirm:
                success, message = signup(signup_username, signup_password, signup_confirm)
                if success:
                    st.success(message)
                    st.info("You can now login with your credentials in the Login tab.")
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
    
    st.stop()

# Main BMI Calculator (only shown when logged in)
st.markdown("<div style='display: flex; justify-content: space-between; align-items: center; margin-top: 0px;'><h1 style='margin: 0;'>⚖️ Body Mass Index Calculator</h1></div>", unsafe_allow_html=True)

# Logout button in sidebar
with st.sidebar:
    st.markdown(f"<p style='color: #3d6d59;'>Logged in as: <b>{st.session_state.username}</b></p>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        logout()

st.markdown("<p style='text-align: center; color: #3d6d59; font-size: 16px;'>Calculate your BMI and get personalized health recommendations</p>", unsafe_allow_html=True)

# BMI Categories and Health Standards
BMI_CATEGORIES = {
    'Underweight': {'min': 0, 'max': 18.4, 'color': '#b8e0d4', 'emoji': '🔵'},
    'Normal Weight': {'min': 18.5, 'max': 24.9, 'color': '#a8d9a8', 'emoji': '🟢'},
    'Overweight': {'min': 25.0, 'max': 29.9, 'color': '#d4c9a8', 'emoji': '🟡'},
    'Obese': {'min': 30.0, 'max': 100, 'color': '#d9b8b8', 'emoji': '🔴'}
}

# Caloric Recommendations (daily intake)
CALORIC_RECOMMENDATIONS = {
    'Underweight': {
        'calories': '2500-3000 kcal',
        'description': 'Focus on nutrient-dense foods to gain weight healthily',
        'foods': ['Nuts and nut butters', 'Avocados', 'Olive oil', 'Whole grains', 'Lean proteins', 'Dairy products', 'Seeds']
    },
    'Normal Weight': {
        'calories': '1800-2500 kcal',
        'description': 'Maintain a balanced, healthy diet',
        'foods': ['Fruits and vegetables', 'Whole grains', 'Lean proteins', 'Low-fat dairy', 'Legumes', 'Fish', 'Nuts']
    },
    'Overweight': {
        'calories': '1500-2000 kcal',
        'description': 'Focus on calorie control and regular exercise',
        'foods': ['Leafy greens', 'Cruciferous vegetables', 'Lean proteins', 'Whole grains', 'Berries', 'Fish', 'Legumes']
    },
    'Obese': {
        'calories': '1200-1800 kcal',
        'description': 'Work with a professional for a structured diet plan',
        'foods': ['Low-calorie vegetables', 'Lean proteins', 'Whole grains', 'Berries', 'Green tea', 'Fish', 'Legumes']
    }
}

# Initialize session state for BMI calculator
if 'bmi' not in st.session_state:
    st.session_state.bmi = None
if 'category' not in st.session_state:
    st.session_state.category = None

# Parse query parameters
query_params = st.query_params

# Set defaults from query parameters
default_weight = 70.0
default_weight_unit = "Kilograms (kg)"
default_height = 170.0
default_height_unit = "Centimeters (cm)"
default_feet = 5
default_inches = 7
auto_calculate = False

if "weight" in query_params:
    try:
        default_weight = float(query_params["weight"])
    except ValueError:
        pass

if "weight_unit" in query_params:
    unit_param = query_params["weight_unit"].lower()
    if unit_param == "lbs":
        default_weight_unit = "Pounds (lbs)"
    elif unit_param == "kg":
        default_weight_unit = "Kilograms (kg)"

if "height" in query_params:
    try:
        default_height = float(query_params["height"])
    except ValueError:
        pass

if "height_unit" in query_params:
    unit_param = query_params["height_unit"].lower()
    if unit_param == "cm":
        default_height_unit = "Centimeters (cm)"
    elif unit_param == "ft_in":
        default_height_unit = "Feet and Inches"

if "feet" in query_params:
    try:
        default_feet = int(query_params["feet"])
    except ValueError:
        pass

if "inches" in query_params:
    try:
        default_inches = int(query_params["inches"])
    except ValueError:
        pass

if "auto_calculate" in query_params:
    auto_calculate = query_params["auto_calculate"].lower() == "true"

# Input Section
st.markdown("<h2>📊 Your Measurements</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    weight_unit = st.selectbox(
        "Weight Unit",
        ["Kilograms (kg)", "Pounds (lbs)"],
        index=0 if default_weight_unit == "Kilograms (kg)" else 1,
        key="weight_unit"
    )
    weight = st.number_input(
        "Weight",
        min_value=20.0,
        max_value=500.0,
        step=0.1,
        value=default_weight,
        help="Enter your weight"
    )

with col2:
    height_unit = st.selectbox(
        "Height Unit",
        ["Centimeters (cm)", "Feet and Inches"],
        index=0 if default_height_unit == "Centimeters (cm)" else 1,
        key="height_unit"
    )
    
    if height_unit == "Centimeters (cm)":
        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            step=0.1,
            value=default_height,
            help="Enter your height in centimeters"
        )
    else:
        feet = st.number_input("Feet", min_value=3, max_value=8, step=1, value=default_feet, format="%d")
        inches = st.number_input("Inches", min_value=0, max_value=11, step=1, value=default_inches, format="%d")
        height = feet * 30.48 + inches * 2.54  # Convert to cm

# Calculate BMI
calculate_button = st.button("Calculate BMI", use_container_width=True, type="primary")

# Auto-calculate if parameter is set
if auto_calculate and not st.session_state.get('auto_calculated', False):
    calculate_button = True
    st.session_state.auto_calculated = True

if calculate_button:
    # Convert weight to kg if needed
    if weight_unit == "Pounds (lbs)":
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight
    
    # Height in meters
    height_m = height / 100
    
    # Calculate BMI
    bmi = weight_kg / (height_m ** 2)
    st.session_state.bmi = bmi
    
    # Determine category
    for category, details in BMI_CATEGORIES.items():
        if details['min'] <= bmi <= details['max']:
            st.session_state.category = category
            break

# Display Results
if st.session_state.bmi is not None:
    st.markdown("<h2>📈 Your Results</h2>", unsafe_allow_html=True)
    
    # BMI Value and Category
    col1, col2 = st.columns(2)
    
    category_info = BMI_CATEGORIES[st.session_state.category]
    
    with col1:
        st.metric(
            label="Your BMI",
            value=f"{st.session_state.bmi:.1f}",
            help="Body Mass Index"
        )
    
    with col2:
        st.markdown(f"""
            <div style='background-color: {category_info['color']}; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='margin: 0; color: white;'>{category_info['emoji']} {st.session_state.category}</h3>
            </div>
        """, unsafe_allow_html=True)
    
    # Health Status Message
    status_messages = {
        'Underweight': "Your BMI indicates you are underweight. You may need to increase your caloric intake to reach a healthy weight.",
        'Normal Weight': "Great! Your BMI indicates you are at a healthy weight. Keep maintaining your lifestyle!",
        'Overweight': "Your BMI indicates you are overweight. Consider implementing a balanced diet and regular exercise routine.",
        'Obese': "Your BMI indicates obesity. We recommend consulting with a healthcare professional for personalized guidance."
    }
    
    st.info(f"ℹ️ {status_messages[st.session_state.category]}")
    
    # BMI Formula Section
    st.markdown("<h2>📐 BMI Formula</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: #e8f4e8; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: #2d5d4a; margin: 0;'>BMI = Weight (kg) / Height (m)²</h3>
            <p style='color: #3d6d59; font-size: 14px; margin-top: 10px;'>
                Where weight is in kilograms and height is in meters
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Recommendations Section
    st.markdown("<h2>💡 Personalized Recommendations</h2>", unsafe_allow_html=True)
    
    rec = CALORIC_RECOMMENDATIONS[st.session_state.category]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style='background-color: #e8f4e8; padding: 15px; border-radius: 10px;'>
                <h3 style='color: #2d5d4a; margin-top: 0;'>Daily Caloric Intake</h3>
                <p style='font-size: 20px; color: #3d6d59; font-weight: bold;'>{rec['calories']}</p>
                <p style='color: #3d6d59; font-size: 14px;'>{rec['description']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background-color: #e8f4e8; padding: 15px; border-radius: 10px;'>
                <h3 style='color: #2d5d4a; margin-top: 0;'>Recommended Foods</h3>
                <ul style='color: #3d6d59; margin: 0; padding-left: 20px;'>
                    {''.join([f'<li>{food}</li>' for food in rec['foods']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # BMI Categories Reference
    st.markdown("<h2>📋 BMI Categories Reference</h2>", unsafe_allow_html=True)
    
    reference_data = {
        'Category': [],
        'BMI Range': [],
        'Status': []
    }
    
    for category, details in BMI_CATEGORIES.items():
        reference_data['Category'].append(f"{details['emoji']} {category}")
        reference_data['BMI Range'].append(f"{details['min']} - {details['max']}")
        reference_data['Status'].append("Underweight" if category == 'Underweight' else "Healthy" if category == 'Normal Weight' else "Needs Attention")
    
    st.table(reference_data)
