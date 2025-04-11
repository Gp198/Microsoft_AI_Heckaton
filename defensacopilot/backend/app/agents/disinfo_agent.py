# disinfo_agent.py
# ---------------------------------------------------------------
# Disinformation Agent - Simulates fact-checking of questionable claims
# This module is part of the DefensaCopilot agent system.
# ---------------------------------------------------------------

# agents/disinfo_agent.py

from semantic_kernel import KernelFunctionFromPrompt
from semantic_kernel.orchestration.kernel_context import KernelContext

# 🧠 Professional prompt to detect misinformation context
DISINFO_PROMPT = """
You are a specialized disinformation analyst focused on military and geopolitical topics.
Evaluate the following statement and determine if it shows signs of misinformation, disinformation, or propaganda.
Back your analysis with facts from verifiable sources.

Statement:
{{$input}}

Respond in a professional and concise manner, avoiding speculation or hallucinations.
"""

# ⬇️ Register disinfo agent as a semantic function
def get_disinfo_function(kernel) -> KernelFunctionFromPrompt:
    return kernel.create_function_from_prompt(
        function_name="DisinfoAnalysis",
        plugin_name="DisinfoAgent",
        prompt_template=DISINFO_PROMPT,
        description="Analyzes a statement for potential misinformation or propaganda."
    )
