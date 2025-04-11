# planner.py
# This module sets up and executes a FunctionCallingStepwisePlanner using Semantic Kernel v1.28.0

import semantic_kernel as sk
from semantic_kernel.planners import FunctionCallingStepwisePlanner
from semantic_kernel.kernel import Kernel

# === Initialize the planner ===
def initialize_planner(kernel: Kernel) -> FunctionCallingStepwisePlanner:
    """
    Initializes the FunctionCallingStepwisePlanner using the provided kernel.

    Args:
        kernel (Kernel): The configured Semantic Kernel instance.

    Returns:
        FunctionCallingStepwisePlanner: A planner ready to create and execute plans.
    """
    return FunctionCallingStepwisePlanner(kernel)

# === Plan and run the user's request ===
async def plan_and_run(kernel: Kernel, user_input: str) -> str:
    """
    Creates and executes a plan based on user input using Semantic Kernel planner.

    Args:
        kernel (Kernel): The configured Semantic Kernel instance.
        user_input (str): The natural language instruction from the user.

    Returns:
        str: The final result from the planner execution or an error message.
    """
    try:
        # Create planner instance
        planner = initialize_planner(kernel)

        # Generate plan based on user input
        plan = await planner.create_plan_async(user_input)

        # Execute the generated plan
        result = await planner.execute_plan_async(plan)

        return str(result)

    except Exception as e:
        return f"❌ Planner failed: {e}"
