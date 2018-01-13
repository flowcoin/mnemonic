import requests
import json
from local.config import api_key

words = json.loads(open("codemojo/english.json").read())


for word, binary in words.items():
    print requests.post("http://mnemonic-si.appspot.com/api/import/Word/%s?api_key=%s" % (word, api_key), data=json.dumps({"name": word, "binary": binary, "decimal": int(binary, 2), "length": len(word)})).text
