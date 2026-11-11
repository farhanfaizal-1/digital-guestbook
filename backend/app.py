
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# Lokasi penyimpanan data pengunjung
DATA_FILE = os.environ.get(
    "DATA_FILE",
    "./guestbook.json"
)

# Membuat folder penyimpanan jika belum tersedia
os.makedirs(os.path.dirname(os.path.abspath(DATA_FILE)), exist_ok=True)


def load_messages():
    """Membaca data pengunjung dari file JSON."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_messages(messages):
    """Menyimpan data pengunjung ke file JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


class GuestbookHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        """Mengirim respons dalam format JSON."""
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path.split("?")[0] == "/messages":
            messages = load_messages()
            self.send_json(200, {"messages": messages})
        else:
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})

    def do_POST(self):
        if self.path != "/messages":
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(content_length))

            name = data.get("name", "").strip()
            institution = data.get("institution", "").strip()
            purpose = data.get("purpose", "").strip()

            if not name or not institution or not purpose:
                self.send_json(400, {
                    "error": "Nama, instansi, dan keperluan wajib diisi"
                })
                return

            messages = load_messages()

            new_message = {
                "name": name,
                "institution": institution,
                "purpose": purpose
            }

            messages.append(new_message)
            save_messages(messages)

            self.send_json(201, {
                "message": "Data pengunjung berhasil ditambahkan",
                "data": new_message
            })

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Format JSON tidak valid"})

    def do_DELETE(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path != "/messages":
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})
            return

        params = parse_qs(parsed_url.query)

        if "index" not in params:
            self.send_json(400, {"error": "Parameter index wajib diisi"})
            return

        try:
            index = int(params["index"][0])
            messages = load_messages()

            if index < 0 or index >= len(messages):
                self.send_json(404, {"error": "Data pengunjung tidak ditemukan"})
                return

            deleted = messages.pop(index)
            save_messages(messages)

            self.send_json(200, {
                "message": "Data berhasil dihapus",
                "data": deleted
            })

        except ValueError:
            self.send_json(400, {"error": "Index harus berupa angka"})


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 5000), GuestbookHandler)

    print("Digital Guestbook Backend berjalan di port 5000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan")
        server.server_close()
