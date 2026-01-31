import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .models import UserInput, AgentResponse
from .logic import run_decision_engine

app = FastAPI()

# IMPORTANT: CORS must be here for IBM Orchestrate to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Page Routes (Replaces @app.route from Flask)
@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/app")
async def serve_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

# API Route for IBM Orchestrate
@app.post("/api/analyze", response_model=AgentResponse)
async def analyze(data: UserInput):
    return run_decision_engine(data)
