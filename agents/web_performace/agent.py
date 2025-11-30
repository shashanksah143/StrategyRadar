import os
import sys

# Add the project root to sys.path before importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent
from utils.file_loader import load_file_content
from utils.file_saver import save_output_file
from tools.web_vitals_fetcher import analyze_web_vitals

performace_reporter_agent = LlmAgent(
    name="performace_reporter_agent",
    model="gemini-2.5-flash",
    instruction=load_file_content("agents/web_performace/instructions.txt"),
    description=load_file_content("agents/web_performace/description.txt"),
    output_key="performace_reporter_output",
    tools=[analyze_web_vitals,save_output_file]
)

# Export as root_agent for ADK web server
root_agent = performace_reporter_agent