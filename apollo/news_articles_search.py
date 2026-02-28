from typing import Optional, List, Any
from pydantic import BaseModel, Field


class NewsArticlesSearchQuery(BaseModel):
    """Query for News Articles Search endpoint."""
    organization_ids: List[str] = Field(
        description="The Apollo IDs for the companies. Required. Example: 5e66b6381e05b4008c8331b8"
    )
    categories: Optional[List[str]] = Field(
        default=None,
        description="Filter by news categories. Examples: hires; investment; contract"
    )
    published_at_min: Optional[str] = Field(
        default=None,
        description="Lower bound of date range (YYYY-MM-DD). Use with published_at_max."
    )
    published_at_max: Optional[str] = Field(
        default=None,
        description="Upper bound of date range (YYYY-MM-DD). Use with published_at_min."
    )
    page: Optional[int] = Field(default=None, description="Page number for pagination.")
    per_page: Optional[int] = Field(default=None, description="Results per page.")


class NewsArticle(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    domain: Optional[str] = None
    title: Optional[str] = None
    snippet: Optional[str] = None
    organization_ids: Optional[List[str]] = None
    published_at: Optional[str] = None
    event_categories: Optional[List[str]] = None


class NewsArticlesSearchResponse(BaseModel):
    pagination: Optional[Any] = None
    news_articles: Optional[List[NewsArticle]] = None
