from agents import (
    MentalHealthAgent,
    OrganizationalPsychologyAgent,
    HumanResourcesAgent,
    HumanEscalationHandler
)

class TriageAgent:
    """Classifies the user's message and routes to the appropriate GPT agent or human escalation."""
    def __init__(self, name):
        self.name = name
        self.escalation_handler = HumanEscalationHandler()

        # Routing keyword categories
        self.environment_keywords = [
            "team", "colleague", "manager", "office", "communication", "environment",
            "leadership", "conflict", "boss",
            "equipa", "colega", "chefe", "gestor", "ambiente", "comunicação", "liderança", "conflito"
        ]
        self.hr_keywords = [
            "schedule", "hours", "workload", "remote", "leave", "pay", "benefits",
            "vacation", "salary", "contract", "promotion", "transfer", "flexibility",
            "horário", "carga horária", "folga", "remoto", "salário", "contrato", "férias", "promoção", "reposição"
        ]

    def analyze_message(self, message):
        """Basic keyword classifier + safety guardrail escalation check."""
        if self.escalation_handler.detect_risk(message):
            return "escalate"
        message_lower = message.lower()

        if any(keyword in message_lower for keyword in self.environment_keywords):
            return "organizational_psychology"

        if any(keyword in message_lower for keyword in self.hr_keywords):
            return "hr"

        return "mental_health"

    def respond(self, message):
        """Returns a summary and the routed agent or an escalation message."""
        route = self.analyze_message(message)

        if route == "escalate":
            return self.escalation_handler.trigger_escalation(), None
        elif route == "mental_health":
            return "Routing to Mental Health Agent...", MentalHealthAgent()
        elif route == "organizational_psychology":
            return "Routing to Organizational Psychology Agent...", OrganizationalPsychologyAgent()
        elif route == "hr":
            return "Routing to Human Resources Agent...", HumanResourcesAgent()
