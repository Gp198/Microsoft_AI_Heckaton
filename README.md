# 🧠 MindCare Agent Network

## Overview
**MindCare Agent Network** is an AI-powered, multi-agent system built to proactively assess and support employee mental health.  
It uses intelligent triage, GPT-powered agents, and safety guardrails to deliver ethical, responsive, and multilingual mental health support.

Built with Azure OpenAI GPT-4o and Python (Streamlit), the system integrates Responsible AI best practices, dynamic parameter tuning, and real-time escalation to a human when risk is detected.

---

## 🔬 Innovation
- **Multi-Agent Architecture**: Decentralized system with GPT-4o agents handling specific domains (HR, Psychology, Mental Health).
- **Dual Language Support**: Seamlessly handles user input in both English and Portuguese (Portugal).
- **Human-in-the-Loop Escalation**: Automatically detects emotional distress and routes user to a human specialist.
- **Dynamic GPT Control**: Users adjust temperature, top_p, and max_tokens from the UI for real-time tuning.

---

## 🌍 Impact
- Designed to support **mental wellness** in corporations, schools, and public-sector teams.
- Prevents burnout through **accessible, stigma-free interaction**.
- Reduces pressure on HR by providing 24/7 first-line AI guidance.
- Enables organizations to scale mental health initiatives ethically and securely.

---

## 🧪 Usability
- Addresses a **critical real-world problem**: emotional exhaustion and stress in professional settings.
- Includes **real-time emotional risk detection** with automatic escalation.
- Guided **Streamlit interface** ensures accessibility for non-technical users.
- Built-in **language awareness** and ethical constraints prevent unsafe behavior.

---

## 👥 Agent Network Architecture

| Agent                     | Purpose                                                      |
|--------------------------|--------------------------------------------------------------|
| Triage Agent             | Routes user input based on content and safety analysis       |
| Mental Health Agent      | Provides practical, empathetic support for emotional distress|
| Organizational Psychology Agent | Offers team/workplace optimization tips          |
| Human Resources Agent    | Explains flexibility options and HR policies                 |
| Human Escalation Handler | Triggers alerts on detection of emotional danger             |


![image](https://github.com/user-attachments/assets/b4631e74-ba98-4fa5-b0b4-5f33a922be64)


---

## 📁 Project Structure

| File/Folder               | Purpose                                                                          |
|--------------------------|----------------------------------------------------------------------------------|
| `app.py`                 | Final Streamlit application with UI, branding, safety, and model controls        |
| `agents.py`              | Main agents using GPT-4o and professional prompts with risk detection     |
| `triage_module.py`       | Classifies input and routes to proper agent or escalates on emotional risk      |
| `requirements.txt`       | Lists Python packages (Streamlit, OpenAI SDK, Dotenv)                           |
| `Procfile`               | Launch script for deployment (Streamlit Cloud or Azure Web Apps)                |
| `setup.sh`               | Optional setup file for cloud environments                                      |
| `.env.`                  | Template for environment variables (`OPENAI_API_KEY`, `DEPLOYMENT`, etc.)      |
| `README.md`              | This file — describes functionality, architecture, and purpose                  |

---

## 🌍 Languages Supported
- English
- Portuguese (Portugal)

---

## 🛡️ Safety Guardrails
- **Keyword Escalation**: Triggers on 15+ terms for crisis/emotional risk.
- **No personal data stored**.
- **Ethical prompt design** — never offers diagnoses or final decisions.

---

## 🎛️ GPT Model Controls
- Adjustable from the sidebar:
  - `temperature`
  - `top_p`
  - `max_tokens`
- All settings passed live to GPT-4o.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add environment variables (or use .env file)
# Example .env:
OPENAI_API_KEY=your-api-key
OPENAI_ENDPOINT=https://your-azure-instance.openai.azure.com/
OPENAI_DEPLOYMENT=gpt-4o-deployment-name

# 3. Run the app
streamlit run app.py
```

---

## 📽️ Demo Video
[Insert your video demo link here]

---

## 🧾 Submission Details
- **Category**: Responsible AI / Python / Azure OpenAI
- **Team**: [StatiC]
- **Platform**: Azure + Streamlit

---

## 📜 License
MIT License

Done by Gonçalo Pedro for the Microsoft AI Hackaton
