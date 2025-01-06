from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
import os


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(f"get: {self.path}")
            filename = self.path[1:]

            # Get file size for Content-Length header
            file_size = os.path.getsize(filename)

            # Send headers
            self.send_response(200)
            if filename.endswith(".mp3"):
                self.send_header("Content-Type", "audio/mpeg")
            elif filename.endswith(".wav"):
                self.send_header("Content-Type", "audio/wav")
            self.send_header("Content-Length", file_size)
            self.end_headers()

            # Stream file in chunks
            CHUNK_SIZE = 8192  # 8KB chunks
            with open(filename, "rb") as file:
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        print("Client disconnected")
                        return

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


# Start server

# Start server - just change this part
server = ThreadingHTTPServer(("0.0.0.0", 3333), RequestHandler)
print("Threaded server running at http://0.0.0.0:3333")
print("Put your audio file in the same directory as this script")
print("Access it at http://0.0.0.0:3333/sample.mp3")


try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down...")
    server.server_close()
