# Apollo.io MCP Server

This project provides an MCP server that exposes the Apollo.io API functionalities as tools. It allows you to interact with the Apollo.io API using the Model Context Protocol (MCP).

## Overview

The project consists of the following main components:

- `apollo_client.py`: Defines the `ApolloClient` class for interacting with the Apollo.io API. Uses query params (not JSON body) for POST endpoints per [Apollo API docs](https://docs.apollo.io/reference/authentication).
- `server.py`: Defines the FastMCP server exposing Apollo.io API as MCP tools.
- `apollo/`: Data models for the Apollo.io API.

## Functionalities

MCP tools aligned with [Apollo API Reference](https://docs.apollo.io/reference/authentication):

**Enrichment**
- `people_enrichment`: Enrich data for 1 person.
- `bulk_people_enrichment`: Enrich up to 10 people in one call.
- `organization_enrichment`: Enrich data for 1 company.
- `bulk_organization_enrichment`: Enrich up to 10 companies by domain.

**Search**
- `people_search`: People API Search (no credits, no emails/phones). Uses `/mixed_people/api_search`.
- `organization_search`: Organization Search. Uses `/mixed_companies/search`.
- `organization_job_postings`: Job postings for an organization.
- `get_organization`: Complete organization info by ID (requires master API key).
- `news_articles_search`: News articles related to companies.

## Usage

To use this MCP server, you need to:

1. Set the `APOLLO_IO_API_KEY` environment variable with your Apollo.io API key. Or create '.env' file in the project root with `APOLLO_IO_API_KEY`.
2. Get dependencies: `uv sync`
3. Run the `uv run mcp run server.py`

## Data Models

The `apollo/` directory contains the data models for the Apollo.io API. These models are used to define the input and output of the MCP tools.

- `apollo/people.py`: People Enrichment models.
- `apollo/organization.py`: Organization Enrichment models.
- `apollo/people_search.py`: People API Search models.
- `apollo/organization_search.py`: Organization Search models.
- `apollo/organization_job_postings.py`: Organization Job Postings models.
- `apollo/news_articles_search.py`: News Articles Search models.
- `apollo/bulk_enrichment.py`: Bulk People/Organization Enrichment models.

## Testing

To test, set `APOLLO_IO_API_KEY` environment variable and run `uv run apollo_client.py`.

## Usage with Claude for Desktop

1. Configure Claude for Desktop to use these MCP servers by adding them to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "apollo-io-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "mcp",
        "run",
        "path/to/apollo-io-mcp-server/server.py"
      ]
    }
  }
}
```

## Resources

- [Apollo.io API Documentation](https://docs.apollo.io/reference/)
- [MCP Protocol Documentation](https://github.com/modelcontextprotocol/mcp)
- [Claude for Desktop Documentation](https://claude.ai/docs)
