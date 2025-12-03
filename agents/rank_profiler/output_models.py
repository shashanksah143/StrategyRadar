"""
Pydantic models for Rank Profiler Agent structured output.
These models define the schema for ranking data from SERPAPI Google Search results.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SearchMetadata(BaseModel):
    """Metadata about the search request and response"""
    id: Optional[str] = None
    status: Optional[str] = None
    json_endpoint: Optional[str] = None
    created_at: Optional[str] = None
    processed_at: Optional[str] = None
    google_url: Optional[str] = None
    raw_html_file: Optional[str] = None
    total_time_taken: Optional[float] = None


class SearchParameters(BaseModel):
    """Parameters used for the search request"""
    engine: Optional[str] = None
    q: Optional[str] = None
    google_domain: Optional[str] = None
    hl: Optional[str] = None
    gl: Optional[str] = None
    num: Optional[int] = None
    device: Optional[str] = None


class SearchInformation(BaseModel):
    """Information about the search results"""
    organic_results_state: Optional[str] = None
    query_displayed: Optional[str] = None
    total_results: Optional[int] = None
    time_taken_displayed: Optional[float] = None


class OrganicResult(BaseModel):
    """A single organic search result"""
    position: int
    title: str
    link: str
    displayed_link: Optional[str] = None
    snippet: Optional[str] = None
    date: Optional[str] = None
    redirect_link: Optional[str] = None
    thumbnail: Optional[str] = None


class RichSnippet(BaseModel):
    """Rich snippet data from a search result"""
    rating: Optional[float] = None
    reviews: Optional[int] = None
    extensions: Optional[List[str]] = Field(default_factory=list)


class SearchSource(BaseModel):
    """Information about the source of a search result"""
    description: Optional[str] = None
    source_info_link: Optional[str] = None
    security: Optional[str] = None
    icon: Optional[str] = None


class AboutThisResult(BaseModel):
    """Metadata about the search result from Google"""
    source: Optional[SearchSource] = None
    keywords: Optional[List[str]] = Field(default_factory=list)
    languages: Optional[List[str]] = Field(default_factory=list)
    regions: Optional[List[str]] = Field(default_factory=list)


class Sitelink(BaseModel):
    """Sitelinks for a search result"""
    title: Optional[str] = None
    link: Optional[str] = None


class Sitelinks(BaseModel):
    """Collection of sitelinks"""
    inline: Optional[List[Sitelink]] = Field(default_factory=list)


class EnhancedOrganicResult(BaseModel):
    """Enhanced organic result with additional metadata"""
    position: int
    title: str
    link: str
    displayed_link: Optional[str] = None
    snippet: Optional[str] = None
    date: Optional[str] = None
    redirect_link: Optional[str] = None
    thumbnail: Optional[str] = None
    rich_snippet: Optional[RichSnippet] = None
    about_this_result: Optional[AboutThisResult] = None
    sitelinks: Optional[Sitelinks] = None
    cached_page_link: Optional[str] = None
    related_pages_link: Optional[str] = None


class Pagination(BaseModel):
    """Pagination information for results"""
    current: Optional[int] = None
    next: Optional[str] = None
    next_link: Optional[str] = None
    previous: Optional[str] = None
    previous_link: Optional[str] = None
    other_pages: Optional[Dict[str, str]] = None


class RelatedSearch(BaseModel):
    """A related search suggestion"""
    query: str
    link: str


class KnowledgeGraphAttribute(BaseModel):
    """An attribute in the knowledge graph"""
    name: Optional[str] = None
    value: Optional[str] = None
    link: Optional[str] = None


class KeywordMetrics(BaseModel):
    """Metrics for keyword performance"""
    keyword: str
    position: Optional[int] = None
    domain: Optional[str] = None
    url: str
    snippet: Optional[str] = None
    is_featured_snippet: bool = False
    cpc: Optional[float] = None
    search_volume: Optional[int] = None


class CompetitorPosition(BaseModel):
    """Competitor's position for a specific keyword"""
    rank: int
    domain: str
    title: str
    url: str
    snippet: Optional[str] = None


class KeywordRankingAnalysis(BaseModel):
    """Complete ranking analysis for a keyword"""
    keyword: str
    total_results: Optional[int] = None
    search_time_seconds: Optional[float] = None
    top_3_competitors: List[CompetitorPosition] = Field(default_factory=list)
    top_10_results: List[EnhancedOrganicResult] = Field(default_factory=list)
    featured_snippet: Optional[EnhancedOrganicResult] = None
    related_searches: List[RelatedSearch] = Field(default_factory=list)


class RankingInsight(BaseModel):
    """SEO insight from ranking data"""
    keyword: str
    insight_type: str  # e.g., "opportunity", "threat", "market_gap"
    description: str
    confidence: float = Field(ge=0, le=1)
    suggested_action: Optional[str] = None


class CompetitorAnalysis(BaseModel):
    """Analysis of competitor presence"""
    domain: str
    keywords_ranking: int
    top_position: Optional[int] = None
    average_position: Optional[float] = None
    backlink_count: Optional[int] = None
    domain_authority: Optional[float] = None


class RankProfilerOutput(BaseModel):
    """
    Complete output schema for Rank Profiler Agent.
    Contains comprehensive ranking data and analysis for keywords.
    """
    metadata: SearchMetadata
    search_parameters: SearchParameters
    search_information: SearchInformation
    keyword: str
    organic_results: List[EnhancedOrganicResult] = Field(default_factory=list)
    pagination: Optional[Pagination] = None
    related_searches: List[RelatedSearch] = Field(default_factory=list)
    featured_snippet: Optional[EnhancedOrganicResult] = None
    knowledge_graph: Optional[Dict[str, Any]] = None
    
    # Analysis fields
    top_3_competitors: List[CompetitorPosition] = Field(default_factory=list)
    competitor_analysis: Optional[List[CompetitorAnalysis]] = Field(default_factory=list)
    ranking_insights: Optional[List[RankingInsight]] = Field(default_factory=list)
    
    # Summary fields
    total_results: Optional[int] = None
    current_client_position: Optional[int] = None
    current_client_rank: Optional[CompetitorPosition] = None
    market_saturation_level: Optional[str] = None  # LOW, MEDIUM, HIGH
    opportunity_score: Optional[float] = Field(default=None, ge=0, le=100)
    
    # Error handling
    error: Optional[str] = None
    error_code: Optional[str] = None
    recovery_suggestion: Optional[str] = None
