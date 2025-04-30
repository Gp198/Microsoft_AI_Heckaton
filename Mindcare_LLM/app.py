import streamlit as st
from dotenv import load_dotenv
from triage_module import TriageAgent
from agents import HumanEscalationHandler

# Load environment variables
load_dotenv()

# Configure the Streamlit UI
st.set_page_config(
    page_title="MindCare Agent Network",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h1 style='color: #2C3E50;'>🧠 MindCare Agent Network</h1>
        <p style='font-size: 18px; color: #34495E;'>Multilingual AI for Mental Health in the Workplace</p>
    </div>
    """, unsafe_allow_html=True
)

# Instructions section
with st.expander("ℹ️ How to Use This App", expanded=True):
    st.markdown("""
    **Instructions**:
    - Describe how you feel at work in English or Portuguese (Portugal).
    - The system will route you to the most appropriate support agent.
    - Try different cases:
        - Mental health: *"I feel overwhelmed with deadlines"*
        - Team issue: *"My team doesn't communicate well"*
        - HR support: *"Can I switch to a flexible schedule?"*
        - Escalation: *"I feel like giving up"*
    """)

# --- Sidebar controls ---
st.sidebar.title("🛠️ GPT Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 1.0, 0.05)
max_tokens = st.sidebar.slider("Max Tokens", 64, 1024, 300, 32)

# --- Chat UI ---
user_input = st.text_area("How have you been feeling at work lately?", "")

if st.button("Submit") and user_input:
    escalation = HumanEscalationHandler()
    if escalation.detect_risk(user_input):
        st.markdown(f"**🚨 Human Escalation Handler:** {escalation.trigger_escalation()}")
    else:
        triage = TriageAgent("Triage Agent")
        summary, agent = triage.respond(user_input)
        st.markdown(f"**🧠 Triage Agent:** {summary}")
        if agent:
            agent.client_params = {
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens
            }
            with st.spinner("Agent is thinking..."):
                try:
                    response = agent.respond(user_input)
                except Exception as e:
                    response = f"⚠️ Error: {str(e)}"
            st.markdown(f"**👤 {agent.name}:** {response}")

# --- Footer ---
st.markdown(
    """
    <hr style="margin-top: 2rem;">
    <p style='text-align: center; font-size: 14px; color: gray;'>
        © 2025 MindCare – Built for Microsoft AI Hackathon
    </p>
    """, unsafe_allow_html=True
)
