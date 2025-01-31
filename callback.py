from flask import Flask, request, send_from_directory, abort
import base64
import logging
import sys
import argparse
import time
import threading
import os
from werkzeug.serving import make_server

# Suppress Werkzeug logs
import click
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass
def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass
click.echo = echo
click.secho = secho

# Configure custom logging
def configure_logging(level="INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        stream=sys.stdout
    )

def success(text):
    logging.info("[\033[32;1m+\033[0m] " + text)

def failure(text):
    logging.critical("[\033[31;1m✘\033[0m] \033[31;1m" + text + "\033[0m")

def debug(text):
    logging.debug("[\033[90m#\033[0m] " + text)

def info(text):
    logging.info("[\033[34;1m*\033[0m] " + text)

def warning(text):
    logging.warning("[\033[33;1m!\033[0m] \033[93m" + text + "\033[0m")

class Callback:
    def __init__(self, host="0.0.0.0", port=8000, headers=False, b64=False, serve=False):
        configure_logging()
        self.host = host
        self.port = port
        self.headers = headers
        self.b64 = b64
        self.serve = serve
        self.messages = [] 
        self.app = Flask(__name__)
        self.server = make_server(self.host, self.port, self.app)
        self.start()

        @self.app.route('/', methods=['GET', 'POST'])
        def handle_request():
            # Default callback handling
            query_params = request.args if request.method == 'GET' else request.form

            if self.headers:
                for header in request.headers:
                    print(': '.join(str(i) for i in header))
                print()

            if 'msg' in query_params:
                msg = query_params.get('msg')
                try:
                    decoded_msg = base64.b64decode(msg).decode('utf-8')
                    success(msg)
                    if self.b64:
                        info(f'b64_decoded: {decoded_msg}')
                        self.messages.append(decoded_msg) 
                    else:
                        self.messages.append(msg)
                except (base64.binascii.Error, UnicodeDecodeError):
                    info(msg)
                    self.messages.append(msg)

            if 'error' in query_params:
                error = query_params.get('error')
                failure(error)
                return "ERROR"
            return "Callback received"

        @self.app.route('/<path:filename>', methods=['GET'])
        def serve_file(filename):
            # Check if the file exists
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, filename)
            if os.path.isfile(file_path):
                # If serve is disabled, return 403 Forbidden
                if not self.serve:
                    return "Access forbidden, maybe run with --serve?", 403
                # If serve is enabled, serve the file
                return send_from_directory(current_directory, filename)
            # If the file does not exist, return 404 Not Found
            return "File not found", 404

    def start(self):
        def run():
            self.serve_forever()

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        time.sleep(1)  # Allow the server time to start
        return thread
    
    def serve_forever(self):
        info(f"XSS Server started on {self.host}:{self.port}")
        self.server.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()
            info("XSS Server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Callback Server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to.")
    parser.add_argument("--headers", action="store_true", help="Display HTTP headers for each request.")
    parser.add_argument("--b64", action="store_true", help="Automatically decode base64'd strings received on the server")
    parser.add_argument("--serve", action="store_true", help="Enable serving files from the current directory.")

    args = parser.parse_args()
    
    server = Callback(host=args.host, port=args.port, headers=args.headers, b64=args.b64, serve=args.serve)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
