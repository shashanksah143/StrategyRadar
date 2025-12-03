import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content, get_item_by_position
from tools.ranking_monitor import get_indian_organic_results
from utils.file_saver import save_output_file
from agents.rank_profiler.output_models import RankProfilerOutput

# --- Configuration & Data Loading ---

def safe_load(path):
    try:
        return load_file_content(path)
    except Exception:
        return ""

# Load keywords
keywords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'keywords.txt'))
keywords_list = safe_load(keywords_path)

# Load Instructions (using simplified version to avoid LLM confusion)
instruction_template = safe_load("agents/rank_profiler/instructions.txt")
agent_description = safe_load("agents/rank_profiler/description.txt")

# --- Shared Configuration ---
gemini_config = Gemini(
    model="gemini-2.5-flash-lite", 
    retry_options=get_http_retry_config()
)

# Both tools are required for every agent
tools_list = [get_indian_organic_results, save_output_file]

# --- Define Agents with Output Schema ---

# Extract keywords for reference
keyword_1 = get_item_by_position(keywords_list, 1) or "keyword_1"
keyword_2 = get_item_by_position(keywords_list, 2) or "keyword_2"
keyword_3 = get_item_by_position(keywords_list, 3) or "keyword_3"
keyword_4 = get_item_by_position(keywords_list, 4) or "keyword_4"
keyword_5 = get_item_by_position(keywords_list, 5) or "keyword_5"

rank_agent_1 = LlmAgent(
    name="keyword_1_ranking_data", 
    model=gemini_config,
    instruction=instruction_template.format(keyword=keyword_1, keywords_list=keywords_list),
    description=agent_description,
    output_schema=RankProfilerOutput,
    tools=tools_list
)

rank_agent_2 = LlmAgent(
    name="keyword_2_ranking_data",
    model=gemini_config,
    instruction=instruction_template.format(keyword=keyword_2, keywords_list=keywords_list),
    description=agent_description,
    output_schema=RankProfilerOutput,
    tools=tools_list
)

rank_agent_3 = LlmAgent(
    name="keyword_3_ranking_data",
    model=gemini_config,
    instruction=instruction_template.format(keyword=keyword_3, keywords_list=keywords_list),
    description=agent_description,
    output_schema=RankProfilerOutput,
    tools=tools_list
)

rank_agent_4 = LlmAgent(
    name="keyword_4_ranking_data",
    model=gemini_config,
    instruction=instruction_template.format(keyword=keyword_4, keywords_list=keywords_list),
    description=agent_description,
    output_schema=RankProfilerOutput,
    tools=tools_list
)

rank_agent_5 = LlmAgent(
    name="keyword_5_ranking_data",
    model=gemini_config,
    instruction=instruction_template.format(keyword=keyword_5, keywords_list=keywords_list),
    description=agent_description,
    output_schema=RankProfilerOutput,
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