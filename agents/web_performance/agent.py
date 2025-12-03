import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from utils.file_saver import save_output_file
from tools.web_vitals_fetcher import analyze_web_vitals
from agents.web_performance.output_models import WebPerformanceOutput

# Load Instructions
instruction_text = load_file_content("agents/web_performance/instructions.txt")
description_text = load_file_content("agents/web_performance/description.txt")

performace_reporter_agent = LlmAgent(
    name="performace_reporter_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=get_http_retry_config()
    ),
    instruction=instruction_text,
    description=description_text,
    output_key="performace_reporter_output", # The Analyst will look for this key
    output_schema=WebPerformanceOutput,  # Structured output schema for Google ADK LLM
    tools=[analyze_web_vitals, save_output_file]
)

root_agent = performace_reporter_agent