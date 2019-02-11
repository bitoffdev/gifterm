import argparse
import logging
from . import server

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Run the GifTerm server',
                                 prog='python3 -m gifterm')
parser.add_argument('--port', type=int, default=5000, help='server port')
parser.add_argument('--host', default='127.0.0.1', help='host interface')
args = parser.parse_args()

server.app.run(host=args.host, port=args.port)
