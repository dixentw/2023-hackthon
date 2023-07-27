# 2023 Hackerthon

A natural language client for users who want to send pushes via smartnews push platform

1. Replace API_KEY in Dockerfile with the key
2. local run with `docker_compose up --build`
3. Client call:

```
curl --location 'localhost:8000' \
--header 'Content-Type: application/json' \
--data '{
    "condition" : "the push type is dixen verification push, and the link would be www.google.com, with specific targeting to abtest variant id 457"
}'
```
