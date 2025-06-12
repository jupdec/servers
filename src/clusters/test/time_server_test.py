import asyncio

async def test_cluster_server():
    cluster_server = ClusterServer()
    
    # Test describe cluster
    cluster = cluster_server.describe_cluster("cluster1")
    print("Describe Cluster:", cluster)
    
    # Test list clusters
    clusters = cluster_server.list_clusters()
    print("List Clusters:", clusters)

# Run the test
asyncio.run(test_cluster_server())