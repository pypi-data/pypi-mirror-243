import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from instagrapi import Client
#from aioinstagrapi import Client

creds = {
    "uuids": {
        "phone_id": "52d63238-9a28-4b3f-8c77-f3da7709fe9f",
        "uuid": "c0a6f2c4-391c-42a3-ac42-de01db58607a",
        "client_session_id": "006b09a4-b8c0-489b-b42e-1095df0b3ae7",
        "advertising_id": "29e39755-5bba-4583-bde4-ed2aa24ef8e8",
        "android_device_id": "android-849bd0bcdf56ab1f",
        "request_id": "64131060-2f21-4925-b032-90b16af02ee0",
        "tray_session_id": "821f6cd5-1175-4c7e-9c4a-9cdc8839afe7",
    },
    "mid": "ZVWGowABAAHaePKwtOaftvAR4V8T",
    "ig_u_rur": None,
    "ig_www_claim": None,
    "authorization_data": {
        "ds_user_id": "61136867925",
        "sessionid": "61136867925%3AaNaA56uNCexBbq%3A24%3AAYfvp7YFxDpIGuCXNkhylAH5UYiZMiJ1p0f2ffFQNQ",
    },
    "cookies": {},
    "last_login": 1700103853.690681,
    "device_settings": {
        "app_version": "269.0.0.18.75",
        "android_version": 26,
        "android_release": "8.0.0",
        "dpi": "480dpi",
        "resolution": "1080x1920",
        "manufacturer": "OnePlus",
        "device": "devitron",
        "model": "6T Dev",
        "cpu": "qcom",
        "version_code": "314665256",
    },
    "user_agent": "Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; 6T Dev; devitron; qcom; en_US; 314665256)",
    "country": "US",
    "country_code": 1,
    "locale": "en_US",
    "timezone_offset": -14400,
}





def compare_keys(x, creds):
    keys1 = list(x.keys())
    keys2 = list(creds.keys())
    for key in keys1:
        if key not in keys2:
            print(key)
            continue
        old_value = creds[key]
        new_value = x[key]
        if type(old_value) == dict:
            compare_keys(old_value, new_value)
        print(key)

