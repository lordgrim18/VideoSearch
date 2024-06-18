import time
import logging

# Set up logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LatencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        latency = end_time - start_time

        logger.info(f"Request to {request.path} took {latency:.4f} seconds")

        if latency > 1:
            response.content += b'\nWarning: Request latency exceeded 1 second!'
        response['X-Request-Latency'] = str(latency)

        return response
