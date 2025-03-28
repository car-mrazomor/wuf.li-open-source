import requests
import json

import time

avoid_domains:list = ["wesellconsulting.ca", "automatedpartners.ai", "efukt.tv", "4fuck.org", "chudai.me", "buraqlab.com", "flatworm.lol", "terraconsults.com", "owo.farm",
                                "campornhot.com", "loly.tube", "pornblogr.com", "3porn.org", "horrorporn.tv", "ovo.hr"]
api_key:str = open("static/.secret_key", "r").read().split("\n")[0]

def func() -> any:
    headers:dict = { "Content-Type": "application/json",
        "X-API-Key": api_key }
    try:
        res = requests.get("https://mail.wuf.li/api/v1/get/domain/all", headers=headers)
        data:json = json.loads(res.text)
        with open("static/.domains", "w") as f:
            for _ in data:
                if _["domain_name"] in avoid_domains:
                    continue
                f.write(f"{_['domain_name']},{_['mboxes_in_domain']}\n")
    except Exception as e:
        print(e)
        pass

while True:
    try:
        func()
        time.sleep(60)
    except KeyboardInterrupt:
        exit(-1)