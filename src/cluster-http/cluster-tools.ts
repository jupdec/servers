import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

// Define cluster status enum
enum ClusterStatus {
    RUNNING = "Running",
    INITIALIZING = "Initializing",
    STOPPED = "Stopped",
    ERROR = "Error"
}

// Define cluster model
interface Cluster {
    id: string;
    name: string;
    status: ClusterStatus;
    nodeCount: number;
    region: string;
    createdAt: string;
}

// Sample cluster data
const clusters: Record<string, Cluster> = {
    "cluster1": {
        id: "cluster1",
        name: "Production Cluster",
        status: ClusterStatus.RUNNING,
        nodeCount: 5,
        region: "us-west-2",
        createdAt: new Date().toISOString()
    },
    "cluster2": {
        id: "cluster2",
        name: "Staging Cluster",
        status: ClusterStatus.INITIALIZING,
        nodeCount: 3,
        region: "us-east-1",
        createdAt: new Date().toISOString()
    }
};

// Define the schema for list-clusters
export const listClustersSchema = z.object({});

// Define the schema for describe-clusters
export const describeClusterSchema = z.object({
    clusterId: z.string().describe("Unique identifier of the cluster to describe")
});

// Function to list all clusters
export function listClusters(): Cluster[] {
    return Object.values(clusters);
}

// Function to describe a specific cluster
export function describeCluster(params: z.infer<typeof describeClusterSchema>): Cluster {
    const { clusterId } = params;
    const cluster = clusters[clusterId];

    if (!cluster) {
        throw new Error(`Cluster with ID ${clusterId} not found`);
    }

    return cluster;
}

// Export JSON schemas for use in MCP tool definitions
export const listClustersJsonSchema = zodToJsonSchema(listClustersSchema);
export const describeClusterJsonSchema = zodToJsonSchema(describeClusterSchema);