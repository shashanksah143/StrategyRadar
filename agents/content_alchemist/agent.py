import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent, ParallelAgent
from utils.file_loader import load_file_content
from tools.nlp_analyzer import analyze_competitors_content

# Load the list of competitors
competitor_list = load_file_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'data', 'competitor_url.txt')))

# Define the 5 parallel sub-agents
content_analyst_1 = LlmAgent(
    name="content_analyst_1",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the 1st competitor." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="competitor_1_content_data",
    tools=[analyze_competitors_content]
)

content_analyst_2 = LlmAgent(
    name="content_analyst_2",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the 2nd competitor." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="competitor_2_content_data",
    tools=[analyze_competitors_content]
)

content_analyst_3 = LlmAgent(
    name="content_analyst_3",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the 3rd competitor." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="competitor_3_content_data",
    tools=[analyze_competitors_content]
)

content_analyst_4 = LlmAgent(
    name="content_analyst_4",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the 4th competitor." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="competitor_4_content_data",
    tools=[analyze_competitors_content]
)

content_analyst_5 = LlmAgent(
    name="content_analyst_5",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the 5th competitor." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="competitor_5_content_data",
    tools=[analyze_competitors_content]
)


content_analyst_for_our_website = LlmAgent(
    name="content_analyst_for_our_website",
    model="gemini-2.5-flash",
    instruction="You are a Content Alchemist. Analyze the `https://www.weddingbiodata.in`." + load_file_content("agents/content_alchemist/instructions.txt") + competitor_list,
    description=load_file_content("agents/content_alchemist/description.txt"),
    output_key="content_analyst_for_our_website",
    tools=[analyze_competitors_content]
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