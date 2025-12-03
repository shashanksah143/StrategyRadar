"""
Pydantic output models for Competitor Update Checker agent.
Maps competitor sitemap data into structured JSON schema.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SitemapUrl(BaseModel):
    """Individual URL entry from a sitemap."""
    url: str = Field(
        ...,
        description="The full URL from the sitemap"
    )
    last_modified: Optional[str] = Field(
        None,
        description="Last modification date (ISO 8601 format). None if not available."
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com/page1",
                "last_modified": "2025-03-15"
            }
        }
    )


class SitemapIndex(BaseModel):
    """Sitemap index entry."""
    url: str = Field(
        ...,
        description="The URL of the sub-sitemap"
    )
    last_modified: Optional[str] = Field(
        None,
        description="Last modification date of the sitemap file"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com/sitemap-en.xml",
                "last_modified": "2025-03-10"
            }
        }
    )


class SitemapMetadata(BaseModel):
    """Metadata about the sitemap structure."""
    target_url: str = Field(
        ...,
        description="The competitor URL that was analyzed"
    )
    is_sitemap_index: bool = Field(
        default=False,
        description="Whether this is a sitemap index or regular sitemap"
    )
    total_entries: int = Field(
        default=0,
        description="Total number of URL or sitemap entries found"
    )
    analysis_date: str = Field(
        default="2025-03-15T10:30:00Z",
        description="When this analysis was performed (ISO 8601 format)"
    )
    timestamps_available: bool = Field(
        default=True,
        description="Whether lastmod timestamps were found in the sitemap"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "target_url": "https://competitor.com",
                "is_sitemap_index": False,
                "total_entries": 245,
                "analysis_date": "2025-03-15T10:30:00Z",
                "timestamps_available": True
            }
        }
    )


class RecentUpdate(BaseModel):
    """A recent URL update from competitor analysis."""
    rank: int = Field(
        ...,
        description="Position in the top recently modified list (1-5)"
    )
    url: str = Field(
        ...,
        description="The URL that was modified"
    )
    last_modified: Optional[str] = Field(
        None,
        description="Last modification date"
    )
    days_ago: Optional[int] = Field(
        None,
        description="Approximate number of days since modification"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rank": 1,
                "url": "https://competitor.com/latest-article",
                "last_modified": "2025-03-15",
                "days_ago": 0
            }
        }
    )


class ContentStrategy(BaseModel):
    """Strategic insights derived from competitor sitemap analysis."""
    update_frequency_assessment: str = Field(
        ...,
        description="Assessment of how frequently the competitor updates content (daily/weekly/monthly/sporadic)"
    )
    primary_content_focus: Optional[str] = Field(
        None,
        description="Identified main content categories or focus areas"
    )
    is_actively_updated: bool = Field(
        default=True,
        description="Whether the site shows active, ongoing updates"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable insights for competitive strategy"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "update_frequency_assessment": "weekly",
                "primary_content_focus": "Blog articles, product pages, documentation",
                "is_actively_updated": True,
                "recommendations": [
                    "Increase publishing frequency to match competitor pace",
                    "Focus on blog content as primary driver",
                    "Maintain freshness signals with regular updates"
                ]
            }
        }
    )


class CompetitorUpdateCheckerOutput(BaseModel):
    """
    Complete structured output for competitor update checker analysis.
    Contains sitemap metadata, recent updates, and strategic insights.
    """
    # Metadata
    metadata: SitemapMetadata = Field(
        ...,
        description="Information about the sitemap analyzed"
    )
    
    # Sitemap entries
    recent_updates: List[RecentUpdate] = Field(
        default_factory=list,
        description="Top 5 most recently modified URLs from the sitemap"
    )
    
    # Index entries (if sitemap index)
    sitemap_indexes: List[SitemapIndex] = Field(
        default_factory=list,
        description="Sub-sitemaps if this is a sitemap index"
    )
    
    # Analysis
    strategy_insights: ContentStrategy = Field(
        ...,
        description="Strategic analysis and recommendations"
    )
    
    # Raw data
    raw_xml_summary: str = Field(
        ...,
        description="Brief summary of the raw XML structure encountered"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metadata": {
                    "target_url": "https://competitor.com",
                    "is_sitemap_index": False,
                    "total_entries": 245,
                    "analysis_date": "2025-03-15T10:30:00Z",
                    "timestamps_available": True
                },
                "recent_updates": [
                    {
                        "rank": 1,
                        "url": "https://competitor.com/latest",
                        "last_modified": "2025-03-15",
                        "days_ago": 0
                    }
                ],
                "sitemap_indexes": [],
                "strategy_insights": {
                    "update_frequency_assessment": "weekly",
                    "primary_content_focus": "Blog and product updates",
                    "is_actively_updated": True,
                    "recommendations": ["Increase frequency", "Monitor trends"]
                },
                "raw_xml_summary": "Standard sitemap with 245 URLs. Contains lastmod dates for all entries."
            }
        }
    )
