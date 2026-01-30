# Dinta | Democratizing smart decision making

A decision intelligence tool powered by IBM watsonx Orchestrate that applies decision and strategy frameworks to user problems and produces executable plans.

## Implementation
- **Backend**: Flask (Python)
- **Frontend**: Native JavaScript and CSS Grid, ensuring a lightweight, secure, and responsive institutional experience.
- **Agentic Workdlow**: IBM Wastson Orchestrate.

## Project Structure
```
dinta/
├── app.py              
├── requirements.txt  
├── vercel.json   
├── README.md                 
└── templates/
    ├── index.html
    ├── app.html
    ├── 404.html
```

## IBM Waston Orchestrate Architecture
```
Browser (app.html)
        ↓
Flask API (app.py)
        ↓
watsonx Orchestrate Workflow (HTTP trigger)
        ↓
5 Orchestrate LLM Skills (sequential reasoning)
        ↓
watsonx.ai foundation model
        ↓
Structured JSON result
        ↓
Back to Flask → UI render
```

## Installation and Deployment
### Environmental Setup
```
pip install -r requirements.txt
```
### Application Launch
```
python app.py
```
