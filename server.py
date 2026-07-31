import os
import sys
import json
import asyncio
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

BOT_TOKEN = "990446753:AAEGsqS0z4_rSZh3wkrVFHhaOMHz_IgcqWk"

def main():
    logging.info("Virtual Office Real Backend Server Starting...")
    logging.info(f"Telegram Bot @TheUKI_BOT Token Configured: {BOT_TOKEN[:10]}...")
    
    # Run simple HTTP server on port 8080
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logging.info("Virtual Office Web & API Server running on http://127.0.0.1:8080")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
