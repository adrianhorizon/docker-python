import os
import logging

import hug
from hug.middleware import LogMiddleware

from pythonjsonlogger import jsonlogger

from datetime import datetime

from Hitos.Hitos import Hitos

@hug.middleware_class()
class CustomLogger(LogMiddleware):
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        super().__init__(logger=logger)

    def _generate_combined_log(self, request, response):
        current_time = datetime.utcnow()
        return {'remote_addr':request.remote_addr,
                'time': current_time,
                'method': request.method,
                'uri': request.relative_uri,
                'status': response.status,
                'user-agent': request.user_agent }
    
estos_hitos = Hitos()

@hug.get('/')
def status():
    return { "status": "OK" }

@hug.get('/status')
def status():
    return { "status": "OK" }

@hug.get('/all')
def all():
    return { "hitos": estos_hitos.todos_hitos() }

@hug.get('/one/{id}')
def one( id: int ):
    return { "hito": estos_hitos.uno( id ) }

if 'PORT' in os.environ :
    port = int(os.environ['PORT'])
else:
    port = 8000

if __name__ == '__main__':
    hug.API(__name__).http.serve(port )
