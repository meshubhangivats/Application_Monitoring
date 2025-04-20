import requests
import random
import time

endpoints = ["users", "products", "orders", "login", "logout", "health"]

while True:
    endpoint = random.choice(endpoints)
    try:
        requests.get(f"http://localhost:5000/{endpoint}")
    except:
        pass
    time.sleep(random.uniform(0.3, 1.2))
