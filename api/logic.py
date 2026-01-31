import os
from .models import AgentResponse, UserInput

def run_decision_engine(data: UserInput) -> AgentResponse:
    """
    The core brain of the Dinta Agent.
    Validates input, selects frameworks, and generates the strategy.
    """
    problem_text = data.problem.strip()
    assumptions_text = data.assumptions.strip() if data.assumptions else "None provided"

    # 1. ACTIVE INQUIRY: Validation Loop
    # If the input is too brief, we trigger the 'needs_info' status.
    if len(problem_text) < 25:
        return AgentResponse(
            status="needs_info",
            clarifying_questions=[
                "Could you provide more detail on the specific goal?",
                "Are there any timeline or budget constraints I should know about?",
                "Who are the primary stakeholders affected by this decision?"
            ]
        )

    # 2. FRAMEWORK SELECTION
    # If the user chose 'auto', we use simple keyword heuristics.
    # In a real-world scenario, you would use an LLM call here to categorize the problem.
    selected_framework = data.framework
    
    if selected_framework == "auto":
        low_problem = problem_text.lower()
        if any(w in low_problem for w in ["competitor", "market", "threat", "rival"]):
            selected_framework = "Porter's Five Forces"
        elif any(w in low_problem for w in ["cost", "budget", "roi", "price"]):
            selected_framework = "Cost-Benefit Analysis"
        elif any(w in low_problem for w in ["feature", "product", "priority", "user"]):
            selected_framework = "RICE Scoring"
        else:
            selected_framework = "SWOT Analysis"

    # 3. STRATEGY GENERATION (Mock Logic)
    # This is where you would call the IBM Orchestrate SDK or Watsonx.ai
    # For now, we return a structured mock that matches your UI requirements.
    
    framework_data = {
        "Analysis Point 1": [f"Evaluation of {problem_text[:20]}... based on {selected_framework}."],
        "Key Assumption": [f"Verified: {assumptions_text[:30]}..."]
    }

    # Example: If SWOT was picked, structure the output specifically for the UI Grid
    if "SWOT" in selected_framework:
        framework_data = {
            "Strengths": ["Internal expertise", "Existing infrastructure"],
            "Weaknesses": ["Limited documentation", "Tight deadline"],
            "Opportunities": ["Market expansion", "Automation potential"],
            "Threats": ["Changing regulations", "High competition"]
        }

    return AgentResponse(
        status="success",
        selected_framework=selected_framework,
        structured_problem=f"Challenge: {problem_text}\n\nAssumptions: {assumptions_text}",
        framework_output=framework_data,
        solution="Implement a phased rollout starting with a Minimum Viable Product (MVP) to gather real-world data before full commitment.",
        execution_plan=[
            "Phase 1: Validation & Stakeholder Alignment",
            "Phase 2: Technical Pilot & Feedback Loop",
            "Phase 3: Scale & Full Implementation"
        ],
        clarifying_questions=[]
    )
