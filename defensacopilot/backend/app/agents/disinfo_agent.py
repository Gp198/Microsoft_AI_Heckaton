# disinfo_agent.py
# ---------------------------------------------------------------
# Disinformation Agent - Simulates fact-checking of questionable claims
# This module is part of the DefensaCopilot agent system.
# ---------------------------------------------------------------

# agents/disinfo_agent.py

from semantic_kernel import Kernel
from semantic_kernel.contents import PromptTemplateConfig, PromptTemplate
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.prompt_template.prompt_template_engine import PromptTemplateEngine
from semantic_kernel.semantic_function import SemanticFunction
from semantic_kernel.orchestration.kernel_context import KernelContext

# 🧠 Prompt for disinformation analysis
DISINFO_PROMPT = """
You are an expert in detecting disinformation in defense and geopolitical contexts.
Analyze the following statement and indicate if it might be misinformation, disinformation, or propaganda.

Statement:
{{$input}}

Provide reasoning and suggest how to verify or refute the claim. Avoid speculation or hallucinations.
"""

# ✅ Return a SemanticFunction that can be registered to the kernel
def get_disinfo_function(kernel: Kernel) -> SemanticFunction:
    prompt_config = PromptTemplateConfig(
        name="disinfo_analysis",
        description="Analyzes if a statement contains disinformation.",
        template=DISINFO_PROMPT,
        template_format="semantic-kernel",
        input_variables=[{"name": "input", "description": "Statement to analyze", "is_required": True}]
    )

    prompt_template = PromptTemplate(
        config=prompt_config,
        template_engine=PromptTemplateEngine()
    )

    return SemanticFunction(
        prompt_template=prompt_template,
        kernel=kernel
    )
