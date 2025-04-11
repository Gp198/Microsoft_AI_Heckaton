# disinfo_agent.py
# ---------------------------------------------------------------
# Disinformation Agent - Simulates fact-checking of questionable claims
# This module is part of the DefensaCopilot agent system.
# ---------------------------------------------------------------

from semantic_kernel import Kernel

# Professional prompt with guardrails to reduce hallucinations
DISINFO_PROMPT = """
You are a defense and geopolitics expert. Analyze the following statement for signs of:
- misinformation
- disinformation
- propaganda

Statement:
{{$input}}

Respond only if relevant. Avoid speculation. Be concise and suggest ways to verify.
"""

# Function to register the disinformation analysis with the kernel
def get_disinfo_function(kernel: Kernel):
    return kernel.create_semantic_function(
        function_name="disinfo_analysis",
        plugin_name="DisinfoPlugin",
        prompt=DISINFO_PROMPT,
        description="Analyze a statement for possible disinformation or propaganda.",
        max_tokens=512,
        temperature=0.2,
        top_p=0.5
    )
