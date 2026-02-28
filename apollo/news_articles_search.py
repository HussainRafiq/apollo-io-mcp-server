from typing import Optional, List, Any
from pydantic import BaseModel, Field


class NewsArticlesSearchQuery(BaseModel):
    """Query parameters for the Apollo News Articles Search endpoint."""

    organization_ids: List[str] = Field(
        description=(
            "REQUIRED. List of Apollo organization IDs for the companies whose news articles "
            "you want to retrieve. Each company in the Apollo database is assigned a unique "
            "string ID. You must obtain these IDs before calling this tool by using one of "
            "the following approaches: "
            "(1) Call `organization_search` with filters such as company name, location, or "
            "industry — then extract the `id` field from each returned organization object. "
            "(2) Call `organization_enrichment` with the company's primary domain — then "
            "extract the `id` field from the returned organization object. "
            "You can provide multiple IDs to retrieve news for several companies in one call. "
            "Example: ['5e66b6381e05b4008c8331b8']"
        )
    )
    categories: Optional[List[str]] = Field(
        default=None,
        description=(
            "Filter news articles by event category. Omit this field to retrieve all news "
            "types. You can provide multiple categories to include articles matching any of "
            "them. Common supported categories include: 'hires', 'investment', 'contract', "
            "'partnership', 'product_launch', 'acquisition', 'expansion'. "
            "Examples: ['hires', 'investment']"
        ),
    )
    published_at_min: Optional[str] = Field(
        default=None,
        description=(
            "Lower bound of the publication date range. Only articles published on or after "
            "this date will be returned. Format: YYYY-MM-DD. Use together with "
            "`published_at_max` to define a bounded date window, or use alone for an "
            "open-ended lower bound. Example: '2024-01-01'"
        ),
    )
    published_at_max: Optional[str] = Field(
        default=None,
        description=(
            "Upper bound of the publication date range. Only articles published on or before "
            "this date will be returned. Format: YYYY-MM-DD. Use together with "
            "`published_at_min` to define a bounded date window, or use alone for an "
            "open-ended upper bound. Example: '2024-12-31'"
        ),
    )
    page: Optional[int] = Field(
        default=None,
        description=(
            "Page number for paginating through results. Starts at 1. Use together with "
            "`per_page` to navigate large result sets. Example: 2"
        ),
    )
    per_page: Optional[int] = Field(
        default=None,
        description=(
            "Number of articles to return per page. Use together with `page` to paginate "
            "through large result sets. Smaller values improve response time. Example: 25"
        ),
    )


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
