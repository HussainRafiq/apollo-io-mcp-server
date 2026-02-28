from typing import Optional, List, Annotated
from mcp.server.fastmcp import FastMCP
from apollo_client import ApolloClient
from apollo import *
from pydantic import Field

import os

from dotenv import load_dotenv
load_dotenv()

apollo_client = ApolloClient(api_key=os.getenv("APOLLO_IO_API_KEY"))

mcp = FastMCP("Apollo.io")


@mcp.tool()
async def people_enrichment(query: PeopleEnrichmentQuery) -> Optional[dict]:
    """
    Enrich data for a single person using the Apollo People Enrichment API.

    Use this tool when you already have some identifying information about a person
    (name, email, LinkedIn URL, or Apollo person ID) and want to retrieve their full
    profile — including current job title, employer, location, contact details, social
    links, and employment history.

    At least one identifying field must be provided in the query. The more fields you
    supply, the more accurate and confident the match will be. Providing `email` or
    `linkedin_url` typically yields the highest match confidence.

    Returned data includes:
    - Name, title, headline, photo
    - Current and past employer details (name, domain, LinkedIn)
    - Email address and status (if available)
    - LinkedIn, Twitter, GitHub, Facebook URLs
    - Location (city, state, country)
    - Employment history
    - Organization details

    Credit usage:
    - No credits consumed unless `reveal_personal_emails` or `reveal_phone_number` is true.
    - Setting `reveal_phone_number` to true requires a `webhook_url` as phone results
      are delivered asynchronously by Apollo.

    Reference: https://docs.apollo.io/reference/people-enrichment
    """
    result = await apollo_client.people_enrichment(query)
    return result.model_dump() if result else None


@mcp.tool()
async def organization_enrichment(query: OrganizationEnrichmentQuery) -> Optional[dict]:
    """
    Enrich data for a single organization (company) using the Apollo Organization Enrichment API.

    Use this tool when you know a company's primary web domain and want to retrieve a
    comprehensive company profile. This is useful for account research, qualifying leads,
    or populating CRM records with firmographic data.

    The `domain` field is required. It must be the plain primary domain of the company
    (e.g., "apollo.io", "microsoft.com"). Do not include "www.", "@", "http://", or
    any other prefix.

    Returned data includes:
    - Basic info: company name, website, LinkedIn, Twitter, Facebook URLs
    - Financials: annual revenue, total funding, latest funding round, funding events
    - People: estimated employee count, departmental headcount breakdown
    - Technology stack: list of currently used technologies with categories
    - Location: HQ street address, city, state, postal code, country
    - Industries and keyword tags
    - Org chart information

    The `id` field in the response is the Apollo organization ID, which can be passed
    to `organization_job_postings`, `get_organization`, and `news_articles_search`.

    Credit usage: This endpoint does NOT consume credits.

    Reference: https://docs.apollo.io/reference/organization-enrichment
    """
    result = await apollo_client.organization_enrichment(query)
    return result.model_dump() if result else None


@mcp.tool()
async def people_search(query: PeopleSearchQuery) -> Optional[dict]:
    """
    Search for people (contacts / leads) in the Apollo database using various filters.

    Use this tool for prospecting — finding net-new people that match criteria such as
    job title, seniority level, personal location, employer location, company size, or
    employer domain. This is ideal for building targeted lead lists before enriching
    individual people with `people_enrichment`.

    Key notes:
    - Results do NOT include email addresses or direct phone numbers. No credits are
      consumed. To get contact details for a specific person, pass their Apollo person
      ID (the `id` field in results) to `people_enrichment`.
    - To filter by specific target companies using Apollo IDs, populate `organization_ids`.
      First call `organization_search` to find the companies and extract their `id` values,
      then pass those IDs here.
    - To filter by company domain instead of Apollo ID, use `q_organization_domains_list`.
    - Use `page` and `per_page` together to paginate through large result sets.
    - Combining `person_titles` with `person_seniorities` gives the most precise results
      for targeting specific job functions at specific levels.

    Returned data per person:
    - Name, title, headline, LinkedIn URL, photo
    - Current employer name and domain
    - Location (city, state, country)
    - Seniority, departments, subdepartments
    - Apollo person ID (use this in `people_enrichment` or `bulk_people_enrichment`)

    Credit usage: This endpoint does NOT consume credits.

    Reference: https://docs.apollo.io/reference/people-api-search
    """
    result = await apollo_client.people_search(query)
    return result.model_dump() if result else None


@mcp.tool()
async def organization_search(query: OrganizationSearchQuery) -> Optional[dict]:
    """
    Search for organizations (companies) in the Apollo database using various filters.

    Use this tool to find target accounts that match firmographic criteria such as
    employee headcount range, HQ location, revenue range, technology stack, or keyword
    tags. This is the primary way to build lists of target companies for outbound sales,
    research, or account-based marketing.

    Key notes:
    - The `id` field in each returned organization is the Apollo organization ID. Save
      these IDs to use in other tools:
        * `organization_job_postings` — get job openings at that company
        * `get_organization` — get full detailed company profile
        * `news_articles_search` — get news articles about that company
        * `people_search` (via `organization_ids`) — find people at that company
        * `bulk_organization_enrichment` (via domains) — enrich multiple companies at once
    - Use `page` and `per_page` for pagination through large result sets.
    - Revenue values must be plain integers without currency symbols, commas, or decimals.
    - Technology UIDs use underscores for spaces and periods (e.g., "google_analytics",
      "wordpress_org"). Download the full list from Apollo's supported technologies CSV.

    Returned data per organization:
    - Name, website URL, LinkedIn URL, primary domain
    - Employee count estimate, industry, keyword tags
    - HQ location (city, state, country)
    - Technologies in use
    - Apollo organization ID (critical for use in other tools)

    Credit usage: This endpoint does NOT consume credits.

    Reference: https://docs.apollo.io/reference/organization-search
    """
    result = await apollo_client.organization_search(query)
    return result.model_dump() if result else None


@mcp.tool()
async def organization_job_postings(
    organization_id: Annotated[
        str,
        Field(
            description=(
                "The unique Apollo ID for the organization whose active job postings you want "
                "to retrieve. Each company in the Apollo database is assigned a unique string ID. "
                "To obtain this ID, you must first identify the organization using one of these "
                "approaches: "
                "(1) Call `organization_search` with filters like company name, location, or "
                "industry — then extract the `id` field from the returned organization objects. "
                "(2) Call `organization_enrichment` with the company's domain — then extract "
                "the `id` field from the returned organization object. "
                "Example value: '5e66b6381e05b4008c8331b8'"
            )
        ),
    ],
) -> Optional[dict]:
    """
    Retrieve all currently active job postings for a specific organization by its Apollo ID.

    Use this tool to discover what roles a company is actively hiring for. This is useful
    for sales intelligence (e.g., identifying companies expanding a specific department),
    recruiting research, or tracking company growth signals.

    IMPORTANT — You must supply a valid Apollo `organization_id`. This is NOT the company
    name or domain. To get the ID:
    1. Call `organization_search` (filter by name, location, industry, etc.) and copy the
       `id` field from the matching organization in the response.
    2. Or call `organization_enrichment` with the company domain and copy the `id` field
       from the returned organization object.

    Returned data per job posting:
    - Job title
    - Posting URL (link to the original job listing)
    - Location: city, state, country
    - Dates: when the posting was first seen (`posted_at`) and last verified (`last_seen_at`)

    Credit usage: This endpoint does NOT consume credits.

    Reference: https://docs.apollo.io/reference/organization-jobs-postings
    """
    result = await apollo_client.organization_job_postings(organization_id)
    return result.model_dump() if result else None


@mcp.tool()
async def get_organization(
    organization_id: Annotated[
        str,
        Field(
            description=(
                "The unique Apollo ID for the organization you want complete details on. "
                "Each company in the Apollo database is assigned a unique string ID. "
                "To obtain this ID, you must first identify the organization using one of these "
                "approaches: "
                "(1) Call `organization_search` with filters like company name, location, or "
                "industry — then extract the `id` field from the returned organization objects. "
                "(2) Call `organization_enrichment` with the company's domain — then extract "
                "the `id` field from the returned organization object. "
                "Example value: '5e66b6381e05b4008c8331b8'. "
                "NOTE: This endpoint requires a master-level Apollo API key and will return "
                "an error if called with a standard API key."
            )
        ),
    ],
) -> Optional[dict]:
    """
    Retrieve the complete, detailed organization profile by Apollo organization ID.
    Requires a master-level Apollo API key.

    Use this tool when you need the most comprehensive company data available in Apollo,
    including all fields that are not returned by `organization_enrichment`. This is
    suitable for deep account research or populating detailed CRM records.

    IMPORTANT — You must supply a valid Apollo `organization_id`. This is NOT the company
    name or domain. To get the ID:
    1. Call `organization_search` (filter by name, location, industry, etc.) and copy the
       `id` field from the matching organization in the response.
    2. Or call `organization_enrichment` with the company domain and copy the `id` field
       from the returned organization object.

    NOTE: This endpoint requires a master-level Apollo API key. It will return an
    authorization error if called with a standard (non-master) API key.

    Returned data includes all organization fields:
    - Full company profile: name, website, social URLs, description
    - Financials: revenue, funding rounds, funding stage
    - Headcount: total estimated employees, departmental breakdown
    - Technology stack
    - HQ address and contact details
    - Org chart data and industry tags

    Credit usage: This endpoint does NOT consume credits.

    Reference: https://docs.apollo.io/reference/get-complete-organization-info
    """
    return await apollo_client.get_organization(organization_id)


@mcp.tool()
async def news_articles_search(query: NewsArticlesSearchQuery) -> Optional[dict]:
    """
    Search for news articles related to one or more organizations using the Apollo News API.

    Use this tool to find recent news coverage, press releases, and business events
    (such as funding rounds, executive hires, product launches, partnerships, or contracts)
    for target companies. This is useful for sales intelligence, pre-call research, and
    identifying trigger events for outreach.

    IMPORTANT — `organization_ids` is REQUIRED. You must provide at least one valid Apollo
    organization ID. To get organization IDs:
    1. Call `organization_search` with filters like company name, location, or industry,
       then extract the `id` field from the returned organization objects.
    2. Or call `organization_enrichment` with the company domain and extract the `id`
       from the returned organization object.

    Optional filters:
    - `categories`: filter by event type, e.g., "hires", "investment", "contract",
      "partnership", "product_launch". Omit to retrieve all news types.
    - `published_at_min` / `published_at_max`: restrict articles to a date range
      (format: YYYY-MM-DD). Use both together for a bounded range, or either alone for
      an open-ended range.
    - `page` / `per_page`: paginate through large result sets.

    Returned data per article:
    - Title and snippet (summary excerpt)
    - Article URL
    - Domain of the news source
    - Publication date
    - Event categories associated with the article
    - Apollo organization IDs linked to the article

    Credit usage: This endpoint CONSUMES credits on each call.

    Reference: https://docs.apollo.io/reference/news-articles-search
    """
    result = await apollo_client.news_articles_search(query)
    return result.model_dump() if result else None


@mcp.tool()
async def bulk_people_enrichment(
    details: Annotated[
        List[dict],
        Field(
            description=(
                "A list of up to 10 people to enrich in a single call. Each item is a dict "
                "containing identifying fields for one person. At least one identifying field "
                "is required per person — providing more fields improves match accuracy. "
                "Supported fields per person dict: "
                "`first_name` (str) — person's first name; "
                "`last_name` (str) — person's last name; "
                "`name` (str) — full name, use instead of first_name + last_name; "
                "`email` (str) — work or personal email; highest match accuracy; "
                "`hashed_email` (str) — MD5 or SHA-256 hash of the email address; "
                "`organization_name` (str) — current or past employer name; "
                "`domain` (str) — employer domain without www/@ prefix, e.g. 'apollo.io'; "
                "`id` (str) — Apollo person ID; obtain from the `id` field in responses "
                "from `people_search` or `people_enrichment`; "
                "`linkedin_url` (str) — full LinkedIn profile URL; very high match accuracy. "
                "Example: [{'first_name': 'Tim', 'last_name': 'Zheng', 'domain': 'apollo.io'}, "
                "{'email': 'jane@microsoft.com'}]"
            )
        ),
    ],
    run_waterfall_email: Annotated[
        Optional[bool],
        Field(
            description=(
                "Set to true to enable waterfall email enrichment, which tries multiple data "
                "sources sequentially to find an email address for each person. This may "
                "consume additional credits beyond the base enrichment cost. Default: false."
            )
        ),
    ] = False,
    run_waterfall_phone: Annotated[
        Optional[bool],
        Field(
            description=(
                "Set to true to enable waterfall phone enrichment, which tries multiple data "
                "sources sequentially to find a phone number for each person. This may consume "
                "additional credits beyond the base enrichment cost. Default: false."
            )
        ),
    ] = False,
    reveal_personal_emails: Annotated[
        Optional[bool],
        Field(
            description=(
                "Set to true to include personal (non-work) email addresses in enrichment "
                "results. Consumes additional credits per person. People located in "
                "GDPR-compliant regions will not have personal emails revealed regardless "
                "of this setting. Default: false."
            )
        ),
    ] = False,
    reveal_phone_number: Annotated[
        Optional[bool],
        Field(
            description=(
                "Set to true to include phone numbers (including mobile numbers) in enrichment "
                "results. Consumes additional credits per person. When set to true, you MUST "
                "also provide a `webhook_url` — Apollo verifies and delivers phone numbers "
                "asynchronously to that URL (may take several minutes). Default: false."
            )
        ),
    ] = False,
    webhook_url: Annotated[
        Optional[str],
        Field(
            description=(
                "Required when `reveal_phone_number` is true; otherwise omit this field. "
                "The HTTPS URL where Apollo will POST a JSON response containing the enriched "
                "phone numbers for all matched people. Phone verification is asynchronous "
                "and the webhook may be called minutes after the initial API response. "
                "Example: 'https://webhook.site/your-unique-id'"
            )
        ),
    ] = None,
) -> Optional[dict]:
    """
    Enrich up to 10 people in a single API call using the Apollo Bulk People Enrichment API.

    Use this tool when you need to enrich multiple people at once to minimize the number
    of API calls. Each person in the `details` list is matched and enriched independently.
    This is more efficient than calling `people_enrichment` repeatedly for each person.

    Key notes:
    - Maximum 10 people per call. For lists larger than 10, split into multiple calls.
    - Each person entry must have at least one identifying field. Best practice is to
      provide `email` or `linkedin_url` for highest match accuracy, or `first_name` +
      `last_name` + `domain` as a fallback combination.
    - Apollo person IDs (the `id` field in each person dict) can be obtained from
      `people_search` results or from previous `people_enrichment` responses.
    - If `reveal_phone_number` is true, you MUST also provide a valid `webhook_url`.
      The enrichment API response will NOT include phone numbers directly — they are
      sent asynchronously to the webhook URL.
    - Results are returned per-person in the same order as the input `details` list.

    Credit usage: This endpoint CONSUMES credits for each person successfully matched.

    Reference: https://docs.apollo.io/reference/bulk-people-enrichment
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
async def bulk_organization_enrichment(
    domains: Annotated[
        List[str],
        Field(
            description=(
                "A list of up to 10 company domains to enrich in a single call. Each domain "
                "must be the primary web domain of the company — plain, without 'www.', '@', "
                "'http://', or 'https://' prefixes. Each domain is enriched independently "
                "and returns a full organization profile including headcount, funding history, "
                "technology stack, revenue range, industry, and HQ location. "
                "If a domain cannot be matched in the Apollo database, that entry will return "
                "null or an empty result — no error is thrown for unmatched domains. "
                "Examples: ['apollo.io', 'microsoft.com', 'salesforce.com']"
            )
        ),
    ],
) -> Optional[dict]:
    """
    Enrich up to 10 organizations by domain in a single API call using the Apollo Bulk
    Organization Enrichment API.

    Use this tool when you have a list of company domains and want to retrieve full
    company profiles for all of them efficiently, instead of calling `organization_enrichment`
    one by one for each domain.

    Key notes:
    - Maximum 10 domains per call. For lists larger than 10, split into multiple calls.
    - Domains must be plain primary domains (e.g., 'apollo.io'), without any protocol,
      subdomain prefix (www), or path.
    - Each successfully matched domain returns a complete organization profile identical
      in structure to the `organization_enrichment` response.
    - Unmatched domains return null/empty for that entry rather than raising an error.
    - The `id` field in each returned organization can be used in `organization_job_postings`,
      `get_organization`, `news_articles_search`, and `people_search` (via `organization_ids`).

    Credit usage: This endpoint CONSUMES credits for each organization successfully matched.

    Reference: https://docs.apollo.io/reference/bulk-organization-enrichment
    """
    from apollo.bulk_enrichment import BulkOrganizationEnrichmentQuery
    query = BulkOrganizationEnrichmentQuery(domains=domains)
    return await apollo_client.bulk_organization_enrichment(query)


# if __name__ == "__main__":
#     mcp.run(transport="stdio")
