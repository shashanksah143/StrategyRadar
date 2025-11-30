# SEO Audit & Competitor Intelligence System

An intelligent multi-agent system that performs comprehensive SEO analysis and competitive intelligence gathering using Google's Agent Development Kit (ADK) and Gemini AI models.

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Agents Overview](#agents-overview)
- [Agent Workflow](#agent-workflow)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [ADK Web Interface](#adk-web-interface)
- [Output Structure](#output-structure)
- [Technologies Used](#technologies-used)

---

## Project Overview

This project is an **SEO Analysis & Competitive Intelligence Platform** designed to:

1. **Monitor Search Rankings**: Track your website and competitors' positions for target keywords on Google India
2. **Analyze Content**: Perform NLP analysis on competitor and client websites to identify content gaps and topic strategies
3. **Track Competitor Updates**: Monitor competitor sitemaps to understand their update frequency and content velocity
4. **Assess Web Performance**: Evaluate technical health metrics (Core Web Vitals, performance scores)
5. **Generate Strategic Reports**: Synthesize all collected data into actionable insights and recommendations

The system is built for the **biodata/matrimonial website niche**, analyzing 5 target keywords against 5 main competitors while also evaluating the client's website.

### Report Type: Daily Competitive Intelligence & SEO Strategic Report

This system generates a **"Daily Competitive Intelligence & SEO Strategic Report"** - a comprehensive, multi-dimensional intelligence brief that goes far beyond traditional L3 matrices. Rather than simple ranking checklists, this report:

- **Synthesizes 5 data sources** into correlated insights
- **Identifies root causes** (e.g., "Poor rankings due to technical performance bottleneck")
- **Recommends specific actions** with business impact
- **Tracks competitor velocity** and market positioning shifts
- **Analyzes content gaps** using AI-powered NLP
- **Targets multi-stakeholder audiences** (C-level, product, marketing, technical teams)

**Key Difference from L3 Matrix**: Traditional L3 matrices show keyword rankings in a table format for execution teams. This report connects rankings to technical issues, content gaps, and competitor strategies, then prioritizes 3 specific action items for decision-makers.

### Use Cases & Stakeholder Value

| Stakeholder             | Value Delivered                                                                                |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| **C-Level Executives**  | Daily market positioning brief, strategic threats & opportunities, ROI-focused recommendations |
| **Product Managers**    | Competitive feature gaps, market velocity trends, product roadmap impact                       |
| **Content Strategists** | Content gap analysis, topic opportunities, competitor content velocity                         |
| **SEO Specialists**     | Detailed technical audits, ranking analysis, actionable optimization tickets                   |
| **Engineering Teams**   | Performance bottlenecks, Core Web Vitals assessment, technical priorities                      |
| **Marketing Directors** | Competitive benchmarking, market share insights, campaign impact data                          |

---

## System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│           MASTER ORCHESTRATOR (Sequential Agent)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
   PHASE 1: DATA GATHERING         PHASE 2: ANALYSIS & MONITORING
   (Parallel Execution)           (Sequential & Continuous)
        │                             │
        ├─ Content Alchemist          │
        │  ├─ Competitor 1-5          ├─ Competitor Analyst
        │  └─ Client Website          │  (Synthesizes to report)
        │                             │
        ├─ Rank Profiler              ├─ Google Update Analyst
        │  ├─ Keyword 1-5             │  (Monitors updates)
        │  └─ (Google SERP data)      │
        │                             ├─ Competitor Analyst
        ├─ Competitor Update Checker  │  (Final report generation)
        │  ├─ Sitemap 1-5             │
        │  └─ (Update frequency)      │
        │                             │
        └─ Web Performance Analyzer   │
           └─ (Core Web Vitals)       │
                                      │
                ┌─────────────────────┘
                │
        ┌───────▼────────────┐
        │ Final Report       │
        │ (Multi-layer       │
        │  Intelligence)     │
        └────────────────────┘
```

---

## Agents Overview

### 1. **Content Alchemist** 🧪

**Type**: Parallel Agent (6 sub-agents)

**Responsibility**: NLP content analysis using TF-IDF and n-gram extraction

**Sub-Agents**:

- `content_analyst_1` to `content_analyst_5`: Analyze each of the 5 competitors
- `content_analyst_for_our_website`: Analyze the client's website

**Tools Used**:

- `analyze_content`: Fetches HTML, cleans text, extracts TF-IDF keywords, and generates n-gram analysis

**Output**:

- TF-IDF scores for keywords
- High-frequency bigrams and trigrams
- Topic vocabulary analysis
- Content structure insights

**Key Metrics**:

- Term Frequency-Inverse Document Frequency (TF-IDF)
- N-gram patterns (1-gram, 2-gram, 3-gram, 4-gram)
- Unique vocabulary per domain

---

### 2. **Rank Profiler** 📊

**Type**: Parallel Agent (5 sub-agents)

**Responsibility**: Monitor search engine rankings for target keywords

**Sub-Agents**:

- `keyword_1_ranking_data` to `keyword_5_ranking_data`: Analyze each target keyword separately

**Tools Used**:

- `get_indian_organic_results`: Fetches top 10 Google Search results for India using SerpAPI
- Supports keyword list from `config/data/keywords.txt`

**Output**:

- Current ranking position for client website
- Competitor positions in SERP
- URL structure of top-ranked pages
- Ranking gaps vs competitors

**Key Features**:

- India-specific search results (Google.co.in)
- Top 10 organic results per keyword
- Real-time SERP data

---

### 3. **Competitor Update Checker** 🕵️

**Type**: Parallel Agent (5 sub-agents)

**Responsibility**: Track competitor website updates and content velocity

**Sub-Agents**:

- `sitemap_analyzer_1` to `sitemap_analyzer_5`: Analyze each competitor's sitemap

**Tools Used**:

- `fetch_competitor_sitemap`: Fetches and parses `sitemap.xml` from competitor domains
- Reads competitor URLs from `config/data/competitor_url.txt`

**Output**:

- Total URL count per competitor
- Last update timestamps
- Content velocity metrics
- Sitemap structure analysis
- Update frequency patterns

**Key Metrics**:

- Total pages indexed
- Recently updated pages
- Content addition rate
- Update schedule patterns

---

### 4. **Web Performance Analyzer** ⚡

**Type**: Standalone LLM Agent (Single)

**Responsibility**: Evaluate technical SEO and Core Web Vitals

**Tools Used**:

- `analyze_web_vitals`: Fetches Google PageSpeed Insights data for both client and competitor URLs

**Output** (key metrics):

- **Performance Score** (0-100): Overall page speed
- **LCP (Largest Contentful Paint)**: Loading performance (target: <2.5s)
- **CLS (Cumulative Layout Shift)**: Visual stability (target: <0.1)
- **FID (First Input Delay)**: Interactivity (target: <100ms)
- **TTFB (Time to First Byte)**: Server response time
- **FCP (First Contentful Paint)**: Paint timing

**Metrics for Both**:

- Mobile performance
- Desktop performance
- Device-specific insights

**Rating System**:

- 🟢 **GOOD**: Metric meets Google's threshold
- 🟠 **NEEDS_IMPROVEMENT**: Between good and poor
- 🔴 **POOR**: Below Google's minimum threshold

---

### 5. **Competitor Analyst** 🎯

**Type**: Standalone LLM Agent (Final synthesizer)

**Responsibility**: Consolidate all gathered data into strategic insights

**Input Data Sources**:

- `performace_reporter_output`: Web Vitals data from Phase 1
- `keyword_1-5_ranking_data`: Ranking positions from Phase 1
- `competitor_1-5_sitemap_data`: Competitor update data from Phase 1
- `competitor_1-5_content_data`: Content analysis from Phase 1
- `content_analyst_for_our_website`: Client content analysis from Phase 1

**Tools Used**:

- `save_output_file`: Saves final strategic report to output folder

**Output Structure** (Markdown Report):

1. **Technical Health Check**

   - Performance scorecard (Mobile vs Desktop)
   - Core Web Vitals assessment
   - Critical bottleneck identification

2. **SERP Battlefield**

   - Keyword ranking leaderboard
   - Volatility alerts
   - Urgent attention keywords

3. **Competitor Intelligence & Velocity**

   - Activity log of competitor updates
   - Content volume comparison
   - Update frequency patterns

4. **Content Gap Analysis**

   - Missing vocabulary analysis
   - High TF-IDF keywords competitors use but client doesn't
   - N-gram pattern gaps
   - Search intent analysis

5. **Executive Action Plan**
   - Top 3 priority tickets
   - Specific, actionable recommendations
   - Resource allocation suggestions

---

### 6. **Google Update Analyst** 📡

**Type**: Standalone LLM Agent (Monitoring)

**Responsibility**: Monitor and analyze latest Google Search algorithm updates and announcements

**Tools Used**:
- `fetch_google_search_status_updates`: Fetches latest updates from [Google Search Status Page](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history)
- `save_output_file`: Saves analysis report

**Output** (JSON Analysis):

- **Latest Update Title**: Name of the most recent update
- **Impact Summary**: What changed and why it matters
- **SEO Implications**: How this affects:
  - Organic search visibility
  - Ranking algorithms
  - Indexing behavior
  - SERP features
- **Action Required**: Specific steps to take in response
- **Severity Level**: Critical → High → Medium → Low
- **Status**: Active, Resolved, or Monitoring
- **Affected Areas**: Which parts of search are impacted
- **Timestamp**: When the update was announced

**Update Types Monitored**:
- 🔴 **Core Algorithm Updates**: Broad ranking changes
- 🟠 **Spam Updates**: Combat spam and low-quality content
- 🟡 **Feature Rollouts**: New SERP features, rich results
- 🔵 **Technical Changes**: Crawling, indexing, rendering improvements
- ⚪ **Policy Changes**: Content guidelines, removal policies

**Use Case**:
- Track Google's official announcements
- Understand ranking impacts immediately
- Prepare SEO strategy adjustments
- Communicate changes to stakeholders

---

## Agent Workflow

### Execution Flow

```
START
  │
  ├─► MASTER ORCHESTRATOR (Sequential)
  │   │
  │   ├─► PHASE 1: DATA GATHERING (Parallel)
  │   │   │
  │   │   ├─► Content Alchemist (Parallel)
  │   │   │   ├─► Competitor 1 Content Analysis
  │   │   │   ├─► Competitor 2 Content Analysis
  │   │   │   ├─► Competitor 3 Content Analysis
  │   │   │   ├─► Competitor 4 Content Analysis
  │   │   │   ├─► Competitor 5 Content Analysis
  │   │   │   └─► Client Website Analysis
  │   │   │
  │   │   ├─► Rank Profiler (Parallel)
  │   │   │   ├─► Keyword 1 SERP Analysis
  │   │   │   ├─► Keyword 2 SERP Analysis
  │   │   │   ├─► Keyword 3 SERP Analysis
  │   │   │   ├─► Keyword 4 SERP Analysis
  │   │   │   └─► Keyword 5 SERP Analysis
  │   │   │
  │   │   ├─► Competitor Update Checker (Parallel)
  │   │   │   ├─► Competitor 1 Sitemap Analysis
  │   │   │   ├─► Competitor 2 Sitemap Analysis
  │   │   │   ├─► Competitor 3 Sitemap Analysis
  │   │   │   ├─► Competitor 4 Sitemap Analysis
  │   │   │   └─► Competitor 5 Sitemap Analysis
  │   │   │
  │   │   └─► Web Performance Analyzer
  │   │       ├─► Client Website Performance
  │   │       └─► Competitor Performance
  │   │
  │   ├─► [WAIT for Phase 1 Completion]
  │   │
  │   └─► PHASE 2: ANALYSIS (Sequential)
  │       │
  │       └─► Competitor Analyst
  │           ├─► Technical Health Review
  │           ├─► SERP Analysis
  │           ├─► Competitor Intelligence
  │           ├─► Content Gap Analysis
  │           └─► Strategic Report Generation
  │
  └─► END

Timeline:
Phase 1: ~15-20 minutes (all agents run in parallel)
Phase 2: ~5-10 minutes (synthesis and analysis)
Total: ~20-30 minutes
```

### Data Flow

```
Content Analysis      Ranking Data        Sitemap Data         Performance Data
      │                    │                    │                      │
      └────────────────────┴────────────────────┴──────────────────────┘
                           │
                    ┌──────▼──────┐
                    │   CONTEXT   │
                    │   MEMORY    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────────┐
                    │ Competitor      │
                    │ Analyst Agent   │
                    │                 │
                    │ Synthesizes &   │
                    │ Correlates All  │
                    │ Data Sources    │
                    └──────┬──────────┘
                           │
                    ┌──────▼──────────┐
                    │ Final Report    │
                    │ (Markdown)      │
                    │                 │
                    │ • Technical     │
                    │ • Rankings      │
                    │ • Competitors   │
                    │ • Content Gaps  │
                    │ • Action Plan   │
                    └─────────────────┘
```

---

## Prerequisites

Before running the project, ensure you have:

### System Requirements

- **Python**: 3.12 or higher
- **macOS/Linux/Windows**: Any modern OS
- **Internet Connection**: Required for API calls and web scraping

### API Keys Required

1. **SERPAPI API Key** (for keyword ranking)

   - Sign up at [serpapi.com](https://serpapi.com)
   - Get your free/paid API key
   - Cost: Free tier available, ~$100/month for 100k queries

2. **Google API Key** (for PageSpeed Insights)
   - Set up at [Google Cloud Console](https://console.cloud.google.com)
   - Enable PageSpeed Insights API
   - Create an API key for your project

### Optional Dependencies

- `.env` file for secure credential storage (recommended)

---

## Installation & Setup

### Step 1: Clone or Navigate to Project

```bash
cd /Users/shashanksah/Desktop/Project/kaggle_capstone_project
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# On Windows, use:
# .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or using the pyproject.toml
pip install -e .

# Manual installation (if above doesn't work):
pip install google-adk python-multipart serpapi beautifulsoup4 scikit-learn python-dotenv requests
```

**Dependencies**:

- `google-adk`: Google Agent Development Kit for multi-agent orchestration
- `serpapi`: Google Search API client for SERP data
- `beautifulsoup4`: HTML parsing and scraping
- `scikit-learn`: TF-IDF vectorization and NLP analysis
- `requests`: HTTP requests for web scraping
- `python-dotenv`: Environment variable management (optional)
- `python-multipart`: Multipart form data handling

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << 'EOF'
# SerpAPI Configuration (for Google Search rankings)
SERPAPI_KEY=your_serpapi_api_key_here

# Google API Configuration (for PageSpeed Insights)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Log Level
LOG_LEVEL=INFO
EOF
```

**Or set environment variables directly**:

```bash
# In your shell (macOS/Linux)
export SERPAPI_KEY="your_api_key_here"
export GOOGLE_API_KEY="your_api_key_here"

# In Windows PowerShell
[Environment]::SetEnvironmentVariable("SERPAPI_KEY", "your_api_key_here", "User")
[Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your_api_key_here", "User")
```

### Step 5: Verify Installation

```bash
# Test Python and packages
python --version
python -c "import google.adk; import serpapi; import bs4; import sklearn; print('All dependencies installed!')"
```

---

## Configuration

### 1. Update Target Keywords

Edit `config/data/keywords.txt`:

```plaintext
1. keyword one
2. keyword two
3. keyword three
4. keyword four
5. keyword five
```

**Example** (current):

```plaintext
1. biodata
2. marriage biodata
3. bio data
4. shaadi biodata
5. wedding biodata
```

### 2. Update Competitor URLs

Edit `config/data/competitor_url.txt`:

```plaintext
1: https://competitor1.com/
2: https://competitor2.com/
3: https://competitor3.com/
4: https://competitor4.com/
5: https://competitor5.com/
```

**Example** (current):

```plaintext
1: https://biodatamaker.app/
2: https://createmybiodata.com/
3: https://www.myperfectbiodata.com/
4: https://www.simplebiodatamaker.in/
5: https://marathibiodatamaker.com/
```

### 3. Update Client Website URL

Edit `config/data/client_url.txt`:

```plaintext
https://your-client-website.com/
```

### 4. Agent Configuration (Advanced)

Agents use specific Gemini models:

- **Heavy Analysis**: `gemini-1.5-pro` (Content Analyst, Final Report)
- **Standard Processing**: `gemini-2.5-flash` (Ranking, Performance)
- **Lightweight Tasks**: `gemini-2.5-flash-lite` (Sitemaps, Parallel tasks)

To modify, edit the respective agent files in `agents/*/agent.py`:

```python
model=Gemini(
    model="gemini-2.5-flash-lite",  # Change model here
    retry_options=get_http_retry_config()
)
```

---

## Running the Project

### Method 1: Run Full Pipeline (Recommended)

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Run the complete orchestration
python -m agents.root_agent.agent

# Alternative (if main.py is configured):
python main.py
```

### Method 2: Run Individual Agents

```bash
# Test Content Alchemist (NLP Analysis)
python -c "from agents.content_alchemist.agent import root_agent; root_agent.execute()"

# Test Rank Profiler (Keyword Rankings)
python -c "from agents.rank_profiler.agent import root_agent; root_agent.execute()"

# Test Competitor Update Checker (Sitemaps)
python -c "from agents.competitor_update_checker.agent import root_agent; root_agent.execute()"

# Test Web Performance Analyzer
python -c "from agents.web_performance.agent import root_agent; root_agent.execute()"

# Test Competitor Analyst (Final Report)
python -c "from agents.competitor_analyst.agent import root_agent; root_agent.execute()"
```

### Method 2b: Run Using ADK Web Interface

```bash
# Launch interactive web UI for the agents
adk web ./agents

# This starts a local web server (typically at http://localhost:8080)
# where you can:
# - View all available agents
# - Test individual agents with custom inputs
# - Monitor agent execution in real-time
# - View agent outputs and logs
# - Trigger specific agents or the full pipeline
```

### Method 3: Interactive Testing

```bash
# Start Python interactive shell
python

# Inside Python:
from agents.root_agent.agent import root_agent
result = root_agent.execute()
print(result)
```

### Expected Output Flow

```
[INFO] Starting Master Orchestrator...
[INFO] PHASE 1: Data Gathering (Parallel)
[INFO]   ├─ Content Alchemist started (6 agents)
[INFO]   ├─ Rank Profiler started (5 agents)
[INFO]   ├─ Competitor Update Checker started (5 agents)
[INFO]   └─ Web Performance Analyzer started

[Waiting for Phase 1 to complete... ~15-20 minutes]

[INFO] PHASE 2: Analysis
[INFO]   └─ Competitor Analyst synthesizing data...

[SUCCESS] Report saved to: output/01-12-2025/daily_report.md
```

---

## ADK Web Interface

### Overview

The ADK (Agent Development Kit) Web interface provides an interactive dashboard to manage, monitor, and test your agents without writing code.

### Launch ADK Web UI

```bash
# Start the ADK web server
adk web ./agents

# The server will start at http://localhost:8080 (default)
# Output:
# Server running on http://localhost:8080
# Press Ctrl+C to stop
```

### ADK Web Commands

```bash
# Start web UI with custom port
adk web ./agents --port 3000

# Run with verbose logging
adk web ./agents --verbose

# Start web UI with environment file
adk web ./agents --env .env

# Specify custom host
adk web ./agents --host 0.0.0.0 --port 8080

# Enable debug mode
adk web ./agents --debug
```

### Using the Web Interface

Once the server is running:

1. **View Agents**

   - Navigate to `http://localhost:8080`
   - See all available agents organized by category
   - View agent descriptions and capabilities

2. **Test Individual Agents**

   - Click on any agent to view details
   - Provide input parameters
   - Execute agent and view real-time output
   - Check execution logs and performance metrics

3. **Monitor Execution**

   - Watch agent status (Running, Completed, Failed)
   - View progress bars for long-running agents
   - Access streaming logs in real-time

4. **Manage Outputs**

   - View all generated outputs
   - Download reports and analysis files
   - Check execution history
   - Compare results across runs

5. **Run Full Pipeline**
   - Trigger the complete Master Orchestrator
   - Monitor all phases in real-time
   - Track progress from Phase 1 (Data Gathering) to Phase 2 (Analysis)

### Example Web UI Workflow

```
1. Open browser → http://localhost:8080
2. Click "Master Orchestrator" agent
3. Review input parameters and configuration
4. Click "Execute" button
5. Watch PHASE 1 (Parallel execution of all data gathering agents)
6. Wait for completion indicator
7. PHASE 2 (Competitor Analyst) starts automatically
8. View final report in "Outputs" section
9. Download or share the daily_report.md
```

### Troubleshooting ADK Web

```bash
# If port is already in use
adk web ./agents --port 8081

# If connection refused, check if service is running
lsof -i :8080  # macOS/Linux

# Restart the service
Ctrl+C  # Stop current server
adk web ./agents  # Start fresh

# View web interface logs
adk web ./agents --verbose 2>&1 | tee adk_web.log
```

---

## Output Structure

### Report Naming & Classification

**Official Report Name**: `Daily Competitive Intelligence & SEO Strategic Report`

**File Generated**: `daily_report.md`

**Report Classification**:

- ✅ **Executive Intelligence Dashboard** (Strategic level)
- ✅ **Competitive Intelligence Report** (Market analysis level)
- ✅ **Strategic SEO Audit** (Technical + Content + Competitive)
- ❌ **NOT an L3 Matrix** (L3 matrices are execution-focused checklists)

**Key Distinction**:
| Aspect | L3 Matrix | Your Report |
|---|---|---|
| **Format** | Spreadsheet table | Markdown document |
| **Audience** | Execution teams | Decision-makers |
| **Data Layers** | Keyword rankings only | 5 interconnected data sources |
| **Analysis Depth** | Static yes/no | Root cause analysis |
| **Recommendations** | Task lists | Strategic priorities |
| **Frequency** | Monthly | Daily (automated) |

### Output Directory

All outputs are saved in `output/` with date-based folders:

```
output/
├── 01-12-2025/
│   ├── daily_report.md                    # Main strategic report
│   ├── competitor_1_result.json            # Content analysis
│   ├── competitor_2_result.json
│   ├── competitor_3_result.json
│   ├── competitor_4_result.json
│   ├── competitor_5_result.json
│   ├── client_website_result.json          # Your website analysis
│   ├── keyword_1_ranking_data.json         # SERP data
│   ├── keyword_2_ranking_data.json
│   ├── keyword_3_ranking_data.json
│   ├── keyword_4_ranking_data.json
│   ├── keyword_5_ranking_data.json
│   ├── sitemap_1.json                      # Competitor sitemaps
│   ├── sitemap_2.json
│   ├── sitemap_3.json
│   ├── sitemap_4.json
│   ├── sitemap_5.json
│   ├── performace_reporter_output.json     # Web Vitals
│   └── [additional analysis files]
└── [previous dates]/
```

### Main Report Format

`daily_report.md` is a **Markdown-formatted strategic intelligence brief** structured as follows:

```markdown
# Daily Competitive Intelligence & SEO Strategic Report

**Date**: 2025-12-01 | **Generated by**: Master Orchestrator

## Executive Summary

- Key metrics snapshot
- Critical alerts
- Strategic opportunities

## Section 1: Technical Health Check

- **Performance Scorecard**: Mobile vs Desktop comparison
- **Core Web Vitals Assessment**:
  - LCP (Loading), CLS (Stability), FID (Interactivity) ratings
  - Device-specific insights
  - Impact on rankings (correlation analysis)
- **Critical Bottlenecks**: Issues affecting search visibility

## Section 2: SERP Battlefield (Ranking Analysis)

- **Keyword Leaderboard**:
  - Your rank vs competitors for each keyword
  - Ranking gaps and volatility
  - Position trends
- **Quick Wins**: Keywords near breakthrough (position 3-5)
- **Urgent Attention**: Keywords at risk (position 8+)

## Section 3: Competitor Intelligence & Velocity

- **Activity Log**:
  - Which competitors updated recently
  - New content published
  - Site growth patterns
- **Content Velocity Comparison**:
  - Total URLs per competitor
  - Update frequency (daily/weekly/monthly)
  - Market aggressiveness indicator
- **Market Positioning**: Competitive threats and opportunities

## Section 4: Content Gap Analysis

- **Missing Vocabulary**:
  - High TF-IDF keywords competitors use but you don't
  - Search intent gaps
  - Topic recommendations
- **N-Gram Pattern Analysis**:
  - 2-word, 3-word, 4-word phrases you're missing
  - Examples: "marriage biodata format", "shaadi biodata template"
- **Content Opportunity Score**: Prioritized list of topics to create

## Section 5: Executive Action Plan

- **Priority Ticket #1**: High-impact, quick-win opportunity
- **Priority Ticket #2**: Medium-impact strategic initiative
- **Priority Ticket #3**: Long-term competitive advantage
- Each includes: Business impact, effort estimate, success metrics
```

**Report Characteristics**:

- **Length**: 5-10 pages (comprehensive yet readable)
- **Audience**: C-level, Product, Marketing, SEO leadership
- **Actionability**: Every section ends with specific next steps
- **Format**: Plain Markdown (easily shareable, convertible to PDF/HTML/Slack)
- **Refresh**: Generated daily (can be automated via scheduler)

### Data Files Format

**Content Analysis** (JSON):

```json
{
  "url": "https://competitor.com/",
  "tfidf_keywords": {
    "keyword1": 0.85,
    "keyword2": 0.72
  },
  "bigrams": { "phrase one": 45, "phrase two": 38 },
  "trigrams": { "three word phrase": 12 },
  "unique_vocabulary_count": 2341
}
```

**Ranking Data** (JSON):

```json
{
  "keyword": "biodata",
  "top_10_results": [
    {
      "position": 1,
      "title": "...",
      "url": "...",
      "snippet": "..."
    }
  ],
  "client_rank": 3,
  "top_competitor": "competitor_name"
}
```

**Sitemap Analysis** (JSON):

```json
{
  "competitor": "competitor_name",
  "total_urls": 1250,
  "last_updated": "2025-12-01T10:30:00Z",
  "recently_updated": ["url1", "url2"],
  "update_frequency": "daily"
}
```

**Performance Metrics** (JSON):

```json
{
  "website": "client or competitor",
  "performance_score": 85,
  "lcp": 2.1,
  "cls": 0.05,
  "ttfb": 0.8,
  "fcp": 1.2,
  "device": "mobile",
  "rating": "GOOD"
}
```

---

## Technologies Used

### Core Framework

- **Google Agent Development Kit (ADK)**: Multi-agent orchestration
- **Gemini AI Models**: LLM backbone for analysis

### APIs & Services

- **Google Gemini API**: Large language model inference
- **SerpAPI**: Google Search SERP data
- **Google PageSpeed Insights API**: Web performance metrics

### Libraries

- **BeautifulSoup4**: HTML parsing and web scraping
- **scikit-learn**: Machine learning utilities (TF-IDF, vectorization)
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

### Architecture Patterns

- **Parallel Agent Pattern**: Run multiple agents simultaneously
- **Sequential Agent Pattern**: Chain agents with dependencies
- **Tool-Augmented LLM**: LLMs with access to external tools
- **Context Passing**: Share data between agents via context memory

---

## Troubleshooting

### Common Issues

#### 1. "Missing API Key" Error

```
Error: Missing API Key. Please set SERPAPI_KEY in your .env file
```

**Solution**:

```bash
export SERPAPI_KEY="your_key_here"
# Or update .env file
```

#### 2. "Unable to fetch URL" Error

```
Error: Connection timeout while fetching https://competitor.com/
```

**Solution**:

- Check internet connection
- Verify URL is correct in config files
- Try adding/removing trailing slashes

#### 3. "Module not found" Error

```
ModuleNotFoundError: No module named 'google.adk'
```

**Solution**:

```bash
pip install google-adk --upgrade
```

#### 4. API Rate Limiting

```
Error: API rate limit exceeded
```

**Solution**:

- Wait before retrying (automatic retry is built-in)
- Upgrade SerpAPI plan for higher limits
- Reduce number of concurrent agents

#### 5. Python Version Issue

```
Error: Python 3.12+ required
```

**Solution**:

```bash
python3 --version
# If < 3.12, upgrade:
brew install python3  # macOS
# Or download from python.org
```

---

## Future Enhancements

- [ ] Scheduler for daily/weekly automatic reports
- [ ] Database integration for historical tracking
- [ ] Slack/Email delivery of reports
- [ ] Frontend dashboard for visualization
- [ ] A/B testing recommendations
- [ ] Content calendar generation
- [ ] Backlink analysis integration
- [ ] Search intent classification
- [ ] Seasonal trend analysis

---

## Support & Contribution

For issues or improvements:

1. Check logs in `output/` folder
2. Verify all configuration files are updated
3. Test individual agents first
4. Check API key quotas

---

## License

[Add your license information]

---

## Project Metadata

- **Author**: [Your Name]
- **Created**: December 2025
- **Purpose**: SEO Audit & Competitive Intelligence
- **Target Domain**: Biodata/Matrimonial Services
- **Python Version**: 3.12+
- **Status**: Active Development
