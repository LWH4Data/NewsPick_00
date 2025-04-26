from kafka import KafkaConsumer
import json
import time

consumer = KafkaConsumer(
    'article-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"메시지 수신: {message.value}")
    # 여기서 메시지를 처리하는 로직을 추가할 수 있습니다.
    time.sleep(1)  # 메시지 처리 후 잠시 대기
    
