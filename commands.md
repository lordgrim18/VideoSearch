celery -A VideoSearch worker -l INFO

docker exec -it redis-stack-server redis-cli

docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest