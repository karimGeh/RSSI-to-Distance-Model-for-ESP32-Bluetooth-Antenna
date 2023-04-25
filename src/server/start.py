import os

ip_address = "192.168.2.100"

os.system(f"uvicorn main:app --host {ip_address} --reload")
