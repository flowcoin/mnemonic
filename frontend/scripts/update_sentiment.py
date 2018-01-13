import requests
from urllib import urlopen
import json
from local.config import api_key, mashape_key

words = json.loads(urlopen("http://mnemonic-si.appspot.com/api/words").read())["result"]

for word in words:
    name = word["name"]
    if word["sentiment"] is not None:
        continue
            
    res = json.loads(requests.get("https://twinword-sentiment-analysis.p.mashape.com/analyze/?text=%s" % name,
      headers={"X-Mashape-Key": mashape_key}).text)
    print res
    sentiment = int(res["score"] * 100)
    
    print requests.post(
        "http://mnemonic-si.appspot.com/api/import/Word/%s?api_key=%s" % (name, api_key),
        data=json.dumps({"sentiment": sentiment, "seniment": None})).text
