import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from google.adk.agents import SequentialAgent, ParallelAgent

# --- Import all your Root Agents ---
# (Assumes your agents are exported as 'root_agent' in their respective files)

from agents.content_alchemist.agent import root_agent as content_agent
from agents.rank_profiler.agent import root_agent as rank_agent
from agents.competitor_update_checker.agent import root_agent  as spy_agent
from agents.web_performance.agent import root_agent as perf_agent
from agents.competitor_analyst.agent import root_agent as analyst_agent

# --- PHASE 1: THE GATHERING SQUAD (Parallel) ---
# This agent groups the 4 data fetchers. It will not finish until ALL 4 are done.
data_gathering_squad = ParallelAgent(
    name="data_gathering_squad",
    description="Fetches Content, Rankings, Sitemaps, and Performance data simultaneously.",
    sub_agents=[
        content_agent,  # Analyzes Competitor Content (1-5) + Client Content
        rank_agent,     # Checks Rankings (1-5)
        spy_agent,      # Checks Sitemaps (1-5)
        perf_agent      # Checks Web Vitals
    ]
)

# --- PHASE 2: THE MASTER SEQUENCE (Sequential) ---
# This runs Phase 1, waits for completion, then runs Phase 2 (Analyst).
master_orchestrator = SequentialAgent(
    name="master_orchestrator",
    description="Executes the full SEO Audit pipeline: Gather Data -> Analyze Data.",
    sub_agents=[
        data_gathering_squad,  # Step 1: Run all fetchers in parallel
        analyst_agent          # Step 2: Run the analyst (accesses data from Step 1)
    ]
)

root_agent = master_orchestrator