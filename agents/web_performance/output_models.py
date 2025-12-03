"""
Pydantic models for Web Performance Reporter Agent structured output.
These models define the schema for the LLM to generate valid, structured JSON responses.
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Metadata about the analysis report"""
    analysis_timestamp: str
    target_url: str
    agent_name: str
    report_version: str
    analysis_tool: Optional[str] = None


class ScoreInterpretation(BaseModel):
    """Human-readable interpretation of performance scores"""
    mobile_interpretation: Optional[str] = None
    desktop_interpretation: Optional[str] = None
    comparative_analysis: Optional[str] = None


class PerformanceSummary(BaseModel):
    """High-level performance scores and health status"""
    overall_health_status: str
    mobile_score: int = Field(ge=0, le=100)
    desktop_score: int = Field(ge=0, le=100)
    score_interpretation: Optional[ScoreInterpretation] = None
    critical_issues_count: int = 0
    warning_issues_count: int = 0


class Metric(BaseModel):
    """A single Web Vitals or performance metric"""
    metric_name: str
    metric_code: str
    value: float
    unit: str
    display_value: str
    rating: str
    threshold_good: Optional[float] = None
    threshold_needs_improvement: Optional[float] = None
    description: Optional[str] = None
    impact_on_user_experience: Optional[str] = None
    is_core_web_vital: bool = False
    improvement_suggestions: List[str] = Field(default_factory=list)


class MetricSummary(BaseModel):
    """Summary of metric ratings for a device"""
    total_metrics: Optional[int] = None
    good_count: Optional[int] = None
    needs_improvement_count: Optional[int] = None
    poor_count: Optional[int] = None
    rating_distribution: Optional[Dict[str, int]] = None


class DeviceMetrics(BaseModel):
    """Performance metrics for a specific device type (mobile or desktop)"""
    device_type: str
    overall_score: int = Field(ge=0, le=100)
    score_category: Optional[str] = None
    metrics: List[Metric] = Field(default_factory=list)
    device_specific_insights: Optional[str] = None


class DeviceAnalysis(BaseModel):
    """Detailed device-specific metrics breakdown"""
    mobile: DeviceMetrics
    desktop: DeviceMetrics


class MetricsBreakdown(BaseModel):
    """Detailed breakdown of individual Web Vitals metrics"""
    core_web_vitals: List[Metric] = Field(default_factory=list)
    additional_metrics: List[Metric] = Field(default_factory=list)
    metrics_summary_by_device: Optional[Dict[str, MetricSummary]] = None


class PriorityAction(BaseModel):
    """A single priority action for performance improvement"""
    priority_level: str
    action: str
    affected_metrics: List[str] = Field(default_factory=list)
    expected_impact: str
    estimated_effort: Optional[str] = None
    device_specific: Optional[str] = None


class OptimizationArea(BaseModel):
    """A category of optimization with multiple improvements"""
    category: str
    improvements: List[str] = Field(default_factory=list)


class Recommendations(BaseModel):
    """Actionable recommendations to improve performance"""
    priority_actions: List[PriorityAction] = Field(default_factory=list)
    optimization_areas: List[OptimizationArea] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)


class DataSourceInfo(BaseModel):
    """Information about the source of the performance data"""
    data_type: str
    collection_method: str
    is_real_user_data: bool = False
    data_freshness: Optional[str] = None
    limitations: List[str] = Field(default_factory=list)


class ErrorDetail(BaseModel):
    """Details of an error encountered during analysis"""
    error_code: str
    error_message: str
    recovery_suggestion: Optional[str] = None


class Warning(BaseModel):
    """A warning about the analysis or data"""
    warning_message: str
    affected_component: Optional[str] = None


class ErrorsAndWarnings(BaseModel):
    """Errors and warnings encountered during analysis"""
    errors: List[ErrorDetail] = Field(default_factory=list)
    warnings: List[Warning] = Field(default_factory=list)


class ExecutiveSummary(BaseModel):
    """Executive summary for quick understanding"""
    one_liner: Optional[str] = None
    key_findings: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)


class WebPerformanceOutput(BaseModel):
    """
    Structured output schema for Web Performance Reporter Agent.
    This model defines the complete JSON response structure that the LLM will generate.
    All required fields must be present in the output.
    """
    metadata: Metadata
    performance_summary: PerformanceSummary
    device_analysis: DeviceAnalysis
    metrics_breakdown: MetricsBreakdown
    recommendations: Recommendations
    data_source_info: DataSourceInfo
    errors_and_warnings: Optional[ErrorsAndWarnings] = None
    executive_summary: Optional[ExecutiveSummary] = None
