import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from tools.nlp_analyzer import analyze_content


# Load the list of competitors
competitor_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))
client_website_url = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'client_url.txt')))
base_instruction = load_file_content("agents/content_alchemist/instructions.txt")+ competitor_list
agent_description = load_file_content("agents/content_alchemist/description.txt")

# Define the 5 parallel sub-agents
content_analyst_1 = LlmAgent(
    name="content_analyst_1",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the 1st competitor." + base_instruction,
    description=agent_description,
    output_key="competitor_1_content_data",
    tools=[analyze_content]
)

content_analyst_2 = LlmAgent(
    name="content_analyst_2",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the 2nd competitor." + base_instruction,
    description=agent_description,
    output_key="competitor_2_content_data",
    tools=[analyze_content]
)

content_analyst_3 = LlmAgent(
    name="content_analyst_3",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the 3rd competitor." + base_instruction,
    description=agent_description,
    output_key="competitor_3_content_data",
    tools=[analyze_content]
)

content_analyst_4 = LlmAgent(
    name="content_analyst_4",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the 4th competitor." + base_instruction,
    description=agent_description,
    output_key="competitor_4_content_data",
    tools=[analyze_content]
)

content_analyst_5 = LlmAgent(
    name="content_analyst_5",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the 5th competitor." + base_instruction,
    description=agent_description,
    output_key="competitor_5_content_data",
    tools=[analyze_content]
)


content_analyst_for_our_website = LlmAgent(
    name="content_analyst_for_our_website",
     model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=get_http_retry_config()
    ),
    instruction="You are a Content Alchemist. Analyze the `" + client_website_url + "`." + base_instruction,
    description=agent_description,
    output_key="content_analyst_for_our_website",
    tools=[analyze_content]
)

# The Orchestrator
content_alchemist = ParallelAgent(
    name="content_alchemist",
    description="Orchestrates parallel NLP content analysis (TF-IDF & N-Grams) of 5 competitors.",
    sub_agents=[
        content_analyst_1,
        content_analyst_2,
        content_analyst_3,
        content_analyst_4,
        content_analyst_5,
        content_analyst_for_our_website
    ]
)

# Export as root_agent
root_agent = content_alchemist