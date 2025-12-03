import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content, get_item_by_position
from tools.sitemap_fetcher import fetch_competitor_sitemap
from utils.file_saver import save_output_file
from agents.competitor_update_checker.output_models import CompetitorUpdateCheckerOutput

# Load data
competitor_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))
instruction_template = load_file_content("agents/competitor_update_checker/instructions.txt")
agent_description = load_file_content("agents/competitor_update_checker/description.txt")

# Define tools
tools_list = [fetch_competitor_sitemap, save_output_file]

# Extract competitor URLs
competitor_url_1 = get_item_by_position(competitor_list, 1) or "competitor_1"
competitor_url_2 = get_item_by_position(competitor_list, 2) or "competitor_2"
competitor_url_3 = get_item_by_position(competitor_list, 3) or "competitor_3"
competitor_url_4 = get_item_by_position(competitor_list, 4) or "competitor_4"
competitor_url_5 = get_item_by_position(competitor_list, 5) or "competitor_5"

# Define Agents
sitemap_analyzer_1 = LlmAgent(
    name="sitemap_analyzer_1",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction=instruction_template.format(
        competitor_url=competitor_url_1,
        filename="competitor_update_{competitor_url_1.replace('/', '_').replace(':', '').replace('.', '_')}"
    ),
    description=agent_description,
    output_key="competitor_1_sitemap_data",
    output_schema=CompetitorUpdateCheckerOutput,
    tools=tools_list
)

sitemap_analyzer_2 = LlmAgent(
    name="sitemap_analyzer_2",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction=instruction_template.format(
        competitor_url=competitor_url_2,
        filename="competitor_update_{competitor_url_2.replace('/', '_').replace(':', '').replace('.', '_')}"
    ),
    description=agent_description,
    output_key="competitor_2_sitemap_data",
    output_schema=CompetitorUpdateCheckerOutput,
    tools=tools_list
)

sitemap_analyzer_3 = LlmAgent(
    name="sitemap_analyzer_3",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction=instruction_template.format(
        competitor_url=competitor_url_3,
        filename="competitor_update_{competitor_url_3.replace('/', '_').replace(':', '').replace('.', '_')}"
    ),
    description=agent_description,
    output_key="competitor_3_sitemap_data",
    output_schema=CompetitorUpdateCheckerOutput,
    tools=tools_list
)

sitemap_analyzer_4 = LlmAgent(
    name="sitemap_analyzer_4",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction=instruction_template.format(
        competitor_url=competitor_url_4,
        filename="competitor_update_{competitor_url_4.replace('/', '_').replace(':', '').replace('.', '_')}"
    ),
    description=agent_description,
    output_key="competitor_4_sitemap_data",
    output_schema=CompetitorUpdateCheckerOutput,
    tools=tools_list
)

sitemap_analyzer_5 = LlmAgent(
    name="sitemap_analyzer_5",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=get_http_retry_config()),
    instruction=instruction_template.format(
        competitor_url=competitor_url_5,
        filename="competitor_update_{competitor_url_5.replace('/', '_').replace(':', '').replace('.', '_')}"
    ),
    description=agent_description,
    output_key="competitor_5_sitemap_data",
    output_schema=CompetitorUpdateCheckerOutput,
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