import subprocess
import time
import sys

# --- Configuration ---
# Your ngrok URL is needed by the assistant.py script. We will find it here.
ngrok_url = ""

# --- Step 1: Start the ngrok tunnel ---
print("Starting ngrok tunnel...")
ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5)  # Give ngrok a few seconds to start

# Find the ngrok public URL from its output
while True:
    line = ngrok_process.stdout.readline().decode('utf-8')
    if "https://" in line:
        ngrok_url = line.strip().split(" ")[-1]
        print(f"Ngrok URL found: {ngrok_url}")
        break

if not ngrok_url:
    print("Could not find ngrok URL. Exiting.")
    sys.exit()

# --- Step 2: Update the assistant.py file with the URL ---
print("Updating assistant.py with ngrok URL...")
with open("assistant.py", "r") as f:
    content = f.read()

# Replace the placeholder URL in your assistant.py file
new_content = content.replace('ngrok_url = ""', f'ngrok_url = "{ngrok_url}"')

with open("assistant.py", "w") as f:
    f.write(new_content)

# --- Step 3: Start the Flask server ---
print("Starting Flask server...")
flask_process = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5)  # Give Flask a few seconds to start

# --- Step 4: Run the assistant.py script ---
print("Starting the assistant...")
subprocess.run(['python', 'assistant.py'])

print("Project finished. Closing all processes.")

# --- Cleanup ---
ngrok_process.kill()
flask_process.kill()