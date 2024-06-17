# start the celery worker
celery -A VideoSearch worker -l INFO
celery -A VideoSearch worker -l info --pool=solo -E 
celery -A VideoSearch worker --loglevel=info

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

# run redis on docker - for windows

docker exec -it redis-stack-server redis-cli

docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

# django commands

python manage.py runserver   