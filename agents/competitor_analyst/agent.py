import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.retry_config import get_http_retry_config
from utils.file_loader import load_file_content
from utils.file_saver import save_output_file

# Load Instructions
instruction_text = load_file_content("agents/competitor_analyst/instructions.txt")

# This agent does NOT need analysis tools (like sitemap fetcher or google search).
# It only needs the 'save_output_file' tool to write its final report.
# It relies on the CONTEXT provided by the Orchestrator (the outputs of previous agents).

competitor_analyst = LlmAgent(
    name="competitor_analyst",
    model=Gemini(
        model="gemini-2.5-pro", # Using Pro for better reasoning on large context
        retry_options=get_http_retry_config()
    ),
    instruction=instruction_text,
    description="Consolidates data from Rankings, Content, and Sitemaps into a final strategic report.",
    tools=[save_output_file]
)

root_agent = competitor_analyst