import json

def get_uis():
    return [
        {
            "id": "none",
            "name": "None",
            "description": "No graphical environment",
            "type": "-"
        },
        {
            "id": "plasma-mobile",
            "name": "Plasma Mobile",
            "description": "Mobile variant of KDE Plasma (slow without hardware acceleration, allows only numeric passwords!)",
            "type": "wayland"
        },
    ]
