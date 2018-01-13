import requests
from urllib import urlopen
import json
from local.config import api_key

words = json.loads(urlopen("http://mnemonic-si.appspot.com/api/words").read())["result"]

for word in words:
    name = word["name"]
    if not name:
        print requests.post(
            "http://mnemonic-si.appspot.com/api/import/Word/%s?api_key=%s&delete=1" % (name, api_key),
            data=json.dumps({})).text        
    
