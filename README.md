# Dinta | Democratizing smart decision making

A decision intelligence tool powered by IBM watsonx Orchestrate that applies decision and strategy frameworks to user problems and produces executable plans.

## Project Structure
```
dinta
├── app.py
├── api/
│   ├── index.py            # Main FastAPI application entry point
│   ├── models.py           # Pydantic data models (Shared schema)
│   └── logic.py            # The core "Decision Intelligence" brain
├── templates/
│   ├── index.html          # Landing page
│   └── app.html            # Main application Interface
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
└── openapi.json            
```

## System Architecture
The system operates on a "Triangular" flow:

- Frontend (Vercel): Captures user intent and renders the results.

- Middleware/Logic (FastAPI): Acts as the "Guardrail" and "Parser." It ensures the data is clean before the AI sees it and structures the AI's response before the user sees it.

- IBM Orchestrate (The Hub): Manages the AI skills, maintains session context for the "Refinement Phase," and executes the specific decision frameworks.


