from flask import Flask, jsonify
import time, random, json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

app = Flask(__name__)

producer = None

def get_kafka_producer():
    global producer
    if producer is None:
        while True:
            try:
                producer = KafkaProducer(
                    bootstrap_servers='kafka:9092',
                    value_serializer=lambda x: json.dumps(x).encode('utf-8')
                )
                break
            except NoBrokersAvailable:
                print("Kafka broker not available, retrying in 5 seconds...")
                time.sleep(5)
    return producer

endpoints = ["users", "products", "orders", "login", "logout", "health"]

@app.route("/<endpoint>")
def serve(endpoint):
    start_time = time.time()

    if endpoint not in endpoints:
        return jsonify({"error": "Not found"}), 404

    try:
        if random.random() < 0.2:
            raise Exception("Simulated error!")

        response_time = round((time.time() - start_time) * 1000, 2)

        log = {
            "timestamp": time.time(),
            "endpoint": f"/{endpoint}",
            "status_code": 200,
            "response_time_ms": response_time,
            "error": None
        }
        get_kafka_producer().send('api-logs', log)
        print("api-logs", log)
        return jsonify({"message": f"Success on /{endpoint}"}), 200

    except Exception as e:
        response_time = round((time.time() - start_time) * 1000, 2)
        log = {
            "timestamp": time.time(),
            "endpoint": f"/{endpoint}",
            "status_code": 500,
            "response_time_ms": response_time,
            "error": str(e)
        }
        get_kafka_producer().send('error-logs', log)
        print("error-logs", log)
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

