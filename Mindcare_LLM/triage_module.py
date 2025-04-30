from agents import (
    MentalHealthAgent,
    OrganizationalPsychologyAgent,
    HumanResourcesAgent,
    HumanEscalationHandler
)

class TriageAgent:
    """Classifies the user's message and routes it to the appropriate agent."""
    def __init__(self, name):
        self.name = name
        self.escalation_handler = HumanEscalationHandler()

        # Define keyword categories for intelligent routing
        self.environment_keywords = [
            "team", "colleague", "manager", "office", "communication", "environment",
            "leadership", "conflict", "boss"
        ]
        self.hr_keywords = [
            "schedule", "hours", "workload", "remote", "leave", "pay", "benefits",
            "vacation", "salary", "contract", "promotion", "transfer", "flexibility"
        ]

    def analyze_message(self, message):
        """Basic classifier using keywords and safety escalation handler."""
        if self.escalation_handler.detect_risk(message):
            return "escalate"
        message_lower = message.lower()

        # Keyword-based routing (environmental)
        if any(keyword in message_lower for keyword in self.environment_keywords):
            return "organizational_psychology"

        # Keyword-based routing (HR-related)
        if any(keyword in message_lower for keyword in self.hr_keywords):
            return "hr"

        # Default to emotional/mental health
        return "mental_health"

    def respond(self, message):
        """Returns routing summary and the selected agent (or escalation message)."""
        route = self.analyze_message(message)

        if route == "escalate":
            return self.escalation_handler.trigger_escalation(), None
        elif route == "mental_health":
            return "Routing to Mental Health Agent...", MentalHealthAgent()
        elif route == "organizational_psychology":
            return "Routing to Organizational Psychology Agent...", OrganizationalPsychologyAgent()
        elif route == "hr":
            return "Routing to Human Resources Agent...", HumanResourcesAgent()