import mimetypes
import pathlib
import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional, Type
from jinja2 import Environment, FileSystemLoader


HOST = "localhost"
PORT = 3000
DATA_FILE = os.path.join("storage", "data.json")


# Jinja2 environment
env = Environment(loader=FileSystemLoader(""))


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        pr_url = urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif self.path == "/read":
            self.send_read_page()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self) -> None:
        if self.path == "/message":
            content_length: int = int(self.headers["Content-Length"])
            body: str = self.rfile.read(content_length).decode("utf-8")
            data: Dict[str, list] = parse_qs(body)

            username: str = data.get("username", [""])[0]
            message: str = data.get("message", [""])[0]

            if username and message:
                self.save_message(username, message)
                self.redirect("/read")
            else:
                self.send_html_file("error.html", 404)
        else:
            self.send_html_file("error.html", 404)

    def send_html_file(self, filename: str, status: int = 200) -> None:
        try:
            self.send_response(status)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(filename, "rb") as fd:
                self.wfile.write(fd.read())
        except FileNotFoundError:
            self.send_html_file("error.html", 404)

    def send_static(self) -> None:
        self.send_response(200)
        mt: Optional[tuple] = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def send_read_page(self) -> None:
        try:
            with open(DATA_FILE, "r") as f:
                messages: Dict[str, Dict[str, str]] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = {}

        template = env.get_template("read.html")
        html: str = template.render(messages=messages)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    @staticmethod
    def save_message(username: str, message: str) -> None:
        timestamp: str = datetime.now().isoformat()
        with open(DATA_FILE, "r+") as f:
            try:
                data: Dict[str, Dict[str, str]] = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data[timestamp] = {"username": username, "message": message}
            f.seek(0)
            json.dump(data, f, indent=4)

    def redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()


def run(
    server_class: Type[HTTPServer] = HTTPServer,
    handler_class: Type[BaseHTTPRequestHandler] = HttpHandler,
) -> None:
    server_address = (HOST, PORT)
    http = server_class(server_address, handler_class)

    print(f"Server running at http://{HOST}:{PORT}")

    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()