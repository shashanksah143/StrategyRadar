import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from tools.ranking_monitor import get_indian_organic_results
from utils.file_saver import save_output_file

# --- Configuration & Data Loading ---

def safe_load(path):
    try:
        return load_file_content(path)
    except Exception:
        return ""

# Load keywords
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'keywords.txt'))
keywords_list = safe_load(keywords_path)

# Load Instructions
base_instruction_text = safe_load("agents/rank_profiler/instructions.txt")
agent_description = safe_load("agents/rank_profiler/description.txt")

# Combine instructions with the keyword list
# We add a clear header so the LLM knows where the list starts
full_instruction_set = base_instruction_text + "\n\n*** TARGET KEYWORD LIST ***\n" + keywords_list

# --- Shared Configuration ---
gemini_config = Gemini(
    model="gemini-2.5-flash-lite", 
    retry_options=get_http_retry_config()
)

# Both tools are required for every agent
tools_list = [get_indian_organic_results, save_output_file]

# --- Define Agents ---

rank_agent_1 = LlmAgent(
    name="keyword_1_ranking_data", 
    model=gemini_config,
    instruction="You are a Rank Profiler. Analyze the 1st keyword.\n" + full_instruction_set,
    description=agent_description,
    tools=tools_list
)

rank_agent_2 = LlmAgent(
    name="keyword_2_ranking_data",
    model=gemini_config,
    instruction="You are a Rank Profiler. Analyze the 2nd keyword.\n" + full_instruction_set,
    description=agent_description,
    tools=tools_list
)

rank_agent_3 = LlmAgent(
    name="keyword_3_ranking_data",
    model=gemini_config,
    instruction="You are a Rank Profiler. Analyze the 3rd keyword.\n" + full_instruction_set,
    description=agent_description,
    tools=tools_list
)

rank_agent_4 = LlmAgent(
    name="keyword_4_ranking_data",
    model=gemini_config,
    instruction="You are a Rank Profiler. Analyze the 4th keyword.\n" + full_instruction_set,
    description=agent_description,
    tools=tools_list
)

rank_agent_5 = LlmAgent(
    name="keyword_5_ranking_data",
    model=gemini_config,
    instruction="You are a Rank Profiler. Analyze the 5th keyword.\n" + full_instruction_set,
    description=agent_description,
    tools=tools_list
)

# --- The Orchestrator ---

rank_profiler = ParallelAgent(
    name="rank_profiler",
    description="Orchestrates parallel SERP analysis for 5 target keywords.",
    sub_agents=[
        rank_agent_1,
        rank_agent_2,
        rank_agent_3,
        rank_agent_4,
        rank_agent_5
    ]
)

# Export
root_agent = rank_profiler