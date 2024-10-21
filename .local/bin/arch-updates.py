#!/usr/bin/env python3
import subprocess
import json

def get_updates():
    try:
        # Check if 'checkupdates' command is available
        subprocess.run(["which", "checkupdates"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get available updates
        result = subprocess.run(["checkupdates"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        updates = result.stdout.strip()
        updates_count = len(updates.splitlines())

        if updates_count == 0:
            tooltip = "No updates available"
        else:
            tooltip = updates

    except subprocess.CalledProcessError:
        # If 'checkupdates' command is not found or fails
        updates_count = "NaN"
        tooltip = 'Make sure "checkupdates" is installed and working properly'

    # Format output as JSON
    output = {"text": str(updates_count), "tooltip": tooltip}
    print(json.dumps(output))

if __name__ == "__main__":
    get_updates()

