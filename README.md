# 🤖 SEO Competitive Intelligence & Analysis Engine

**AI-Powered Multi-Agent System for Real-Time SEO Audits and Competitive Intelligence**

An intelligent, fully automated multi-agent orchestration system powered by Google's Agent Development Kit (ADK) and Gemini AI that performs comprehensive competitive intelligence, technical SEO audits, and generates data-driven strategic intelligence reports. Built for the biodata/matrimonial niche, the system analyzes 5 target keywords against 5 main competitors while evaluating client website performance.

---

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

### What This Project Does

This is an **autonomous SEO analysis and competitive intelligence platform** that:

1. **Monitors Search Rankings** - Tracks your website and competitors' positions for target keywords on Google India in real-time
2. **Analyzes Content Strategy** - Performs NLP analysis (TF-IDF, n-gram extraction) to identify content gaps and competitive vocabulary
3. **Tracks Competitor Velocity** - Monitors competitor sitemaps to understand update frequency and content publishing patterns
4. **Assesses Technical Health** - Evaluates Core Web Vitals (LCP, CLS, FID, TTFB) and PageSpeed performance metrics
5. **Generates Strategic Reports** - Synthesizes 5 data sources into a comprehensive intelligence brief with actionable recommendations

### The Daily Competitive Intelligence & SEO Strategic Report

Instead of traditional L3 matrices, this system generates a **strategic intelligence brief** that:

- **Synthesizes 5 data sources** into correlated, actionable insights
- **Identifies root causes** for ranking issues (e.g., "Poor rankings linked to Core Web Vitals bottleneck")
- **Recommends specific actions** with business impact and effort estimates
- **Tracks competitor velocity** and market positioning shifts
- **Analyzes content gaps** using AI-powered NLP and keyword analysis
- **Targets multiple stakeholders** with relevant insights for each role

**Key Difference from L3 Matrix**: While L3 matrices show keyword rankings in a spreadsheet for execution teams, this report connects rankings to technical issues, content gaps, and competitor strategies, then prioritizes 3 specific strategic action items for decision-makers.

### Stakeholder Value Matrix

| **Stakeholder Role**    | **Reports & Insights Delivered**                                                                           |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| **C-Level Executives**  | Daily market positioning, strategic threats, competitive threats & opportunities, ROI-focused action items |
| **Product Managers**    | Competitor feature gaps, market velocity trends, technical priorities affecting user experience            |
| **Content Strategists** | Content gap analysis, keyword opportunities, competitor content velocity, topic recommendations            |
| **SEO Specialists**     | Detailed technical audits, ranking positions, root cause analysis, optimization priorities                 |
| **Engineering Teams**   | Web Vitals assessment, performance bottlenecks, technical priorities                                       |
| **Marketing Directors** | Competitive benchmarking, market aggressiveness trends, campaign opportunity analysis                      |

---

## System Architecture

### High-Level Orchestration Flow

The system follows a **two-phase architecture**:

- **Phase 1 (Parallel)**: All data gathering agents run simultaneously for speed
- **Phase 2 (Sequential)**: Analysis agent waits for Phase 1 completion, then synthesizes insights

```
┌────────────────────────────────────────────────────────────────┐
│              MASTER ORCHESTRATOR (Sequential Execution)        │
└────────────────────┬───────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    PHASE 1: DATA GATHERING   PHASE 2: ANALYSIS
    (Parallel - All at Once)  (Sequential - After Phase 1)
        │                         │
        ├─ Content Alchemist      │
        │  (NLP Analysis)         │
        │                         │
        ├─ Rank Profiler          ├─ Competitor Analyst
        │  (SERP Rankings)        │  (Final Report Generation)
        │                         │
        ├─ Competitor Update      │
        │  Checker (Sitemaps)     │
        │                         │
        └─ Web Performance        │
           Analyzer (Web Vitals)  │
                                  │
            ┌─────────────────────┘
            │
        ┌───▼────────────┐
        │ Daily Strategic│
        │ Intelligence   │
        │ Report (MD)    │
        └────────────────┘

⏱️ Timeline: Phase 1 (~15-20 min) → Phase 2 (~5-10 min) = ~25-30 min total
```

---

## Agents Overview

The system consists of **4 parallel data-gathering agents** and **1 synthesis agent**:

### Phase 1: Data Gathering (Parallel Execution)

#### 1. **Content Alchemist** 🧪 - NLP Content Analysis

- **Agents**: 5 competitors + 1 client (6 parallel sub-agents)
- **Process**: Fetches HTML, cleans text, extracts TF-IDF keywords and n-grams
- **Output**:
  - TF-IDF keyword scores (identifies high-value keywords competitors rank for)
  - N-gram patterns (2-gram, 3-gram, 4-gram phrases)
  - Vocabulary gaps (terms competitors use that you don't)
  - Content structure insights

#### 2. **Rank Profiler** 📊 - Google Search Rankings

- **Agents**: 5 keywords in parallel
- **Process**: Queries Google India via SerpAPI for top 10 organic results per keyword
- **Output**:
  - Client's current ranking position
  - Competitor positions in SERP
  - Ranking gaps vs competitors
  - Top-ranking URLs and their snippets

#### 3. **Competitor Update Checker** 🕵️ - Content Velocity

- **Agents**: 5 competitors in parallel
- **Process**: Fetches and parses sitemap.xml from each competitor
- **Output**:
  - Total URLs indexed
  - Last update timestamps
  - Recently modified pages
  - Update frequency patterns (daily/weekly/monthly)
  - Content velocity comparison

#### 4. **Web Performance Analyzer** ⚡ - Technical SEO Health

- **Single Agent**: Analyzes both client and competitors
- **Process**: Fetches Google PageSpeed Insights data (Lab + Real User data)
- **Output** (Mobile & Desktop):
  - Performance Score (0-100)
  - LCP (Largest Contentful Paint): Target <2.5s
  - CLS (Cumulative Layout Shift): Target <0.1
  - FID (First Input Delay): Target <100ms
  - TTFB (Time to First Byte)
  - FCP (First Contentful Paint)
- **Ratings**: 🟢 GOOD | 🟠 NEEDS_IMPROVEMENT | 🔴 POOR

---

### Phase 2: Analysis & Synthesis (Sequential)

#### 5. **Competitor Analyst** 🎯 - Strategic Intelligence Synthesizer

- **Type**: Standalone LLM Agent
- **Process**: Takes all Phase 1 outputs and synthesizes into strategic insights
- **Output** (Markdown Report):
  1. **Technical Health Check** - Performance scorecard, bottleneck identification
  2. **SERP Battlefield** - Ranking leaderboard, volatility alerts, urgency flags
  3. **Competitor Intelligence** - Update activity log, velocity comparison
  4. **Content Gap Analysis** - Missing vocabulary, keyword opportunities, topic recommendations
  5. **Executive Action Plan** - Top 3 priority initiatives with business impact

---

## Execution Workflow

### Complete Pipeline Flow

```
START: Master Orchestrator
│
├─► PHASE 1: DATA GATHERING (All run in parallel, no waiting)
│   │
│   ├─► Content Alchemist (6 parallel sub-agents)
│   │    └─ Analyzes: 5 competitors + client website
│   │
│   ├─► Rank Profiler (5 parallel sub-agents)
│   │    └─ Analyzes: 5 target keywords
│   │
│   ├─► Competitor Update Checker (5 parallel sub-agents)
│   │    └─ Fetches: 5 competitor sitemaps
│   │
│   └─► Web Performance Analyzer (single agent)
│        └─ Fetches: Client + competitor performance metrics
│
├─► [WAIT for Phase 1 completion]  (~15-20 minutes)
│
├─► PHASE 2: ANALYSIS & SYNTHESIS (Sequential)
│   │
│   └─► Competitor Analyst Agent
│        ├─ Reads Phase 1 outputs from context memory
│        ├─ Synthesizes: Technical + Ranking + Content + Performance insights
│        ├─ Generates: Strategic intelligence report (Markdown)
│        └─ Saves: daily_report.md to output folder
│
└─► END: Report ready for stakeholders (~5-10 minutes)

⏱️ TOTAL TIME: 20-30 minutes
```

### Data Flow Architecture

```
All Phase 1 outputs → Shared Context Memory
                     ↓
        ┌────────────┴────────────┐
        │                         │
   Content Analysis          Ranking Data
   (Competitor vocab,        (SERP positions,
    missing keywords)         ranking gaps)
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   Sitemap Data              Performance Data
   (Competitor velocity,     (Web Vitals scores,
    update frequency)         technical issues)
        │                         │
        └────────────┬────────────┘
                     │
            ┌────────▼────────┐
            │  Competitor     │
            │  Analyst Agent  │
            │  (LLM Model)    │
            │  - Reads ALL    │
            │  - Synthesizes  │
            │  - Correlates   │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │ daily_report.md │
            │ (Strategic      │
            │  Intelligence)  │
            └─────────────────┘
```

---

## Prerequisites

### System Requirements

- **Python 3.12+** (required for Google ADK)
- **macOS, Linux, or Windows** with internet connection
- **API Keys**: SerpAPI (for Google Search) + Google Cloud API Key (for PageSpeed Insights)

### Required API Keys

1. **SerpAPI Key** (Google Search Rankings)

   - Sign up: [serpapi.com](https://serpapi.com)
   - Free tier available (100 queries/month)
   - Paid: ~$100/month for 100,000 queries

2. **Google API Key** (PageSpeed Insights)
   - Create in: [Google Cloud Console](https://console.cloud.google.com)
   - Enable PageSpeed Insights API
   - Create service account or API key

---

## Quick Start (5 minutes)

### 1. Clone/Navigate to Project

```bash
cd /Users/shashanksah/Desktop/Project/kaggle_capstone_project
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv sync
# Or manually:
pip install google-adk serpapi beautifulsoup4 scikit-learn requests python-dotenv
```

### 4. Set API Keys

```bash
# Create .env file
cat > .env << 'EOF'
SERPAPI_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_google_api_key_here
PAGESPEED_API_KEY=your_pagespeed_apy_key_here
EOF

# Or export directly:
export SERPAPI_KEY="your_key"
export GOOGLE_API_KEY="your_key"
export PAGESPEED_API_KEY="your_key"
```

### 5. Configure Target Keywords & Competitors

Edit these files to customize analysis:

- **Keywords**: `config/data/keywords.txt` (5 target keywords)
- **Competitors**: `config/data/competitor_url.txt` (5 competitor URLs)
- **Client Site**: `config/data/client_url.txt` (your website URL)

---

## Running the Project

### Use ADK Web Interface (Interactive)

```bash
# Launch web dashboard
adk web ./agents

# Open browser: http://localhost:8080
# Features:
# - View all agents and descriptions
# - Test individual agents interactively
# - Monitor real-time execution
# - Download outputs and reports
```

## Output & Reports

### Output Directory Structure

All reports and data files are saved in `output/` with date-based folders:

```
output/
├── 01-12-2025/
│   ├── daily_report.md                      # Main strategic report (Markdown)
│   ├── competitor_1_result.json             # Content analysis results
│   ├── competitor_2_result.json
│   ├── competitor_3_result.json
│   ├── competitor_4_result.json
│   ├── competitor_5_result.json
│   ├── client_website_result.json           # Your website content analysis
│   ├── keyword_1_ranking_data.json          # SERP ranking data
│   ├── keyword_2_ranking_data.json
│   ├── keyword_3_ranking_data.json
│   ├── keyword_4_ranking_data.json
│   ├── keyword_5_ranking_data.json
│   ├── sitemap_1.json                       # Competitor sitemap analysis
│   ├── sitemap_2.json
│   ├── sitemap_3.json
│   ├── sitemap_4.json
│   ├── sitemap_5.json
│   └── performace_reporter_output.json      # Web Vitals metrics
└── [previous dates]/
```

### Main Report: `daily_report.md`

This is the **strategic intelligence brief** that synthesizes all data sources:

**Report Structure** (5-10 pages):

1. **Executive Summary**

   - Key metrics snapshot
   - Critical alerts and threats
   - Strategic opportunities

2. **Technical Health Check**

   - Performance scorecard (Mobile vs Desktop)
   - Core Web Vitals assessment (LCP, CLS, FID ratings)
   - Critical bottlenecks affecting rankings

3. **SERP Battlefield** (Ranking Analysis)

   - Keyword leaderboard (your rank vs competitors)
   - Ranking gaps and volatility
   - Quick wins (keywords near top positions)
   - Urgent attention items (keywords at risk)

4. **Competitor Intelligence & Velocity**

   - Competitor activity log (recent updates)
   - Content velocity comparison (URLs/month)
   - Update frequency patterns
   - Market aggressiveness trends

5. **Content Gap Analysis**

   - Missing vocabulary (keywords competitors use)
   - N-gram patterns you're missing
   - Search intent gaps
   - Topic recommendations with priority scores

6. **Executive Action Plan**
   - Priority #1: High-impact, quick-win
   - Priority #2: Medium-impact strategic initiative
   - Priority #3: Long-term competitive advantage
   - Each with: business impact, effort estimate, success metrics

**Report Characteristics**:

- ✅ **Actionable**: Every section ends with specific next steps
- ✅ **Multi-stakeholder**: Insights for C-level, product, marketing, SEO, engineering
- ✅ **Data-driven**: All recommendations backed by analysis
- ✅ **Shareable**: Plain Markdown (convertible to PDF, HTML, Slack)
- ✅ **Automatable**: Can be generated daily via scheduler

### Data Files Format

**Content Analysis JSON**:

```json
{
  "url": "https://competitor.com/",
  "tfidf_keywords": { "keyword1": 0.85, "keyword2": 0.72 },
  "bigrams": { "phrase one": 45, "phrase two": 38 },
  "trigrams": { "three word phrase": 12 },
  "unique_vocabulary_count": 2341
}
```

**Ranking Data JSON**:

```json
{
  "keyword": "biodata",
  "top_10_results": [
    { "position": 1, "title": "...", "url": "...", "snippet": "..." }
  ],
  "client_rank": 3,
  "top_competitor": "competitor_name"
}
```

**Web Vitals JSON**:

```json
{
  "website": "client or competitor",
  "performance_score": 85,
  "lcp": 2.1,
  "cls": 0.05,
  "ttfb": 0.8,
  "device": "mobile",
  "rating": "GOOD"
}
```

---

## Technology Stack

### Core Framework

- **Google Agent Development Kit (ADK)** - Multi-agent orchestration and coordination
- **Gemini AI Models** - Language models for analysis and synthesis
  - `gemini-2.5-pro` for heavy analysis
  - `gemini-2.5-flash` for standard processing

### External APIs

- **Google Gemini API** - AI model inference
- **SerpAPI** - Google Search SERP data (rankings)
- **Google PageSpeed Insights API** - Web performance metrics

### Python Libraries

- **BeautifulSoup4** - HTML parsing and web scraping
- **scikit-learn** - TF-IDF vectorization, NLP analysis
- **requests** - HTTP client for API calls
- **python-dotenv** - Environment variable management

### Architecture Patterns

- **Parallel Agent Pattern** - Multiple agents running simultaneously
- **Sequential Agent Pattern** - Chained execution with dependencies
- **Tool-Augmented LLM** - LLM agents with access to external tools
- **Context Sharing** - Data sharing between agents via context memory

---

## Troubleshooting

### Common Issues

#### Missing API Key Error

```
Error: Missing API Key. Please set SERPAPI_KEY in your .env file
```

**Solution**:

```bash
export SERPAPI_KEY="your_key_here"
# Or update .env file and reload
```

#### Connection Timeout

```
Error: Connection timeout while fetching https://competitor.com/
```

**Solution**:

- Check internet connection
- Verify URLs in config files are correct
- Try adding/removing trailing slashes from URLs

#### Module Not Found

```
ModuleNotFoundError: No module named 'google.adk'
```

**Solution**:

```bash
pip install google-adk --upgrade
pip install -e .
```

#### API Rate Limiting

```
Error: API rate limit exceeded (SerpAPI)
```

**Solution**:

- Wait and retry (automatic retry is built-in)
- Upgrade SerpAPI plan for higher limits
- Reduce number of concurrent agents (edit agent configuration)

#### Python Version Error

```
Error: Python 3.12+ required
```

**Solution**:

```bash
python3 --version
# If < 3.12, install Python 3.12+ from python.org or:
brew install python3  # macOS
```

#### Web Interface Not Connecting

```
Error: Could not connect to http://localhost:8080
```

**Solution**:

```bash
# Try different port
adk web ./agents --port 8081

# Check if port is in use
lsof -i :8080  # macOS/Linux

# Kill process if needed, then restart
adk web ./agents
```

---

## Future Enhancements

- [ ] Daily/weekly automatic scheduling (cron or cloud functions)
- [ ] Database integration for historical tracking and trend analysis
- [ ] Slack/Email integration for automated report delivery
- [ ] Frontend dashboard for data visualization and insights
- [ ] A/B testing recommendations engine
- [ ] Automated content calendar generation
- [ ] Backlink analysis and monitoring
- [ ] Search intent classification and clustering
- [ ] Seasonal trend analysis and forecasting
- [ ] Predictive ranking models

---

## Project Structure

```
kaggle_capstone_project/
├── agents/                         # All agent implementations
│   ├── root_agent/                # Master orchestrator
│   ├── content_alchemist/          # NLP content analysis
│   ├── rank_profiler/              # Keyword ranking analysis
│   ├── competitor_update_checker/  # Sitemap monitoring
│   ├── web_performance/            # Web Vitals analysis
│   └── competitor_analyst/         # Final synthesis & reporting
├── tools/                          # Utility tools
│   ├── nlp_analyzer.py             # TF-IDF and n-gram extraction
│   ├── ranking_monitor.py          # SerpAPI integration
│   ├── web_vitals_fetcher.py       # PageSpeed Insights integration
│   └── sitemap_fetcher.py          # Sitemap parsing
├── utils/                          # Helper utilities
│   ├── file_loader.py              # File I/O operations
│   ├── file_saver.py               # Output saving
│   └── retry_config.py             # API retry configuration
├── config/data/                    # Configuration files
│   ├── keywords.txt                # Target keywords (5)
│   ├── competitor_url.txt          # Competitor URLs (5)
│   └── client_url.txt              # Client website URL
├── output/                         # Generated reports and data
├── ARCHITECTURE.md                 # Detailed architecture documentation
├── README.md                       # This file
└── pyproject.toml                  # Project dependencies
```

---

## Key Features

✅ **Automated Intelligence** - Runs without manual intervention  
✅ **Multi-Agent Architecture** - Parallel processing for speed  
✅ **Data Integration** - Synthesizes 5 data sources (rankings, content, velocity, performance, vitals)  
✅ **Strategic Insights** - Beyond rankings: root cause analysis & recommendations  
✅ **Real-Time SERP Data** - Current Google Search rankings for India  
✅ **Content Analysis** - AI-powered NLP for content gaps and opportunities  
✅ **Performance Audits** - Core Web Vitals and PageSpeed Insights  
✅ **Competitor Tracking** - Monitor update frequency and velocity  
✅ **Shareable Reports** - Markdown format for easy distribution  
✅ **Customizable** - Configure keywords, competitors, and client URLs

---

## Support & Debugging

**For troubleshooting**:

1. Check logs in `output/` folder for error messages
2. Verify all API keys are set correctly
3. Confirm configuration files have proper URLs
4. Test individual agents before running full pipeline
5. Check your API quotas (especially SerpAPI)

**For questions or issues**:

- Review `ARCHITECTURE.md` for detailed system design
- Check `agents/*/instructions.txt` for agent-specific behavior
- Review tool documentation in `tools/`

---

## License

MIT License

Copyright (c) 2025 SEO Competitive Intelligence & Analysis Engine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Project Metadata

- **Project Name**: SEO Competitive Intelligence & Analysis Engine
- **Author**: Shashank Sah
- **Contact**: shashanksah143@gmail.com
- **Created**: December 2025
- **Python Version**: 3.12+
- **Framework**: Google Agent Development Kit (ADK)
- **LLM**: Google Gemini (2.5-pro, 2.5-flash)
- **Status**: Active Development
- **Frequency**: Daily automated reporting (manually configurable)

---

**Built with ❤️ for data-driven SEO decisions**
