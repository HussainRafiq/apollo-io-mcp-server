from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BulkPeopleEnrichmentDetail(BaseModel):
    """Detail for one person in bulk enrichment."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    hashed_email: Optional[str] = None
    organization_name: Optional[str] = None
    domain: Optional[str] = None
    id: Optional[str] = None  # Apollo person ID
    linkedin_url: Optional[str] = None


class BulkPeopleEnrichmentRequest(BaseModel):
    """Request body for Bulk People Enrichment."""
    details: List[BulkPeopleEnrichmentDetail] = Field(
        description="Up to 10 people to enrich. Each object can have first_name, last_name, name, email, domain, id, etc."
    )


class BulkPeopleEnrichmentQuery(BaseModel):
    """Query params for Bulk People Enrichment."""
    run_waterfall_email: Optional[bool] = False
    run_waterfall_phone: Optional[bool] = False
    reveal_personal_emails: Optional[bool] = False
    reveal_phone_number: Optional[bool] = False
    webhook_url: Optional[str] = None


class BulkOrganizationEnrichmentQuery(BaseModel):
    """Query for Bulk Organization Enrichment - domains as list."""
    domains: List[str] = Field(
        description="Domain of each company to enrich (up to 10). Example: apollo.io, microsoft.com"
    )
