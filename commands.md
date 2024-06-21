# start the celery worker
celery -A VideoSearch worker -l INFO
celery -A VideoSearch worker -l info --pool=solo -E 
celery -A VideoSearch worker --loglevel=info
celery -A VideoSearch worker -l info --pool=solo -E --concurrency=4

# check the status of celery worker
celery inspect active_queues

celery inspect active

celery status  

# linux commands 

sudo apt update

# install cceextractor

sudo apt install ccextractor

pip install celery[redis]

# install and start redis server

sudo apt install redis-server

sudo service redis-server start

sudo service redis-server status

redis-cli ping

redis://:password@hostname:port/db_number

# run redis on docker - for windows

docker exec -it redis-stack-server redis-cli

docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

# docker commands

docker build . -t videosearch

docker run -p 8000:8000 videosearch gunicorn -b 0.0.0.0:8000 VideoSearch.wsgi:application

# render

python -m gunicorn VideoSearch.asgi:application -k uvicorn.workers.UvicornWorker



# django commands

python manage.py runserver   