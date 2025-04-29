import socket
import time
import functools
import logging

def check_internet_connection(host="anthropic.com", port=443, timeout=3):
    """Check if there is an internet connection by trying to connect to Anthropic's servers."""
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False
    


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def timer(func):
    """
    A decorator that logs the execution time of the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
    
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        
        return result
    
    return wrapper