# Infrastructure

Docker and deployment configurations.

| File | Purpose | Phase |
|------|---------|-------|
| `docker-compose.yml` | Local dev stack (api, worker, postgres, qdrant, redis) | Phase 9 |
| `docker-compose.prod.yml` | Production overrides | Phase 12 |
| `docker/Dockerfile.api` | API container | Phase 9 |
| `docker/Dockerfile.worker` | Worker container | Phase 9 |
| `docker/Dockerfile.web` | Web UI container | Phase 9 |

Start local stack: `make dev`
