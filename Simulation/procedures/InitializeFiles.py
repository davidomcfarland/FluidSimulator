from ..libs import os

def InitializeFiles():
    try:
        for f in os.listdir("images"):
            os.remove(f"images/{f}")
    except FileNotFoundError:
        os.mkdir("images")
    
    try:
        os.remove("sim00.mp4")
    except FileNotFoundError:
        pass