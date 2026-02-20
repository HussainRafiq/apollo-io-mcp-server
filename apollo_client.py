from typing import Optional, List, Any, Dict
import httpx

from apollo import *


def _organization_search_params(query: OrganizationSearchQuery) -> Dict[str, Any]:
    """Build query params for Apollo mixed_companies/search (expects query string, not JSON body)."""
    raw = query.model_dump(exclude_none=True)
    # Apollo OpenAPI uses query params; array params use bracket notation e.g. organization_num_employees_ranges[]
    array_keys = {
        "organization_num_employees_ranges",
        "organization_locations",
        "organization_not_locations",
        "currently_using_any_of_technology_uids",
        "q_organization_keyword_tags",
        "organization_ids",
    }
    params: Dict[str, Any] = {}
    for key, value in raw.items():
        if key in array_keys and isinstance(value, list):
            params[f"{key}[]"] = value
        elif key == "revenue_range_min":
            params["revenue_range[min]"] = value
        elif key == "revenue_range_max":
            params["revenue_range[max]"] = value
        else:
            params[key] = value
    return params


class ApolloClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/api/v1"
        self.headers = {
            "accept": "application/json",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    async def people_enrichment(self, query: PeopleEnrichmentQuery) -> Optional[PeopleEnrichmentResponse]:
        """
        Use the People Enrichment endpoint to enrich data for 1 person.
        https://docs.apollo.io/reference/people-enrichment
        """
        url = f"{self.base_url}/people/match"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return PeopleEnrichmentResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_enrichment(self, query: OrganizationEnrichmentQuery) -> Optional[OrganizationEnrichmentResponse]:
        """
        Use the Organization Enrichment endpoint to enrich data for 1 company.
        https://docs.apollo.io/reference/organization-enrichment
        """
        url = f"{self.base_url}/organizations/enrich"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return OrganizationEnrichmentResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def people_search(self, query: PeopleSearchQuery) -> Optional[PeopleSearchResponse]:
        """
        Use the People Search endpoint to find people.
        https://docs.apollo.io/reference/people-search
        """
        url = f"{self.base_url}/mixed_people/search"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query.model_dump(), headers=self.headers)
            if response.status_code == 200:
                return PeopleSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_search(self, query: OrganizationSearchQuery) -> Optional[OrganizationSearchResponse]:
        """
        Use the Organization Search endpoint to find organizations.
        https://docs.apollo.io/reference/organization-search
        Apollo expects query string parameters (not JSON body) for this POST endpoint.
        """
        url = f"{self.base_url}/mixed_companies/search"
        # Apollo API expects query params; use bracket notation for array keys per OpenAPI spec
        params = _organization_search_params(query)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return OrganizationSearchResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    async def organization_job_postings(self, organization_id: str) -> Optional[OrganizationJobPostingsResponse]:
        """
        Use the Organization Job Postings endpoint to find job postings for a specific organization.
        https://docs.apollo.io/reference/organization-jobs-postings
        """
        url = f"{self.base_url}/organizations/{organization_id}/job_postings"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return OrganizationJobPostingsResponse(**response.json())
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

# Example usage (you'll need to set the APOLLO_IO_API_KEY environment variable)
async def main():
    import os

    api_key = os.getenv('APOLLO_IO_API_KEY')  # Replace with your actual API key or use os.getenv("APOLLO_IO_API_KEY")
    client = ApolloClient(api_key)

    # Example People Enrichment
    people_enrichment_query = PeopleEnrichmentQuery(
        first_name="Tim",
        last_name="Zheng",
    )
    people_enrichment_response = await client.people_enrichment(people_enrichment_query)

    if people_enrichment_response:
        print("People Enrichment Response:", people_enrichment_response.model_dump_json(indent=2))
    else:
        print("People Enrichment failed.")

    # Example Organization Enrichment
    organization_enrichment_query = OrganizationEnrichmentQuery(
        domain="apollo.io",
    )
    organization_enrichment_response = await client.organization_enrichment(organization_enrichment_query)

    if organization_enrichment_response:
        print("Organization Enrichment Response:", organization_enrichment_response.model_dump_json(indent=2))
    else:
        print("Organization Enrichment failed.")

    # Example People Search
    people_search_query = PeopleSearchQuery(
        person_titles=["Marketing Manager"],
        person_seniorities=["vp"],
        q_organization_domains_list=["apollo.io"]
    )
    people_search_response = await client.people_search(people_search_query)

    if people_search_response:
        print("People Search Response:", people_search_response.model_dump_json(indent=2))
    else:
        print("People Search failed.")

    # Example Organization Search
    organization_search_query = OrganizationSearchQuery(
        organization_num_employees_ranges=["250,1000"],
        organization_locations=["japan", "ireland"]
    )
    organization_search_response = await client.organization_search(organization_search_query)

    if organization_search_response:
        print("Organization Search Response:", organization_search_response.model_dump_json(indent=2))
    else:
        print("Organization Search failed.")

    # Example Organization Job Postings
    organization_job_postings_response = await client.organization_job_postings(organization_id="5e66b6381e05b4008c8331b8")

    if organization_job_postings_response:
        print("Organization Job Postings Response:", organization_job_postings_response.model_dump_json(indent=2))
    else:
        print("Organization Job Postings failed.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
