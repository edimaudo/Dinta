Question 1: Written problem and solution statement
Describe your project in 500 words or less. Include the specific problem or challenge that your solution is designed to address. Describe what your solution is, including target users, how they would interact with the solution, and why the solution is creative and unique. Provide clear details on how your project uses agentic AI to effectively and efficiently address the stated issue in a new way the judges have never seen before.

The Problem 
Small business owners and startup founders often suffer from "analysis paralysis.". When faced with challenges such as fluctuating market demands or scaling operations, they usually rely on "gut feel" or informal advice. Traditional consulting is prohibitively expensive, and static business templates are too rigid to adapt to the specific nuances of their business. They need a way to apply professional-grade strategic rigor without the overhead of a consultant.

The Solution
Dinta is an AI-powered decision architect designed for small business owners and entrepreneurs. It transforms raw business challenges into structured, actionable execution plans using world-class mental models like First Principles Thinking, Porter’s Five Forces, and Cost-Benefit Analysis.

User Experience
Users interact with Dinta via a streamlined interface where they describe their current challenge and relevant assumptions. What makes Dinta unique is its Adaptive Reasoning Engine. Instead of forcing a one-size-fits-all approach, it can analyzes the linguistic intent of the user’s input and dynamically suggest a framework or the user can also select the framework that best fits the business problem.

Agentic Design
Dinta utilizes agentic AI to move beyond simple text generation. Unlike standard chatbots that provide generic business advice, the agent acts as a Strategic Consultant. It evaluates the user's input, determines if sufficient information exists to perform a high-quality analysis, and it can autonomously selects from a library of specialized frameworks. By deconstructing the problem into its fundamental truths and building an execution plan from the ground up, the agent provides a level of structural rigor previously unavailable to small-scale operations. It doesn't just discuss a problem; it architecturally solves it.


Question 2: Written statement on agentic AI and IBM watsonx Orchestrate usage in your project
Provide clear and specific details on how and where your project uses agentic AI and IBM watsonx Orchestrate. Be specific about what agent(s) your solution uses, what each agent does, and how each agent works together within the context of the overall solution.

This project leverages IBM watsonx Orchestrate as the primary command center for the agentic workflow. The core logic is hosted as a custom API on Vercel, which is then imported into Orchestrate using an OpenAPI 3.0 specification.

The Orchestrator (IBM watsonx Orchestrate): The agent serves as the user-facing interface and traffic controller. It receives the user’s natural language input (business question) and coordinates the execution of specialized skills based on the user's intent.

The Decision Engine Agent (Dinta Decision Agent): This is the "brain" of the solution. When triggered by Orchestrate, this agent performs three distinct tasks:
- Intent Recognition: It scans the problem for keywords to decide which "mental model" skill to apply (e.g., identifying "cost" or "profit" triggers a Cost-Benefit Analysis).
- Strategic Decomposition: It populates the selected framework with specific, non-generic data points derived from the small business owner's unique situation.
- Action Synthesis: It generates a multi-step execution plan, translating high-level strategy into immediate operational tasks like "Step 1: Finalize budget" or "Step 2: Review ROI".

This is how they all work together.  The user speaks to the Orchestrator, which recognizes the intent to "Analyze a business problem." Orchestrate then calls our Decision Engine skill, passing the problem and assumptions as parameters. The Decision Engine processes the logic and returns a structured JSON payload. Orchestrate then renders this data into a professional dashboard for the user, ensuring a seamless transition from a messy business problem to a clean, structured strategy.
