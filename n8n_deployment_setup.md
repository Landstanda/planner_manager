# n8n Deployment Setup on Fly.io

This document details the configuration for the n8n service deployed on Fly.io, which serves as the automation backbone for the Daily Planner AI Agent.

## `fly.toml` Configuration

The following is the `fly.toml` file used for the n8n application (app name: `aphro-email-manager` as per the file, region: `sjc`).

```toml
# fly.toml app configuration file generated for aphro-email-manager on 2025-04-29T10:17:12-07:00
#
# See https://fly.io/docs/reference/configuration/ for information about how to use this file.
#

app = 'aphro-email-manager'
primary_region = 'sjc'

[build]
  # image = 'node:18-alpine' # This is ignored when a Dockerfile is present

[env]
  GENERIC_TIMEZONE = "America/Los_Angeles"

[http_service]
  internal_port = 5678 # Changed from 8080 to n8n's default port
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ['app']

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1

[mounts]
  source = "n8n_data"
  destination = "/home/node/.n8n"
```

## `Dockerfile`

The n8n service is containerized using the following Dockerfile. It uses the official `n8nio/n8n:latest` image and installs the `n8n-nodes-mcp` community node.

```dockerfile
# Dockerfile
# Use the official n8n base image
FROM n8nio/n8n:latest

# Switch to root temporarily if you need to install custom OS packages
# USER root
# RUN apk --no-cache add --virtual build-deps some-package && \
#     npm install -g my-custom-node && \
#     apk del build-deps
# USER node

# n8n listens on port 5678 by default
EXPOSE 5678

# Install the MCP community node
USER root
RUN npm install -g n8n-nodes-mcp  # replace with the actual npm package name if different
USER node 

# Start n8n without the tunnel since we're running on Fly.io
# The tunnel is only needed for local development
CMD ["start"]
```

## Persistent Volume Setup

A persistent volume is configured to ensure n8n data (workflows, credentials, execution logs, etc.) is retained across deployments and restarts.

-   **Volume Name (source):** `n8n_data`
-   **Mount Path (destination):** `/home/node/.n8n` (This is the default data directory for n8n)

This is configured in the `[mounts]` section of the `fly.toml` file.

## Environment Variables & Secrets

Critical configuration and sensitive data are managed via environment variables and secrets in the Fly.io dashboard for the n8n application.

-   **`GENERIC_TIMEZONE`**: Set to `"America/Los_Angeles"` in `fly.toml`.

The following additional environment variables were noted in an example `n8n_docker-compose.yml` and are likely configured as secrets in Fly.io for the n8n app to enable Python integration and other features. The actual values are stored securely in Fly.io.

-   `NODE_FUNCTION_ALLOW_EXTERNAL=epub,pdf.js-extract`
-   `PYTHONUNBUFFERED=1`
-   `PYTHONPATH=/opt/venv/lib/python3.12/site-packages`
-   `N8N_PYTHON_EXECUTABLE=/opt/venv/bin/python3`
-   `N8N_COMMUNITY_NODES_ENABLED=true`
-   `N8N_COMMUNITY_NODES=n8n-nodes-python-function` (Note: The Dockerfile installs `n8n-nodes-mcp`. Ensure your Fly.io secrets and desired community nodes align.)

It's important to ensure that the community nodes enabled via environment variables match those installed in the Dockerfile or available in the base n8n image. 