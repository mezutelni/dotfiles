#!/usr/bin/env python3
import subprocess
import re

def get_audio_outputs_and_filters():
    # Run wpctl status command and capture output
    wpctl_output = subprocess.run("wpctl status", shell=True, capture_output=True, text=True).stdout
    
    # Initialize dictionaries to store sinks and filters
    audio_outputs = {}
    audio_filters = {}
    is_current = False

    # Flags to identify when within the Sinks or Filters sections
    in_sinks_section = False
    in_filters_section = False
    for line in wpctl_output.splitlines():
        # Check if we're entering the Sinks section
        if re.search(r"├─ Sinks:", line):
            in_sinks_section = True
            in_filters_section = False
            continue
        # Check if we're entering the Filters section
        elif re.search(r"├─ Filters:", line):
            in_filters_section = True
            in_sinks_section = False
            continue
        # Exit both sections when reaching Sources or Streams
        elif re.search(r"├─ Sources:|^ *└─ Streams:", line):
            in_sinks_section = False
            in_filters_section = False

        # Process lines within Sinks section
        if in_sinks_section:
            line = re.sub(r"\[vol: [^]]*\]", "", line).strip()  # Remove volume indicators and whitespace
            if line:
                # Mark default output
                if "*" in line:
                    is_current = True
                # Extract ID and name for Sinks
                match = re.search(r"(\d+)\.\s*(.+)", line)
                if match:
                    device_id = match.group(1).strip()
                    device_name = match.group(2).strip()
                    audio_outputs[device_id] = device_name
                    if is_current:
                        current = device_name
                        is_current = False

        # Process lines within Filters section
        if in_filters_section and "[Stream/Output/Audio]" not in line:
            line = re.sub(r"\[vol: [^]]*\]", "", line).strip()  # Remove volume indicators and whitespace
            if line:
                # Mark default output
                if "*" in line:
                    is_current = True
                # Extract ID and name for Filters
                match = re.search(r"(\d+)\.\s*(.+)", line)
                if match:
                    filter_id = match.group(1).strip()
                    filter_name = match.group(2).strip().split(" ",1)[0]
                    audio_filters[filter_id] = filter_name
                    if is_current:
                        current = filter_name
                        is_current = False
    outputs = audio_outputs.update(audio_filters)
    return audio_outputs, current

def prepare_string(outputs, current):
    # Prepare empty list
    tmp = []

    # Add bold style for default option
    tmp.append(f"<b>{current}</b>")
    
    # Add values of sinks and filters dict into tmp
    tmp = tmp + list(outputs.values())
    
    # Remove duplicate default option (one without <b> tag)
    if current in tmp: tmp.remove(current)
    
    # Save length of the list
    list_len = len(tmp)

    # Convert list of options into string
    tmp = "\n".join(tmp)

    return tmp, list_len


def display_rofi_menu(prepared_string, list_len):
    rofi_cmd = f"rofi -dmenu -markup-rows -theme \"tokyonight-audio-picker\" -theme-str 'window {{ location: '\"center\"'; }} listview {{ lines: {list_len}; }}'"

    rofi_output = subprocess.run(rofi_cmd, input=prepared_string, shell=True, capture_output=True, text=True).stdout

    return rofi_output

def set_new_output(new_output, outputs, current):
    new_output = new_output.replace("<b>","").replace("</b>","").strip()
    
    if new_output == current:
        return True
    
    for key, value in outputs.items():
        if value == new_output:
            id = key

    subprocess.run(f"wpctl set-default {id}", shell=True)
    

# Call function and print the output device and filter dictionaries
outputs, current = get_audio_outputs_and_filters()

# Create STDIN for rofi
prepared_string, list_len = prepare_string(outputs, current)

# Call rofi
new_output = display_rofi_menu(prepared_string, list_len)

# Set output
set_new_output(new_output, outputs, current)
