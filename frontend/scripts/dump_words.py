import requests
import json
from collections import OrderedDict

target = "static/data/words_cached.json"
words_cached = json.loads(requests.get("http://mnemonic-si.appspot.com/api/words").text)
open(target, "w").write(json.dumps(words_cached, indent=4))
print("wrote to %s" % target)

words = OrderedDict({})
for word in words_cached["result"]:
    words[word["name"]] = word
target = "static/data/words.json"
open(target, "w").write(json.dumps(words, indent=4))
print("wrote to %s" % target)

binary_to_name = OrderedDict({})
for word in words_cached["result"]:
    binary_to_name[word["binary"]] = word["name"]
target = "static/data/binary_to_name.json"
open(target, "w").write(json.dumps(binary_to_name, indent=4))
print("wrote to %s" % target)

decimal_to_name = OrderedDict({})
for word in words_cached["result"]:
    decimal_to_name[word["decimal"]] = word["name"]
target = "static/data/decimal_to_name.json"
open(target, "w").write(json.dumps(decimal_to_name, indent=4))
print("wrote to %s" % target)

