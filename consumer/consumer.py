from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import mysql.connector
from mysql.connector import Error
import time

# Retry logic for Kafka connection
while True:
    try:
        consumer = KafkaConsumer(
            'api-logs', 'error-logs',
            bootstrap_servers='kafka:9092',
            #value_deserializer=lambda m: m.decode('utf-8'),
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='log-consumer-group'
        )
        break  # Connection successful
    except NoBrokersAvailable:
        print("Kafka broker not available, retrying in 5 seconds...")
        time.sleep(5)

# Retry logic for MySQL connection
while True:
    try:
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password="rootpass",
            database="logs"
        )
        if conn.is_connected():
            print("Connected to MySQL database.")
            break
    except Error as e:
        print("MySQL not available yet, retrying in 5 seconds...")
        time.sleep(5)

cursor = conn.cursor()

for message in consumer:
    log = message.value
    print("logs before db insert", log)
    cursor.execute("""
        INSERT INTO logs (timestamp, endpoint, response_time, status_code, error_message)
        VALUES (FROM_UNIXTIME(%s), %s, %s, %s, %s)
    """, (
        log['timestamp'],
        log['endpoint'],
        log['response_time_ms'],
        log['status_code'],
        log['error']
    ))
    conn.commit()
