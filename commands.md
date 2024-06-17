celery -A VideoSearch worker -l INFO
celery -A VideoSearch worker -l info --pool=solo -E 

docker exec -it redis-stack-server redis-cli

docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

celery inspect active_queues

celery inspect active

celery status  

python manage.py runserver   