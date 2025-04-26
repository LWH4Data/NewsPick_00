import os
import json
import psycopg2
from dotenv import load_dotenv
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import Configuration

load_dotenv()

# ✅ 텍스트 전처리
def preprocess_content(content):
    import tiktoken
    if not content:
        return ""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    return encoding.decode(tokens[:5000]) if len(tokens) > 5000 else content

# ✅ 키워드 추출
def extract_keywords(text):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"다음 뉴스에서 핵심 키워드 5개를 쉼표로 구분하여 출력해주세요.\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return [k.strip() for k in response.choices[0].message.content.split(",")]

# ✅ 임베딩 생성
def get_embedding(text):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# ✅ 카테고리 분류
def classify_category(text):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    categories = ["IT_과학", "건강", "경제", "교육", "국제", "라이프스타일", "문화", "사건사고", "사회일반",
                  "산업", "스포츠", "여성복지", "여행레저", "연예", "정치", "지역", "취미"]
    prompt = f"""다음 뉴스 내용을 가장 적절한 카테고리 하나로 분류해줘:
{', '.join(categories)}

뉴스 내용:
{text}

답변은 카테고리 이름만 출력해줘."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    output = response.choices[0].message.content.strip()
    return output if output in categories else "미분류"

# ✅ DB 저장
def save_to_postgres(url, keywords, embedding, category):
    conn = psycopg2.connect(
        dbname="news",
        user="postgres",
        password="ssafy",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO news_keyword (url, keyword) VALUES (%s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (url, json.dumps(keywords, ensure_ascii=False)))

        cur.execute("""
            INSERT INTO news_embedding (url, embedding) VALUES (%s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (url, embedding))

        cur.execute("""
            INSERT INTO news_category (url, category) VALUES (%s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (url, category))

        conn.commit()
        print(f"✅ 저장 완료: {url}")
    except Exception as e:
        print(f"❌ 저장 실패: {url} | {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# ✅ Kafka 메시지 처리 함수 (직렬화 안전)
def create_handler():
    def handle_message(msg):
        try:
            data = json.loads(msg)
            url = data["url"]
            text = preprocess_content(data["full_text"])
            keywords = extract_keywords(text)
            embedding = get_embedding(text)
            category = classify_category(text)
            save_to_postgres(url, keywords, embedding, category)
        except Exception as e:
            print(f"❌ 처리 실패: {e}")
    return handle_message

# ✅ Flink 파이프라인 실행
def main():
    config = Configuration()
    config.set_string(
        "pipeline.jars",
        "file:///home/ssafy/jars/flink-connector-kafka-1.17.0.jar;"
        "file:///home/ssafy/jars/kafka-clients-3.4.0.jar"
    )

    env = StreamExecutionEnvironment.get_execution_environment(configuration=config)
    env.set_parallelism(1)

    kafka_props = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'flink-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = FlinkKafkaConsumer(
        topics='fulltext-topic',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    stream = env.add_source(consumer)
    stream.map(create_handler())  # 직렬화-safe한 함수 사용

    env.execute("Flink OpenAI 뉴스 분석")

if __name__ == "__main__":
    main()
