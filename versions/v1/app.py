from flask import Flask, render_template, send_from_directory
import csv
import os
import socket
from datetime import datetime
import subprocess
import socket

app = Flask(__name__)

def check_server_status(hostname):
    """Check if the server is online by pinging its hostname."""
    try:
        ip_address = socket.gethostbyname(hostname)  # Get IP from hostname
        output = subprocess.run(
            ["ping", "-c", "1", hostname],  # For Linux/Mac
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if output.returncode == 0:
            return ip_address, "online"
        else:
            return None, "offline"
    except socket.gaierror as e:
        print(f"Error resolving hostname {hostname}: {e}")
        return None, "offline"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, "offline"

def load_servers():
    """Load servers from the CSV file."""
    servers = []
    try:
        with open('servers.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ip_address, status = check_server_status(row['hostname'])  # Check status by hostname
                servers.append({
                    'hostname': row['hostname'],
                    'ip_address': ip_address if ip_address else "N/A",  # Display IP or N/A
                    'status': status,
                    'last_refreshed': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    except FileNotFoundError:
        print("Error: 'servers.csv' file not found.")
    except Exception as e:
        print(f"An error occurred while loading servers: {e}")
    return servers

@app.route('/')
def index():
    """Render the server status page."""
    servers = load_servers()
    return render_template('index.html', servers=servers)

@app.route('/styles.css')
def send_css():
    return send_from_directory('templates', 'styles.css')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
