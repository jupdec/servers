from datetime import datetime
from enum import Enum
import json
from typing import Sequence, Dict, Any

from pydantic import BaseModel, Field
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError

class ClusterStatus(str, Enum):
    RUNNING = "Running"
    INITIALIZING = "Initializing"
    STOPPED = "Stopped"
    ERROR = "Error"

class ClusterTools(str, Enum):
    DESCRIBE_CLUSTER = "describe_cluster"
    LIST_CLUSTERS = "list_clusters"

class Cluster(BaseModel):
    id: str = Field(..., description="Unique cluster identifier")
    name: str = Field(..., description="Cluster name")
    status: ClusterStatus = Field(..., description="Current cluster status")
    node_count: int = Field(..., description="Number of nodes in the cluster")
    region: str = Field(..., description="Cloud region where cluster is deployed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Cluster creation timestamp")

class ClusterServer:
    def __init__(self):
        self._clusters: Dict[str, Cluster] = {
            "cluster1": Cluster(
                id="cluster1",
                name="Production Cluster",
                status=ClusterStatus.RUNNING,
                node_count=5,
                region="us-west-2"
            ),
            "cluster2": Cluster(
                id="cluster2",
                name="Staging Cluster",
                status=ClusterStatus.INITIALIZING,
                node_count=3,
                region="us-east-1"
            )
        }

    def describe_cluster(self, cluster_id: str) -> Cluster:
        """Retrieve details of a specific cluster"""
        if cluster_id not in self._clusters: #use eks describe clusters - beta clusters 
            raise McpError(f"Cluster with ID {cluster_id} not found")
        return self._clusters[cluster_id]

    def list_clusters(self) -> list[Cluster]:
        """List all available clusters"""
        return list(self._clusters.values())

async def serve() -> None:
    server = Server("mcp-cluster-management")
    cluster_server = ClusterServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available cluster management tools."""
        return [
            Tool(
                name=ClusterTools.DESCRIBE_CLUSTER.value,
                description="Get detailed information about a specific cluster",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster_id": {
                            "type": "string",
                            "description": "Unique identifier of the cluster to describe"
                        }
                    },
                    "required": ["cluster_id"]
                }
            ),
            Tool(
                name=ClusterTools.LIST_CLUSTERS.value,
                description="List all available clusters",
                inputSchema={}
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for cluster management."""
        try:
            match name:
                case ClusterTools.DESCRIBE_CLUSTER.value:
                    cluster_id = arguments.get("cluster_id")
                    if not cluster_id:
                        raise ValueError("Missing required argument: cluster_id")
                    
                    result = cluster_server.describe_cluster(cluster_id)

                case ClusterTools.LIST_CLUSTERS.value:
                    result = cluster_server.list_clusters()

                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [
                TextContent(
                    type="text", 
                    text=json.dumps(
                        [cluster.model_dump() if isinstance(cluster, Cluster) else cluster 
                         for cluster in (result if isinstance(result, list) else [result])], 
                        indent=2, 
                        default=str
                    )
                )
            ]

        except Exception as e:
            raise ValueError(f"Error processing cluster management query: {str(e)}")

    # Initialize and run the server
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

# Optional: If you want to run this as a standalone script
if __name__ == "__main__":
    import asyncio
    asyncio.run(serve())


