import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from tools.sitemap_fetcher import fetch_competitor_sitemap
from utils.file_saver import save_output_file # Added for consistency

# Load data
competitor_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))
base_instruction = load_file_content("agents/competitor_update_checker/instructions.txt") + "\n\n" + competitor_list
agent_description = load_file_content("agents/competitor_update_checker/description.txt")

# Define tools
tools_list = [fetch_competitor_sitemap, save_output_file]

# Define Agents
sitemap_analyzer_1 = LlmAgent(
    name="sitemap_analyzer_1",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Competitor Intelligence Agent. Analyze the 1st competitor's sitemap. Save the result to a file named 'sitemap_1.json'." + base_instruction,
    description=agent_description,
    output_key="competitor_1_sitemap_data",
    tools=tools_list
)

sitemap_analyzer_2 = LlmAgent(
    name="sitemap_analyzer_2",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Competitor Intelligence Agent. Analyze the 2nd competitor's sitemap. Save the result to a file named 'sitemap_2.json'." + base_instruction,
    description=agent_description,
    output_key="competitor_2_sitemap_data",
    tools=tools_list
)

sitemap_analyzer_3 = LlmAgent(
    name="sitemap_analyzer_3",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Competitor Intelligence Agent. Analyze the 3rd competitor's sitemap. Save the result to a file named 'sitemap_3.json'." + base_instruction,
    description=agent_description,
    output_key="competitor_3_sitemap_data",
    tools=tools_list
)

sitemap_analyzer_4 = LlmAgent(
    name="sitemap_analyzer_4",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Competitor Intelligence Agent. Analyze the 4th competitor's sitemap. Save the result to a file named 'sitemap_4.json'." + base_instruction,
    description=agent_description,
    output_key="competitor_4_sitemap_data",
    tools=tools_list
)

sitemap_analyzer_5 = LlmAgent(
    name="sitemap_analyzer_5",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction="You are a Competitor Intelligence Agent. Analyze the 5th competitor's sitemap. Save the result to a file named 'sitemap_5.json'." + base_instruction,
    description=agent_description,
    output_key="competitor_5_sitemap_data",
    tools=tools_list
)

competitor_spy = ParallelAgent(
    name="competitor_spy",
    description="Orchestrates the parallel analysis of 5 competitor sitemaps.",
    sub_agents=[
        sitemap_analyzer_1, 
        sitemap_analyzer_2, 
        sitemap_analyzer_3, 
        sitemap_analyzer_4, 
        sitemap_analyzer_5
    ]
)

root_agent = competitor_spy