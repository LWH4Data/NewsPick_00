# 📰 NewsPick

**NewsPick**은 사용자의 관심사 기반으로 뉴스를 큐레이션하고,  
스크랩 · 분석 · 요약까지 가능한 **AI 기반 뉴스 추천 플랫폼**입니다.
---
## 사용법
1. infra를 실행 (airflow, kafka, redis, postgresql, spark)
```bash
cd 01_infra
docker compose up -d
```
2. django 실행을 통해 db 생성
```bash
cd ../02_web/backend
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
3. rss, kafka, openai 실행
```bash
cd ../03_data
python producer/producer.py
python consumer/consumer.py
```

---

## 🚀 기술 스택

### 🔧 Frontend

- Vue 3 + Vite
- Vuetify 3 (UI 프레임워크)
- Pinia (상태 관리)
- Vue Router (라우팅)

### 🔧 Backend

- Django + Django REST Framework
- SQLite (개발용 DB)
- AI 요약 기능: Gemma3 (로컬) / GPT-4 API (유료 사용자)
- Kafka, Airflow, Spark 기반 뉴스 데이터 수집 및 처리 (예정)

---

## 🎯 주요 기능

### 🏠 메인 페이지

- **비회원**
  - 오늘의 기사
  - 최근 인기 뉴스 목록 (무한 스크롤)

- **로그인 사용자**
  - 개인 맞춤 인기 뉴스 목록 (무한 스크롤)
  - 관심 키워드 기반 추천

---

### 🔍 탐색 및 필터링

- **검색 기능**: 제목 및 본문 키워드 기반 뉴스 탐색
- **태그 필터링**: 정치, 경제, 사회 등 카테고리 기반 뉴스 필터링

---

### 📌 관심 뉴스 기능

- **스크랩**: 관심 뉴스 저장
- **대시보드**:
  - 스크랩된 뉴스 목록 열람
  - 카테고리별 스크랩 분석
  - 주요 키워드 시각화 (도넛 그래프)

---

### 👍 상호작용 기능

- 뉴스 좋아요 기능
- 댓글 기능 (좋아요 및 대댓글 지원)

---

### 📄 상세 페이지

- AI 뉴스 요약 (Gemma3 or GPT-4 API)
- 관련 기사 추천 목록

---

## 📁 프로젝트 구조

```bash
NewsPick/
├── backend/               # Django 백엔드
│   ├── accounts/          # 사용자 인증 앱
│   ├── config/            # 설정 모듈
│   ├── news_api/          # 뉴스 관련 API
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   └── README.md
├── frontend/              # Vue 프론트엔드
│   ├── public/
│   ├── src/
│   ├── .vscode/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── venv/                  # Python 가상환경
└── .gitignore
```

---

## 🛠️ 설치 및 실행

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

### 백엔드 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

---

## 🗺️ 향후 계획

- 뉴스 크롤링 자동화 (Airflow + Kafka + Spark)
- 사용자 행동 기반 추천 시스템 고도화
- 반응형 레이아웃 및 다크모드 지원