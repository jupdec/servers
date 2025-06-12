# Cluster MCP Server

A Model Context Protocol server that provides details of clusters. This server enables LLMs to get cluster information opening opportunitites to perform any actions on clusters as the tools are expanded.

### Available Tools

- `describe_cluster` - Get current time in a specific timezone or system timezone.
  - Required arguments:
    - `cluster name` (string): sample cluster name like "cluster2"

- `list_clusters` - Lists all available clusters
  

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-cluster*.

### Using PIP

Alternatively you can install `mcp-server-cluster` via pip:

```bash
pip install mcp-server-cluster
```

After installation, you can run it as a script using:

```bash
python -m mcp_server_cluster
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-cluster"]
    }
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
{
  "mcpServers": {
    "time": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/cluster"]
    }
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
{
  "mcpServers": {
    "time": {
      "command": "python",
      "args": ["-m", "mcp_server_cluster"]
    }
  }
}
```
</details>

### Configure for Zed

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "mcp-server-cluster": {
    "command": "uvx",
    "args": ["mcp-server-cluster"]
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "mcp-server-cluster": {
    "command": "python",
    "args": ["-m", "mcp_server_cluster"]
  }
},
```
</details>

### Configure for VS Code

For quick installation, use one of the one-click install buttons below...

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=time&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-cluster%22%5D%7D) [![Install with UV in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-UV-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=time&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-cluster%22%5D%7D&quality=insiders)

[![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=time&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Ftime%22%5D%7D) [![Install with Docker in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Docker-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=time&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Ftime%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open User Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is needed when using the `mcp.json` file.

<details>
<summary>Using uvx</summary>

```json
{
  "mcp": {
    "servers": {
      "cluster": {
        "command": "uvx",
        "args": ["mcp-server-cluster"]
      }
    }
  }
}
```
</details>

<details>
<summary>Using Docker</summary>

```json
{
  "mcp": {
    "servers": {
      "cluster": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "mcp/time"]
      }
    }
  }
}
```
</details>

### Customization - System Timezone

By default, the server automatically detects your system's timezone. You can override this by adding the argument `--local-timezone` to the `args` list in the configuration.

Example:
```json
{
  "command": "python",
  "args": ["-m", "mcp_server_cluster"]
}
```

## Example Interactions

1. Get current time:
```json
{
  "name": "describe_cluster",
  "arguments": {
    "timezone": "cluster2"
  }
}
```
Response:
```json
{
    "id": "cluster2",
    "name": "Staging Cluster",
    "status": "Initializing",
    "node_count": 3,
    "region": "us-east-1",
    "created_at": "2025-06-12 18:30:43.125684"
  }
```

2. List all clusters:
```json
{
  "name": "list_clusters",
}
```
Response:
```json
  [{
    "id": "cluster1",
    "name": "Production Cluster",
    "status": "Running",
    "node_count": 5,
    "region": "us-west-2",
    "created_at": "2025-06-12 18:30:43.125665"
  },
  {
    "id": "cluster2",
    "name": "Staging Cluster",
    "status": "Initializing",
    "node_count": 3,
    "region": "us-east-1",
    "created_at": "2025-06-12 18:30:43.125684"
  }
]
```

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-cluster
```

Or if you've installed the package in a specific directory or are developing on it:

```bash
cd path/to/servers/src/time
npx @modelcontextprotocol/inspector uv run mcp-server-cluster
```

## Examples of Questions for Claude

1. "What time is it now?" (will use system timezone)
2. "What time is it in Tokyo?"
3. "When it's 4 PM in New York, what time is it in London?"
4. "Convert 9:30 AM Tokyo time to New York time"

## Build

Docker build:

```bash
cd src/time
docker build -t mcp/cluster .
```

## Contributing

We encourage contributions to help expand and improve mcp-server-cluster. Whether you want to add new time-related tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements to make mcp-server-cluster even more powerful and useful.

## License

mcp-server-cluster is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
