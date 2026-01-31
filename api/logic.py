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
class FirstPrinciplesThinking(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        # This framework focuses on stripping away analogies and "we've always done it this way" thinking.
        return {
            "Fundamental Truths": [
                "What are the physical or logical laws that cannot be broken here?",
                "What are the raw components or absolute requirements of this problem?",
                "Identify facts that are true regardless of industry 'best practices'."
            ],
            "Deconstructed Assumptions": [
                "Challenge: Why do we believe this specific constraint exists?",
                "Analogy Check: Are we just copying what someone else did?",
                "Is this a 'rule of nature' or just a 'shared belief'?"
            ],
            "Socratic Inquiries": [
                "If we started from scratch today with zero legacy, what would we build?",
                "What is the most basic version of this solution that still functions?",
                "How do the raw material costs compare to the finished product costs?"
            ],
            "Ground-Up Synthesis": [
                "Reassemble the basic elements into a non-linear solution.",
                "Combine fundamental truths in a way that ignores traditional industry boundaries."
            ]
        }

class PortersFiveForces(DecisionFramework):
    def analyze(self, problem: str, assumptions: str) -> Dict[str, List[str]]:
        # This framework evaluates the competitive environment and industry profit potential.
        return {
            "Competitive Rivalry": [
                "How many established players are currently in this space?",
                "Is the industry growing fast enough to sustain everyone, or is it a 'fight for share'?",
                "What is the level of product differentiation between you and rivals?"
            ],
            "Threat of New Entrants": [
                "How high are the barriers to entry (capital, patents, regulations)?",
                "Do existing players have massive economies of scale that protect them?",
                "How easy is it for a startup to access the same distribution channels?"
            ],
            "Bargaining Power of Suppliers": [
                "Are there only a few suppliers for your critical inputs?",
                "What is the cost of switching from one supplier to another?",
                "Could your suppliers potentially 'forward integrate' and become competitors?"
            ],
            "Bargaining Power of Buyers": [
                "How many customers do you have? (Fewer customers = higher buyer power)",
                "How sensitive are your buyers to price changes?",
                "Can your customers easily switch to a competitor's offering?"
            ],
            "Threat of Substitutes": [
                "Are there alternative products that solve the same problem in a different way?",
                "What is the price-performance trade-off of these substitutes?",
                "How high are the switching costs for a user to leave your category entirely?"
            ]
        }

# --- 3. The Framework Registry ---

FRAMEWORK_REGISTRY = {
    "SWOT": SWOTAnalysis(),
    "RICE": RICEScoring(),
    "5WHYS": FiveWhys(),
    "COST_BENEFIT": CostBenefitAnalysis(),
    "FIRST_PRINCIPLES": FirstPrinciplesThinking(),
    "PORTERS_FIVE": PortersFiveForces()
}



# --- 4. Engine Logic ---
def run_decision_engine(data: UserInput) -> AgentResponse:
    problem_text = data.problem.strip()
    user_choice = data.framework.upper() if data.framework else "AUTO"

    if user_choice == "AUTO":
        low_problem = problem_text.lower()
        if any(w in low_problem for w in ["market", "competitor", "industry", "rival"]):
            framework_key = "PORTERS_FIVE"
        elif any(w in low_problem for w in ["innovation", "scratch", "fundamental"]):
            framework_key = "FIRST_PRINCIPLES"
        elif any(w in low_problem for w in ["cost", "budget", "profit"]):
            framework_key = "COST_BENEFIT"
        else:
            framework_key = "SWOT"
    else:
        framework_key = user_choice

    analyzer = FRAMEWORK_REGISTRY.get(framework_key, SWOTAnalysis())
    analysis_results = analyzer.analyze(problem_text, data.assumptions)

    return AgentResponse(
        status="success",
        selected_framework=framework_key.replace("_", " ").title(),
        framework_output=analysis_results,
        solution="Focus on building unique differentiation or high switching costs to neutralize competitive forces.",
        execution_plan=[
            "Step 1: Identify the strongest force currently limiting your profitability.",
            "Step 2: Develop a defensive strategy to mitigate that specific force.",
            "Step 3: Explore ways to increase barriers to entry for your niche."
        ]
    )
