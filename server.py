from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
from apollo import *

import os

from dotenv import load_dotenv
load_dotenv()

apollo_client = ApolloClient(api_key=os.getenv("APOLLO_IO_API_KEY"))

mcp = FastMCP("Apollo.io")

@mcp.tool()
async def people_enrichment(query: PeopleEnrichmentQuery) -> Optional[dict]:
    """
    Use the People Enrichment endpoint to enrich data for 1 person.
    https://docs.apollo.io/reference/people-enrichment
    """
    result = await apollo_client.people_enrichment(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_enrichment(query: OrganizationEnrichmentQuery) -> Optional[dict]:
    """
    Use the Organization Enrichment endpoint to enrich data for 1 company.
    https://docs.apollo.io/reference/organization-enrichment
    """
    result = await apollo_client.organization_enrichment(query)
    return result.model_dump() if result else None

@mcp.tool()
async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
    """
    Use the People Search endpoint to find people.
    https://docs.apollo.io/reference/people-search
    """
    result = await apollo_client.people_search(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
    """
    Use the Organization Search endpoint to find organizations.
    https://docs.apollo.io/reference/organization-search
    """
    result = await apollo_client.organization_search(query)
    return result.model_dump() if result else None

@mcp.tool()
async def organization_job_postings(organization_id: str) -> Optional[dict]:
    """
    Use the Organization Job Postings endpoint to find job postings for a specific organization.
    https://docs.apollo.io/reference/organization-jobs-postings
    """
    result = await apollo_client.organization_job_postings(organization_id)
    return result.model_dump() if result else None

@mcp.tool()
async def get_organization(organization_id: str) -> Optional[dict]:
    """
    Get complete organization info by ID. Requires master API key.
    https://docs.apollo.io/reference/get-complete-organization-info
    """
    return await apollo_client.get_organization(organization_id)

@mcp.tool()
async def news_articles_search(query: NewsArticlesSearchQuery) -> Optional[dict]:
    """
    Search news articles related to companies. Consumes credits. organization_ids is required.
    https://docs.apollo.io/reference/news-articles-search
    """
    result = await apollo_client.news_articles_search(query)
    return result.model_dump() if result else None

@mcp.tool()
async def bulk_people_enrichment(
    details: List[dict],
    run_waterfall_email: Optional[bool] = False,
    run_waterfall_phone: Optional[bool] = False,
    reveal_personal_emails: Optional[bool] = False,
    reveal_phone_number: Optional[bool] = False,
    webhook_url: Optional[str] = None,
) -> Optional[dict]:
    """
    Enrich up to 10 people in a single call. Pass details as list of objects with first_name, last_name, email, domain, id, etc. Consumes credits.
    https://docs.apollo.io/reference/bulk-people-enrichment
    """
    from apollo.bulk_enrichment import BulkPeopleEnrichmentRequest, BulkPeopleEnrichmentDetail, BulkPeopleEnrichmentQuery
    body = BulkPeopleEnrichmentRequest(
        details=[BulkPeopleEnrichmentDetail.model_validate(d) for d in details]
    )
    query = BulkPeopleEnrichmentQuery(
        run_waterfall_email=run_waterfall_email,
        run_waterfall_phone=run_waterfall_phone,
        reveal_personal_emails=reveal_personal_emails,
        reveal_phone_number=reveal_phone_number,
        webhook_url=webhook_url,
    )
    return await apollo_client.bulk_people_enrichment(body, query)

@mcp.tool()
async def bulk_organization_enrichment(domains: List[str]) -> Optional[dict]:
    """
    Enrich up to 10 organizations by domain. Consumes credits.
    https://docs.apollo.io/reference/bulk-organization-enrichment
    """
    from apollo.bulk_enrichment import BulkOrganizationEnrichmentQuery
    query = BulkOrganizationEnrichmentQuery(domains=domains)
    return await apollo_client.bulk_organization_enrichment(query)

# if __name__ == "__main__":
#     mcp.run(transport="stdio")
