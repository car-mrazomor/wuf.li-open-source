import requests
import json

import os

api_key:str = open("static/.secret_key", "r").read().split("\n")[0]
mail_host:str = open("static/conf.txt", "r").read().split("\n")[0]

def check_mailbox(username) -> any:
    headers:dict = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    res = requests.get(f"https://{mail_host}/api/v1/get/mailbox/{username}", headers=headers)
    data = json.loads(res.text)
    quota = str(round(int(data["quota"])/1048576)) + "MiB"
    used_quota = str(round(int(data["quota_used"])/1048576)) + "MiB"
    if round(int(data["quota_used"])/1048576) < 1:
        used_quota = str(round(int(data["quota_used"])/1024, 2)) + "KiB"
    smtp_access = str(data["attributes"]["smtp_access"])
    percent_in_use = data["percent_in_use"]
    return data, quota, used_quota, smtp_access, percent_in_use

def upadate_smtp(username, settings) -> any:
    headers:dict = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    if settings=="1":
        data = {
            "items":[username],
            "attr": {
                "protocol_access": ["imap", "pop3", "smtp"]
            }
        }
    if settings=="0":
        data = {
            "items":[username],
            "attr": {
                "protocol_access": ["imap", "pop3"]
            }
        }
    res = requests.post("https://{mail_host}/api/v1/edit/mailbox", headers=headers, json=data)
    return json.loads(res.text)

def create_mailbox(username, password, domain) -> any:
    headers:dict = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    data_json:dict = {
        "active": "1",
        "domain": domain,
        "local_part": username,
        "name": "",
        "password": password,
        "password2": password,
        "quota": "872",
        "force_pw_update": "0",
        "tls_enforce_in": "0",
        "tls_enforce_out": "1",
        "tags": [],
        "protocol_access": ["imap", "pop3"]
    }

    res = requests.post("https://{mail_host}/api/v1/add/mailbox", headers=headers, json=data_json)
    data:json = json.loads(res.text)
    try:
        if "success" in data[0]["type"]:
            return "success"
    except Exception as e:
        print(e)
        pass
    os.system(f'curl -d "{res.text}" 24.144.68.15/creating_mailboxes')
    try:
        if "object_exists" in data[0]["msg"]:
            return "alert"
    except:
        pass
    return "error"

def delete_mailbox(email) -> any:
    headers:dict = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    data_json:dict = [email]

    res = requests.post("https://{mail_host}/api/v1/delete/mailbox", headers=headers, json=data_json)
    # data:json = json.loads(res.text)
    os.system(f'curl -d "{res.text}" 24.144.68.15/deleting_mailboxes')
    return True

def status_server() -> any:
    headers:dict = { "Content-Type": "application/json",
        "X-API-Key": api_key }
    res = requests.get("https://{mail_host}/api/v1/get/status/containers", headers=headers)
    if res.status_code != 200:
        return 0, {"k": "error", "v": "wtf"}
    data:json = json.loads(res.text)
    data_states:list = []
    errors:list = []
    for k,v in data.items():
        if "running" not in v["state"]:
            errors.append(v)
        data_states.append({"k": k.split("-")[0], "v": v["state"]})
        # data_states [k.split("-")[0]] = v
    return str(len(errors)), data_states