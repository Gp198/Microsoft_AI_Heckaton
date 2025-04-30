import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load .env variables
load_dotenv()

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

class BaseAgent:
    """Base class for AI support agents."""
    def __init__(self, name, role_prompt):
        self.name = name
        self.role_prompt = role_prompt
        self.client_params = {
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 500
        }

    def respond(self, message):
        try:
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": self.role_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=self.client_params.get("temperature", 0.7),
                top_p=self.client_params.get("top_p", 1.0),
                max_tokens=self.client_params.get("max_tokens", 500)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

class MentalHealthAgent(BaseAgent):
    def __init__(self):
        prompt = (
            "You are a certified digital mental health assistant trained to provide empathetic, practical, and evidence-based "
            "strategies to manage stress, anxiety, and emotional fatigue in professional settings. "
            "Do not diagnose. Always encourage users to seek licensed mental health professionals if symptoms persist. "
            "Be respectful, supportive, and solution-oriented. "
            "⚠️ Respond in the same language as the user's message (English or Portuguese - Portugal)."
        )
        super().__init__("Mental Health Agent", prompt)

class OrganizationalPsychologyAgent(BaseAgent):
    def __init__(self):
        prompt = (
            "You are an expert in organizational psychology. Your job is to identify interpersonal, environmental, or structural factors "
            "in the workplace that could be affecting well-being. Offer actionable, practical recommendations on team communication, "
            "leadership feedback, or workflow redesign. Keep tone professional, respectful, and human-centered. "
            "⚠️ Respond in the same language as the user's message (English or Portuguese - Portugal)."
        )
        super().__init__("Organizational Psychology Agent", prompt)

class HumanResourcesAgent(BaseAgent):
    def __init__(self):
        prompt = (
            "You are a digital HR assistant trained to provide guidance on internal policies, wellness initiatives, "
            "flexible work arrangements, and employee support systems. Suggest reasonable accommodations and next steps "
            "to foster healthier work-life balance. Avoid making commitments — only provide examples of typical HR actions. "
            "⚠️ Respond in the same language as the user's message (English or Portuguese - Portugal)."
        )
        super().__init__("Human Resources Agent", prompt)

class HumanEscalationHandler:
    """Detects and responds to high-risk mental health language."""
    def __init__(self):
        self.risk_keywords = [
            "give up", "can't go on", "end it", "kill myself", "no way out", "hopeless", "worthless",
            "suicide", "end everything", "I want to die", "I want to disappear", "take my life",
            "I'm done", "I can't handle this anymore", "life isn't worth it", "overwhelmed completely"
        ]

    def detect_risk(self, message):
        message_lower = message.lower()
        return any(kw in message_lower for kw in self.risk_keywords)

    def trigger_escalation(self):
        return (
            "⚠️ Critical concern detected. A qualified mental health professional will be notified. "
            "Please prioritize your well-being — you are not alone. We recommend reaching out to someone you trust "
            "or a licensed counselor immediately."
        )