from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from .config import settings

from .cli import cli

REQUEST_TIMEOUT_SECONDS = 60

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url="https://gitlab.com/api/graphql",
    headers={"Authorization": f"Bearer {settings.gitlab.token}"},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, execute_timeout=REQUEST_TIMEOUT_SECONDS)

# Provide a GraphQL query
query = gql(
    """
    query {
      project(fullPath: "fireblocks/core") {
        id
        name
        pipelines (ref: "master", status: FAILED) {
          nodes {
            source
            ref
            createdAt
            mergeRequest {
              id
            }
            job(name: "py_test_services: [exchange_service]") {
              id
              status
            }
            testReportSummary {
              testSuites {
                nodes {
                  buildIds
                  failedCount
                  name
                }
              }
            }
          }
        }
      }
    }
    """
)

# Execute the query on the transport
# result = client.execute(query)
# print(result)


cli()
