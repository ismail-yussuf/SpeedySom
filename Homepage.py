import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


PORT = 8000
DEFAULT_FILE = "Index.html"  # Specify your default HTML file

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Set the default file to load if the URL points to a directory
        path = super().translate_path(path)
        if path.endswith("/"):
            path += DEFAULT_FILE
        return path

    def do_POST(self):
        if self.path == "/process":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)
            user_input = params.get("userInput", [""])[0]
            # Make an OpenAI API request here and return the response
            generated_text = self.generate_openai_text(user_input)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(generated_text.encode("utf-8"))
        elif self.path == "/verify":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            
            # Perform verification here
            if self.verify_credentials(username, password):
                self.send_response(302)
                self.send_header("Location", "/Homepage.html")
                self.end_headers()
            else:
                self.send_response(403)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Login failed. Please try again.".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def verify_credentials(self, username, password):
        # Replace this with your actual credential verification logic
        # Return True if valid, False otherwise
        try:
            password = password + '\n'
            with open('Data.txt', "r") as file:
                lines = file.readlines()
                for line in lines:
                    fields = line.split(',')
                    if (fields[0] == username and fields[1] == password):
                        return True
        except Exception:
            print(Exception)
        return False

    def generate_openai_text(self, user_input):
        # Define the endpoint URL for chat-based completions
        endpoint = 'https://api.openai.com/v1/chat/completions'

        # Define the parameters for the API request
        params = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7,
        }

        # Make the API request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, json=params)

        # Check the response and return the generated message
        if response.status_code == 200:
            result = response.json()
            generated_message = result['choices'][0]['message']['content']
            return generated_message
        else:
            return f"OpenAI API Error: {response.status_code}"

Handler = CustomHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at localhost:{0}".format(PORT))
    webbrowser.open(f"http://localhost:{PORT}")
    httpd.serve_forever()
