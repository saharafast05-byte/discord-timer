import discord
from discord.ext import tasks
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Paste your real credentials here
BOT_TOKEN = "PASTE_YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = 123456789012345678  # Paste your Channel ID (no quotes)

# --- WEB SERVER INTERFACE FOR RENDER ---
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    server = HTTPServer(("0.0.0.0", 10000), HealthCheckServer)
    server.serve_forever()
# ----------------------------------------

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        if not self.message_loop.is_running():
            self.message_loop.start()

    @tasks.loop(minutes=1.0)
    async def message_loop(self):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("!work") 
            print("Command sent from the cloud!")

# Start the web server in a separate background thread
threading.Thread(target=run_web_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
