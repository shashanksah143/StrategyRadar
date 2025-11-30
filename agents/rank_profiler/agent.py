import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from tools.ranking_monitor import get_indian_organic_results


# Load the list of keywords
keywords_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'keywords.txt')))
base_instruction = load_file_content("agents/rank_profiler/instructions.txt") + + keywords_list
agent_description = load_file_content("agents/rank_profiler/description.txt")

rank_agent_1 = LlmAgent(
    name="keyword_1_ranking_data", 
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Rank Profiler. Analyze the 1st keyword." + base_instruction ,
    description=agent_description,
    tools=[get_indian_organic_results]
)

rank_agent_2 = LlmAgent(
    name="keyword_2_ranking_data",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Rank Profiler. Analyze the 2nd keyword." + base_instruction ,
    description=agent_description,
    tools=[get_indian_organic_results]
)

rank_agent_3 = LlmAgent(
    name="keyword_3_ranking_data",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Rank Profiler. Analyze the 3rd keyword." + base_instruction,
    description=agent_description,
    tools=[get_indian_organic_results]
)

rank_agent_4 = LlmAgent(
    name="keyword_4_ranking_data",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Rank Profiler. Analyze the 4th keyword." + base_instruction,
    description=agent_description,
    tools=[get_indian_organic_results]
)

rank_agent_5 = LlmAgent(
    name="keyword_5_ranking_data",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Rank Profiler. Analyze the 5th keyword." + base_instruction,
    description=agent_description,
    tools=[get_indian_organic_results]
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

# Export as root_agent if this is the entry point, or import 'rank_profiler' elsewhere
root_agent = rank_profiler