# [Video Subtitle Processing and Search Application](http://65.2.179.201/)

This project is a web application that allows users to upload videos, process them to extract subtitles, and then search for specific keywords within the subtitles. The subtitles are extracted using the `ccextractor` binary and stored in AWS DynamoDB, while the videos are stored in AWS S3. The backend is built with Django and uses Celery for background tasks.

The application is deployed on an AWS EC2 instance and can be accessed at [http://65.2.179.201/](http://65.2.179.201/).

The latency of the application was tested repeatedly and each time the application responded with a time of less than 1 second. The application was able to handle multiple requests simultaneously without any noticeable delay in response time.

Note: During deployment, due to using free tiers of AWS services, there are occasional delays in the application's response times, especially during video uploads.

Note: The `main` branch of this repository mainly contains the code for the deployed application which also corresponds to code for the linux os, also present in the `linux` branch. The `windows` branch contains the code for the windows os.

## Features

- **Video Upload**: Users can upload videos through the web interface.
- **Subtitle Extraction**: Extracts subtitles from uploaded videos using `ccextractor`.
- **Background Processing**: Uses Celery to handle video processing in the background.
- **AWS Integration**: Stores videos in AWS S3 and subtitles in AWS DynamoDB.
- **Video Streaming**: Provides pre-signed URLs for streaming videos from S3.
- **Web Interface**: Provides a user-friendly web interface for interacting with the application.
- **API Endpoints**: Provides API endpoints for interacting with the application programmatically.
- **Search Functionality**: Allows users to search for keywords in subtitles and videos.
- **Keyword Search**: Allows users to search for keywords in subtitles and retrieves the relevant time segments in the video.

## Requirements

- Python 3.9+
- Django
- AWS Account with S3 and DynamoDB setup
- `ccextractor` installed
- Redis (for Celery message broker)
- Celery

## Setup and Installation

### Clone the Repository

```sh
git clone https://github.com/lordgrim18/VideoSearch.git
cd videoprocessingapp
```

### Install Dependencies

Create a virtual environment and install the required dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set Environment Variables

Create a `.env` file in the project root directory and add the variables given in the sample `.env.sample` file.

###  AWS Configuration

- Create an AWS account and set up an S3 bucket and DynamoDB table. It is recommended to create a separate IAM user with limited permissions for this project. 
- Use the AWS CLI to configure your credentials:
- Install the AWS CLI:
follow the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- After installing the AWS CLI, run the following command to configure your credentials:

```sh
aws configure
```
Enter your AWS Access Key ID and Secret Access Key when prompted. Then set the default region to the region where you created your S3 bucket and DynamoDB table. You can find the region code in the AWS Management Console in the top left. Set the output format to `json`. 

#### S3 Bucket

- In the AWS Management Console, create an S3 bucket to store the videos.
- Keep in mind that the bucket must be in the same region as the one you configured in the AWS CLI.
- Set the bucket name in the `.env` file.

#### DynamoDB Table

- The DynamoDB table can be created by running the [`core/dynamo_migration.py`](https://github.com/lordgrim18/VideoSearch/blob/main/core/dynamo_migrator.py) script.
- Run the script with the following command:

```sh
python core/dynamo_migrator.py
```

- This will create two tables in DynamoDB: `Video` and `Subtitle`.
- The `Video` table stores information about the uploaded videos, while the `Subtitle` table stores the extracted subtitles.

### Start Redis (for Celery)

- Install Redis:

```sh
sudo apt update
sudo apt install redis-server
```

- Start the Redis server:

```sh
sudo service redis-server start
```

- Check the status of the Redis server:

```sh
sudo service redis-server status
```

- Verify that Redis is running:

```sh
redis-cli ping
```
The server should respond with `PONG`. 

If you are running Redis on a different host or port, you can specify the connection string in the `.env` file.

### Start Celery Worker

Start the Celery worker to handle background tasks:

```sh
celery -A VideoSearch worker -loglevel=info
```

### Run the Application

Start the Django development server:

```sh
python manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000/`.

## Usage

1. Upload a video through the web interface.
2. The video will be processed in the background to extract subtitles.
3. Once the subtitles are extracted, you can search for keywords in the subtitles.
4. The application will display the relevant time segments in the video where the keywords appear.

Users can also interact with the API endpoints directly:
They are located at `http://127.0.0.1:8000/api/v1/`.

## API Endpoints

The API endpoints allow users to interact with the application programmatically. The available endpoints are:

### Videos

- `GET /api/v1/videos/`: List all videos.
- `POST /api/v1/videos/create/`: Upload a video.
- `GET /api/v1/videos/<video_id>/`: Retrieve a specific video.
- `PATCH /api/v1/videos/update/<video_id>/`: Update a video.
- `DELETE /api/v1/videos/delete/<video_id>/`: Delete a video.
- `GET /api/v1/videos/search/`: Search for videos by keyword.

### Subtitles

- `GET /api/v1/subtitles/<video_id>`: Retrieve subtitles for a specific video.
- `GET /api/v1/subtitles/<video_id>/search/`: Search for keywords in the subtitles of a video.
- `GET /api/v1/subtitles/search/`: Search for keywords in all subtitles.

### Storage

- `GET /api/v1/storage/`: List all videos stored in S3.
- `GET /api/v1/storage/object_name/`: Retrieve a specific video stored in S3.
- `POST /api/v1/storage/url/`: Obtain a pre-signed URL from S3 for streaming the video.

### Search

- `GET /api/v1/search/`: Search for keywords in all subtitles and videos.

## Deployment

- The application has been deployed to AWS EC2 instance and can be accessed at [http://65.2.179.201/](http://65.2.179.201/).
- The deployment process involves setting up the EC2 instance, installing the necessary dependencies, configuring the environment variables, and running the application.
- The application is served using Gunicorn and Nginx.
- The Celery worker is also running on the EC2 instance to handle background tasks.
- The Celery worker was daemonized to run in the background.

Note: During deployment, due to using free tiers of AWS services, there are occasional delays in the application's response times, especially during video uploads.