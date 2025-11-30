import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from tools.nlp_analyzer import analyze_content
from utils.file_saver import save_output_file

# --- Load Configuration ---
# Helper to safely load files
def safe_load(path):
    try:
        return load_file_content(path)
    except Exception:
        return ""

competitor_list = safe_load(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))
client_website_url = safe_load(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'client_url.txt')))

# Load the NEW instructions defined above
base_instruction = safe_load("agents/content_alchemist/instructions.txt") 
agent_description = safe_load("agents/content_alchemist/description.txt")

# Combine base instructions with the competitor list once
full_instruction_set = base_instruction + "\n\n*** COMPETITOR LIST ***\n" + competitor_list

# --- Define Agents ---

# Shared Model Configuration
gemini_config = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=get_http_retry_config()
)

# Shared Tools List (All agents need both tools now)
# NOTE: Ensure content_analyst_1 has the save tool!
tools_list = [analyze_content, save_output_file]

content_analyst_1 = LlmAgent(
    name="content_analyst_1",
    model=gemini_config,
    instruction="You are a Content Alchemist. Analyze the 1st competitor.\n" + full_instruction_set,
    description=agent_description,
    output_key="competitor_1_result",
    tools=tools_list 
)

content_analyst_2 = LlmAgent(
    name="content_analyst_2",
    model=gemini_config,
    instruction="You are a Content Alchemist. Analyze the 2nd competitor.\n" + full_instruction_set,
    description=agent_description,
    output_key="competitor_2_result",
    tools=tools_list
)

content_analyst_3 = LlmAgent(
    name="content_analyst_3",
    model=gemini_config,
    instruction="You are a Content Alchemist. Analyze the 3rd competitor.\n" + full_instruction_set,
    description=agent_description,
    output_key="competitor_3_result",
    tools=tools_list
)

content_analyst_4 = LlmAgent(
    name="content_analyst_4",
    model=gemini_config,
    instruction="You are a Content Alchemist. Analyze the 4th competitor.\n" + full_instruction_set,
    description=agent_description,
    output_key="competitor_4_result",
    tools=tools_list
)

content_analyst_5 = LlmAgent(
    name="content_analyst_5",
    model=gemini_config,
    instruction="You are a Content Alchemist. Analyze the 5th competitor.\n" + full_instruction_set,
    description=agent_description,
    output_key="competitor_5_result",
    tools=tools_list
)

content_analyst_for_our_website = LlmAgent(
    name="content_analyst_for_our_website",
    model=gemini_config,
    instruction=f"You are a Content Alchemist. Analyze the client website: {client_website_url}.\n" + base_instruction,
    description=agent_description,
    output_key="client_website_result",
    tools=tools_list
)

# --- The Orchestrator ---
content_alchemist = ParallelAgent(
    name="content_alchemist",
    description="Orchestrates parallel NLP content analysis and file saving.",
    sub_agents=[
        content_analyst_1,
        content_analyst_2,
        content_analyst_3,
        content_analyst_4,
        content_analyst_5,
        content_analyst_for_our_website
    ]
)

root_agent = content_alchemist