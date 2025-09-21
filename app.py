import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

# --- Helper Functions ---
def get_auth_headers():
    if "token" in st.session_state and st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

# --- App State ---
if "token" not in st.session_state:
    st.session_state.token = None

# --- Main App ---
st.set_page_config(page_title="Cognitive Bias Auditor", layout="centered")
st.title("🧠 Cognitive Bias Auditor")
st.caption("A private space to reflect on your thinking.")

# --- Authentication Logic ---
if not st.session_state.token:
    st.info("Please log in or register to begin.")
    login_tab, register_tab = st.tabs(["Login", "Register"])
    
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                response = requests.post(f"{API_BASE_URL}/token", data={"username": username, "password": password})
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    st.success("Logged in!")
                    # FIX: Changed to st.rerun()
                    st.rerun()
                else:
                    st.error("Login failed. Please check your credentials.")

    with register_tab:
        with st.form("register_form"):
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                response = requests.post(f"{API_BASE_URL}/users/", json={"username": username, "password": password})
                if response.status_code == 200:
                    st.success("Registration successful! Please log in.")
                else:
                    st.error(f"Registration failed: {response.text}")
else:
    # --- Logged-in Main Application ---
    st.sidebar.success("You are logged in.")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        # FIX: Changed to st.rerun()
        st.rerun()

    st.header("New Reflection")
    reflection_text = st.text_area("Write about a recent decision, argument, or belief you've been pondering...", height=250, key="reflection_input")

    if st.button("Analyze My Thinking"):
        if reflection_text:
            with st.spinner("Your cognitive coach is analyzing your reflection..."):
                headers = get_auth_headers()
                payload = {"content": reflection_text}
                response = requests.post(f"{API_BASE_URL}/reflections/", headers=headers, json=payload)
                
                if response.status_code == 200:
                    analysis = response.json()
                    st.markdown("---")
                    st.subheader("Analysis Complete")
                    st.markdown(analysis["content"])
                else:
                    st.error(f"An error occurred: {response.text}")
        else:
            st.warning("Please write a reflection before analyzing.")
            
    st.markdown("---")
    
    # --- Display Past Reflections ---
    if st.expander("View Past Reflections"):
        headers = get_auth_headers()
        response = requests.get(f"{API_BASE_URL}/reflections/", headers=headers)
        if response.status_code == 200:
            past_reflections = sorted(response.json(), key=lambda r: r['timestamp'], reverse=True)
            if not past_reflections:
                st.write("You have no past reflections yet.")
            for reflection in past_reflections:
                with st.container():
                    st.caption(f"Reflected on: {reflection['timestamp']}")
                    st.markdown(f"> {reflection['content']}")
                    if reflection.get('analysis'):
                        st.markdown("**AI Analysis:**")
                        st.markdown(reflection['analysis']['content'])
                    st.markdown("---")
        else:
            st.error("Could not load past reflections.")