# docker-spawner

Hello world project of a docker-spawner (not docker in docker)

## What it does

- Based on an API call it spawns a docker container based on a Dockerfile
- The new container is added to the docker compose network of the spawner
- The spawner tests connectivity by calling the API of the spawned container

## How to run

```bash
docker-compose up
```
