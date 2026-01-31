import os
from abc import ABC, abstractmethod
from typing import List, Dict
from .models import AgentResponse, UserInput

# --- 1. Base Framework Class ---

class DecisionFramework(ABC):
    @abstractmethod
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        pass

# --- 2. Specific Framework Implementations ---

class SWOTAnalysis(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        return {
            "Strengths": ["Internal expertise", "Scalable infrastructure"],
            "Weaknesses": ["Budget constraints", "Limited historical data"],
            "Opportunities": ["Market expansion", "Automation potential"],
            "Threats": ["Competitor response", "Regulatory shifts"]
        }

class RICEScoring(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        return {
            "Reach": ["Estimated 5,000 users per month"],
            "Impact": ["High (3/3) for conversion rates"],
            "Confidence": ["80% based on recent surveys"],
            "Effort": ["2 person-months of engineering"]
        }

class FiveWhys(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        return {
            "Level 1 (Direct Cause)": ["Technical debt in the legacy module"],
            "Level 2": ["Lack of refactoring time in previous sprints"],
            "Level 3": ["Priority shifted to feature delivery over stability"],
            "Level 4": ["Quarterly targets prioritized short-term gains"],
            "Level 5 (Root Cause)": ["Alignment between sales targets and engineering health is missing"]
        }

class CostBenefitAnalysis(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        # In a real app, this logic would parse 'problem' to identify specific costs/benefits.
        # For the hackathon, we provide a robust, structured template.
        return {
            "Direct Costs": [
                "Initial implementation & technology acquisition",
                "Labor and specialized personnel expenses",
                "Software licensing or raw material costs"
            ],
            "Indirect & Intangible Costs": [
                "Opportunity cost of diverted resources",
                "Potential productivity dip during transition",
                "Maintenance and ongoing operational overhead"
            ],
            "Tangible Benefits (ROI)": [
                "Expected revenue increase or cost savings",
                "Reduction in manual error rates",
                "Faster time-to-market for core services"
            ],
            "Strategic & Intangible Benefits": [
                "Improved brand reputation and trust",
                "Enhanced employee morale and retention",
                "Increased agility to respond to market shifts"
            ]
        }

# --- 3. The Framework Registry ---

FRAMEWORK_REGISTRY = {
    "SWOT": SWOTAnalysis(),
    "RICE": RICEScoring(),
    "5WHYS": FiveWhys(),
    "COST_BENEFIT": CostBenefitAnalysis() # Ensure this key matches your HTML value!
}

# --- 4. The Core Engine ---

def run_decision_engine(data: UserInput) -> AgentResponse:
    problem_text = data.problem.strip()
    
    # Validation (Active Inquiry)
    if len(problem_text) < 25:
        return AgentResponse(
            status="needs_info",
            clarifying_questions=["Please provide more context regarding your primary goal."]
        )

    # Framework Selection Logic
    framework_key = data.framework.upper()
    
    if framework_key == "AUTO":
        # Simplified heuristic for auto-selection
        if "why" in problem_text.lower(): framework_key = "5WHYS"
        elif "feature" in problem_text.lower(): framework_key = "RICE"
        else: framework_key = "SWOT"

    # Execute the selected strategy
    analyzer = FRAMEWORK_REGISTRY.get(framework_key, SWOTAnalysis())
    analysis_results = analyzer.analyze(problem_text, data.assumptions)

    return AgentResponse(
        status="success",
        selected_framework=framework_key,
        structured_problem=f"Challenge: {problem_text}",
        framework_output=analysis_results,
        solution="Proceed with a focused pilot project to validate the highest impact assumptions.",
        execution_plan=["Define KPIs", "Run 2-week Sprint", "Review and Pivot"],
        clarifying_questions=[]
    )
