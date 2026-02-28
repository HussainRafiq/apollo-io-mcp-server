from typing import Optional, List
from pydantic import BaseModel, Field


class BulkPeopleEnrichmentDetail(BaseModel):
    """Identifying information for one person in a bulk enrichment request. At least one field is required."""

    first_name: Optional[str] = Field(
        default=None,
        description=(
            "First name of the person. Combine with `last_name` and `domain` for better "
            "matching accuracy when an email or LinkedIn URL is not available. Example: 'Tim'"
        ),
    )
    last_name: Optional[str] = Field(
        default=None,
        description=(
            "Last name of the person. Combine with `first_name` and `domain` for better "
            "matching accuracy when an email or LinkedIn URL is not available. Example: 'Zheng'"
        ),
    )
    name: Optional[str] = Field(
        default=None,
        description=(
            "Full name of the person (first and last name). Use this as an alternative to "
            "providing `first_name` and `last_name` separately. Example: 'Tim Zheng'"
        ),
    )
    email: Optional[str] = Field(
        default=None,
        description=(
            "Work or personal email address of the person. Providing an email address "
            "yields the highest match accuracy of all identifying fields. "
            "Example: 'tim@apollo.io'"
        ),
    )
    hashed_email: Optional[str] = Field(
        default=None,
        description=(
            "MD5 or SHA-256 hash of the person's email address. Use this when you have a "
            "hashed email rather than a plain-text email address. "
            "MD5 example: '8d935115b9ff4489f2d1f9249503cadf'. "
            "SHA-256 example: '97817c0c49994eb500ad0a5e7e2d8aed51977b26424d508f66e4e8887746a152'"
        ),
    )
    organization_name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the person's current or past employer. Use in combination with "
            "`first_name` and `last_name` to improve match accuracy. Example: 'Apollo'"
        ),
    )
    domain: Optional[str] = Field(
        default=None,
        description=(
            "Primary web domain of the person's current or past employer. Do not include "
            "'www.', '@', 'http://', or 'https://' prefixes. Use in combination with name "
            "fields to improve match accuracy. Example: 'apollo.io'"
        ),
    )
    id: Optional[str] = Field(
        default=None,
        description=(
            "Apollo's unique person ID. Providing this gives a direct, exact match with no "
            "ambiguity. Obtain this ID from the `id` field in responses from `people_search` "
            "or `people_enrichment`. Example: '587cf802f65125cad923a266'"
        ),
    )
    linkedin_url: Optional[str] = Field(
        default=None,
        description=(
            "Full URL of the person's LinkedIn profile. Providing this yields very high "
            "match accuracy, second only to providing a direct Apollo person ID. "
            "Example: 'https://www.linkedin.com/in/tim-zheng-677ba010'"
        ),
    )


class BulkPeopleEnrichmentRequest(BaseModel):
    """Request body for the Bulk People Enrichment API call."""

    details: List[BulkPeopleEnrichmentDetail] = Field(
        description=(
            "List of up to 10 people to enrich. Each object must include at least one "
            "identifying field. Recommended combinations for best match accuracy: "
            "(1) `email` alone, (2) `linkedin_url` alone, (3) `id` (Apollo person ID) alone, "
            "(4) `first_name` + `last_name` + `domain`. "
            "Apollo person IDs can be obtained from `people_search` or `people_enrichment`."
        )
    )


class BulkPeopleEnrichmentQuery(BaseModel):
    """Optional query parameters for the Bulk People Enrichment API call."""

    run_waterfall_email: Optional[bool] = Field(
        default=False,
        description=(
            "Set to true to enable waterfall email enrichment, which tries multiple data "
            "sources sequentially to find an email for each person. May consume additional "
            "credits beyond the base enrichment cost. Default: false."
        ),
    )
    run_waterfall_phone: Optional[bool] = Field(
        default=False,
        description=(
            "Set to true to enable waterfall phone enrichment, which tries multiple data "
            "sources sequentially to find a phone number for each person. May consume "
            "additional credits beyond the base enrichment cost. Default: false."
        ),
    )
    reveal_personal_emails: Optional[bool] = Field(
        default=False,
        description=(
            "Set to true to include personal (non-work) email addresses in enrichment "
            "results. Consumes additional credits per person. People in GDPR-compliant "
            "regions will not have personal emails revealed regardless of this setting. "
            "Default: false."
        ),
    )
    reveal_phone_number: Optional[bool] = Field(
        default=False,
        description=(
            "Set to true to include phone numbers (including mobile numbers) in enrichment "
            "results. Consumes additional credits per person. When set to true, you MUST also "
            "provide a `webhook_url` — Apollo verifies and delivers phone numbers "
            "asynchronously to that URL and they will NOT appear in the direct API response. "
            "Default: false."
        ),
    )
    webhook_url: Optional[str] = Field(
        default=None,
        description=(
            "Required when `reveal_phone_number` is true; otherwise omit. The HTTPS URL "
            "where Apollo will POST a JSON payload containing verified phone numbers for all "
            "matched people. Delivery is asynchronous and may take several minutes after the "
            "initial API response. Example: 'https://webhook.site/your-unique-id'"
        ),
    )


class BulkOrganizationEnrichmentQuery(BaseModel):
    """Query parameters for the Bulk Organization Enrichment API call."""

    domains: List[str] = Field(
        description=(
            "List of up to 10 company domains to enrich. Each domain must be the plain "
            "primary web domain of the company — without 'www.', '@', 'http://', or "
            "'https://' prefixes. Each domain is matched and enriched independently. "
            "Unmatched domains return null rather than raising an error. "
            "Examples: ['apollo.io', 'microsoft.com', 'salesforce.com']"
        )
    )
