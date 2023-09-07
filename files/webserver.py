from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

save_status = 0


# Load the settings from the JSON file
def load_settings():
    try:
        with open('settings.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        # Return default settings if the file doesn't exist
        return {
                "screen_number": 1,
                "refresh_interval": 5,
                "categories": "abstract",
                "orientation": 1,
                "content_filter": 1,
                "frame_number": 1,
                "api_key": "", 
                "api_limit": -1,
                "last_photo_time": "",
                "next_photo_time": ""

        }

# Save the settings to the JSON file
def save_settings(settings):
    with open('settings.json', 'w') as json_file:
        json.dump(settings, json_file, indent=4)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global save_status 
        
        if self.path == '/':
            # Serve the HTML form for the main page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('webserver/index.html', 'r') as html_file:
                html_content = html_file.read()

                # Load settings from the JSON file
                settings = load_settings()

                # Inject the settings values into the HTML form fields
                
                html_content = html_content.replace('{{api_limit}}',  str(settings['api_limit']))
                html_content = html_content.replace('{{last_photo_time}}',  str(settings['last_photo_time']))
                html_content = html_content.replace('{{next_photo_time}}',  str(settings['next_photo_time']))
                

            self.wfile.write(html_content.encode())

        elif self.path == '/settings':
            # Serve the HTML form for the main page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('webserver/settings.html', 'r') as html_file:
                html_content = html_file.read()

                # Load settings from the JSON file
                settings = load_settings()

                # Inject the settings values into the HTML form fields
                
                html_content = html_content.replace('{{categories}}',  str(settings['categories']))
                html_content = html_content.replace('{{refresh_interval}}',  str(settings['refresh_interval']))
                html_content = html_content.replace('{{orientation}}',  str(settings['orientation']))
                html_content = html_content.replace('{{content_filter}}', str(settings['content_filter']))
                html_content = html_content.replace('{{screen_number}}',  str(settings['screen_number']))
                html_content = html_content.replace('{{save_status}}',  str(save_status))
                
                

            self.wfile.write(html_content.encode())
            save_status = 0

        elif self.path == '/api':
            # Serve the HTML form for the main page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('webserver/api.html', 'r') as html_file:
                html_content = html_file.read()

                # Load settings from the JSON file
                settings = load_settings()

                # Inject the settings values into the HTML form fields
                
                html_content = html_content.replace('{{api_key}}', str(settings['api_key']))
                html_content = html_content.replace('{{save_status}}',  str(save_status))
                

            self.wfile.write(html_content.encode())
        
        elif self.path == '/style.css':
            # Serve the styles.css file from the "static" directory
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('webserver/style.css', 'rb') as file:
                self.wfile.write(file.read())
        
        elif self.path == '/image.jpg':
            # Serve the image file (image.jpg)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open('images/image.jpg', 'rb') as file:
                self.wfile.write(file.read())
            
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        global save_status

        if self.path == '/settings':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            post_vars = dict(x.split("=") for x in post_data.split("&"))

            # Load settings from the JSON file
            settings = load_settings()

            decoded_categories = urllib.parse.unquote(post_vars['categories'])
            decoded_categories = decoded_categories.replace('+', ' ')
           

            # Update the settings with the values from the POST request
            settings['categories'] = decoded_categories
            settings['refresh_interval'] = int(post_vars['refresh_interval'])
            settings['orientation'] = int(post_vars['orientation'])
            settings['content_filter'] = int(post_vars['content_filter'])
            settings['screen_number'] = int(post_vars['screen_number'])

            # Save the updated settings back to the JSON file
            save_settings(settings)
            save_status= 1

            open('reload_flag.txt', 'w').close()

            self.send_response(302)
            self.send_header('Location', '/settings')
            self.end_headers()

        elif self.path == '/api':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            post_vars = dict(x.split("=") for x in post_data.split("&"))

            # Load settings from the JSON file
            settings = load_settings()

            # Update the settings with the values from the POST request
            settings['api_key'] = post_vars['api_key']
            
            # Save the updated settings back to the JSON file
            save_settings(settings)
            save_status= 1
            
            open('reload_flag.txt', 'w').close()

            self.send_response(302)
            self.send_header('Location', '/api')
            self.end_headers()
        
        elif self.path == '/photo':
            
            open('reload_flag.txt', 'w').close()

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        
        elif self.path == '/reboot':
            # Respond to the shutdown request
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Execute the shutdown command (you may need to adjust the command)
            import subprocess
            subprocess.Popen(['sudo', 'reboot'])

            # Optionally, you can send a message back to the client
            self.wfile.write("rebooting...".encode())

        elif self.path == '/shutdown':
            # Respond to the shutdown request
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Execute the shutdown command (you may need to adjust the command)
            import subprocess
            subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])

            # Optionally, you can send a message back to the client
            self.wfile.write("Shutting down...".encode())

        else:
            self.send_error(404, "File not found")
    
def run_server():
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 80...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

