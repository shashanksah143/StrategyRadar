import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from utils.file_loader import load_file_content
from tools.sitemap_fetcher import fetch_competitor_sitemap
from utils.file_loader import load_file_content

competitor_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))

sitemap_analyzer_1 = LlmAgent(
    name="sitemap_analyzer_1",
    model="gemini-2.5-flash", 
    instruction="You are a Competitor Intelligence Agent You will analyze only the 1st competitor's sitemap." + load_file_content("agents/competitor_spy/instructions.txt") + competitor_list,
    description=load_file_content("agents/competitor_spy/description.txt"),
    output_key="competitor_1_sitemap_data", # This puts the result in memory for other agents
    tools=[fetch_competitor_sitemap]
)

sitemap_analyzer_2 = LlmAgent(
    name="sitemap_analyzer_2",
    model="gemini-2.5-flash", 
    instruction="You are a Competitor Intelligence Agent You will analyze only the 2nd competitor's sitemap." + load_file_content("agents/competitor_spy/instructions.txt") + competitor_list,
    description=load_file_content("agents/competitor_spy/description.txt"),
    output_key="competitor_2_sitemap_data", # This puts the result in memory for other agents
    tools=[fetch_competitor_sitemap]
)

sitemap_analyzer_3 = LlmAgent(
    name="sitemap_analyzer_3",
    model="gemini-2.5-flash", 
    instruction="You are a Competitor Intelligence Agent You will analyze only the 3rd competitor's sitemap." + load_file_content("agents/competitor_spy/instructions.txt") + competitor_list,
    description=load_file_content("agents/competitor_spy/description.txt"),
    output_key="competitor_3_sitemap_data", # This puts the result in memory for other agents
    tools=[fetch_competitor_sitemap]
)

sitemap_analyzer_4 = LlmAgent(
    name="sitemap_analyzer_4",
    model="gemini-2.5-flash", 
    instruction="You are a Competitor Intelligence Agent You will analyze only the 4th competitor's sitemap." + load_file_content("agents/competitor_spy/instructions.txt") + competitor_list,
    description=load_file_content("agents/competitor_spy/description.txt"),
    output_key="competitor_4_sitemap_data", # This puts the result in memory for other agents
    tools=[fetch_competitor_sitemap]
)

sitemap_analyzer_5 = LlmAgent(
    name="sitemap_analyzer_5",
    model="gemini-2.5-flash", 
    instruction="You are a Competitor Intelligence Agent You will analyze only the 5th competitor's sitemap." + load_file_content("agents/competitor_spy/instructions.txt") + competitor_list,
    description=load_file_content("agents/competitor_spy/description.txt"),
    output_key="competitor_5_sitemap_data", # This puts the result in memory for other agents
    tools=[fetch_competitor_sitemap]
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