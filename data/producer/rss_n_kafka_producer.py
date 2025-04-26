import requests
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time
from kafka import KafkaProducer
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select
import json

# ✅ DB 연결 및 테이블 준비
engine = create_engine("postgresql+psycopg2://postgres:ssafy@localhost:5432/news")
metadata = MetaData()
metadata.reflect(bind=engine)
news_article = metadata.tables['news_article']

# ✅ 헤더 (403 우회)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36"
}

# ✅ 본문 크롤링 함수
def get_korean_text_from_url(url):
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ 본문 요청 실패: {url} | {e}")
        return ""

    soup = BeautifulSoup(res.text, "html.parser")
    text_list = []

    for string in soup.stripped_strings:
        if re.search(r"[가-힣]{2,}", string) and len(string.strip()) >= 20:
            text_list.append(string.strip())

    return " ".join(text_list)

# ✅ 삽입 함수
def insert_article(title, url, writer, summary, write_date, full_text):
    with engine.begin() as conn:
        stmt = pg_insert(news_article).values(
            url=url,
            title=title,
            writer=writer,
            summary=summary,
            write_date=write_date.date() if isinstance(write_date, datetime) else write_date,
            full_text=full_text
        ).on_conflict_do_nothing(index_elements=['url'])

        conn.execute(stmt)
        print(f"✅ 삽입 완료: {title}")

# ✅ 중복 여부 검사 함수
def article_exists(conn, url):
    query = news_article.select().where(news_article.c.url == url)
    return conn.execute(query).fetchone() is not None

# ✅ RSS 피드 URL (Khan 뉴스 RSS 예시)
RSS_FEED_URL_LIST = ["https://www.khan.co.kr/rss/rssdata/total_news.xml",       # 경향신문 / 전체 뉴스
                    "https://www.khan.co.kr/rss/rssdata/cartoon_news.xml",      # 경향신문 / 만평
                    "https://www.khan.co.kr/rss/rssdata/opinion_news.xml",      # 경향신문 / 오피니언
                    "https://www.khan.co.kr/rss/rssdata/politic_news.xml",      # 경향신문 / 정치
                    "https://www.khan.co.kr/rss/rssdata/economy_news.xml",      # 경향신문 / 경제
                    "https://www.khan.co.kr/rss/rssdata/society_news.xml",      # 경향신문 / 사회
                    "https://www.khan.co.kr/rss/rssdata/local_news.xml",        # 경향신문 / 지역
                    "https://www.khan.co.kr/rss/rssdata/kh_world.xml",          # 경향신문 / 국제
                    "https://www.khan.co.kr/rss/rssdata/culture_news.xml",      # 경향신문 / 문화
                    "https://www.khan.co.kr/rss/rssdata/kh_sports.xml",         # 경향신문 / 스포츠
                    "https://www.khan.co.kr/rss/rssdata/science_news.xml",      # 경향신문 / 과학&환경
                    "https://www.khan.co.kr/rss/rssdata/life_news.xml",         # 경향신문 / 라이프
                    "https://www.khan.co.kr/rss/rssdata/people_news.xml",       # 경향신문 / 사람
                    "https://www.khan.co.kr/rss/rssdata/english_news.xml",      # 경향신문 / 영문
                    "https://www.khan.co.kr/rss/rssdata/newsletter_news.xml",   # 경향신문 / 뉴스레터
                    "https://www.khan.co.kr/rss/rssdata/interactive_news.xml",  # 경향신문 / 인터랙티브
                    "https://www.kmib.co.kr/rss/data/kmibRssAll.xml",           # 국민일보 / 전체기사
                    "https://www.kmib.co.kr/rss/data/kmibPolRss.xml",           # 국민일보 / 정치
                    "https://www.kmib.co.kr/rss/data/kmibEcoRss.xml",           # 국민일보 / 경제
                    "https://www.kmib.co.kr/rss/data/kmibSocRss.xml",           # 국민일보 / 사회
                    "https://www.kmib.co.kr/rss/data/kmibIntRss.xml",           # 국민일보 / 국제
                    "https://www.kmib.co.kr/rss/data/kmibEntRss.xml",           # 국민일보 / 연예
                    "https://www.kmib.co.kr/rss/data/kmibSpoRss.xml",           # 국민일보 / 스포츠
                    "https://www.kmib.co.kr/rss/data/kmibGolfRss.xml",          # 국민일보 / 골프
                    "https://www.kmib.co.kr/rss/data/kmibLifeRss.xml",          # 국민일보 / 라이프
                    "https://www.kmib.co.kr/rss/data/kmibTraRss.xml",           # 국민일보 / 여행
                    "https://www.kmib.co.kr/rss/data/kmibEsportsRss.xml",       # 국민일보 / e스포츠
                    "https://www.kmib.co.kr/rss/data/kmibColRss.xml",           # 국민일보 / 사설/칼럼
                    "https://www.kmib.co.kr/rss/data/kmibChrRss.xml",           # 국민일보 / 더미션
                    ]

# ✅ Kafka 프로듀서 전역 설정 (JSON 직렬화)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
)

def kafka_producer(url, full_text):
    try:
        # Kafka로 보낼 메시지 구성
        message = {
            "url": url,
            "full_text": full_text
        }

        # fulltext 토픽으로 전송
        producer.send("fulltext-topic", value=message)
        print(f"📤 Kafka 전송 완료: {url}")
    except Exception as e:
        print(f"❌ Kafka 전송 실패: {e}")

# ✅ 메인 루프
def main_loop(interval=300):
    print(f"🔁 [5분 간격] RSS 감시 시작...")

    while True:
        try:
            with engine.begin() as conn:
                for feed_url in RSS_FEED_URL_LIST:
                    print(f"\n📡 피드 체크: {feed_url}")
                    response = requests.get(feed_url, headers=headers)
                    feed = feedparser.parse(response.content)

                    duplicate_count = 0  # 연속 중복 수
                    for entry in feed.entries:
                        url = entry.link

                        if article_exists(conn, url):
                            duplicate_count += 1
                            print(f"⚠️ 중복({duplicate_count}): {url}")
                            if duplicate_count >= 3:
                                print("🚫 연속 3회 중복 → 피드 스킵")
                                break
                            continue
                        else:
                            duplicate_count = 0

                        title = entry.title
                        summary = entry.summary
                        write_date = entry.updated_parsed or datetime.now()
                        write_date = datetime(*write_date[:6])
                        writer = entry.author if hasattr(entry, 'author') else "Unknown"

                        full_text = get_korean_text_from_url(url)

                        if len(full_text.strip()) >= 100:
                            if writer.strip() and summary.strip():
                                insert_article(title, url, writer, summary, write_date, full_text)
                                kafka_producer(url, full_text)
                            else:
                                print(f"⚠️ 필수 정보 누락으로 스킵: {title}")
                                print(f"    ⛔ writer: {repr(writer)}, summary 길이: {len(summary.strip())}")
                        else:
                            print(f"⚠️ 본문이 너무 짧아 스킵: {title}")
                            print(full_text)


            print(f"\n⏱ {interval}초 대기 후 재시작...")
            time.sleep(interval)        

        except KeyboardInterrupt:
            print("\n🛑 수집 중단됨.")
            break
        except Exception as e:
            print(f"❌ 예외 발생: {e}")
            time.sleep(interval)

# ✅ 실행 진입점
if __name__ == "__main__":
    main_loop(interval=300)