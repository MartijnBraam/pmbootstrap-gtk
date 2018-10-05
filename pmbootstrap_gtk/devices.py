from pmb.flasher.frontend import list_devices
import subprocess
import json


def get_devices():
    result = []

    # Get adb/heimdall devices from the pmbootstrap flasher
    # devices = list_devices() //TODO: refactor this in pmbootstrap

    # Get possible block devices
    raw = subprocess.check_output(['lsblk', '-J'], universal_newlines=True)
    decoded = json.loads(raw)
    for device in decoded["blockdevices"]:
        # Only list removable devices
        if device["rm"] == "0":
            continue
        result.append({
            "type": "sdcard",
            "size": device["size"],
            "name": "/dev/{}".format(device["name"])
        })

    return result
