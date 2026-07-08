# ShiftLens BE

교대조 인수인계 카드, 설비 알림 수집, audit trail을 제공하는 Flask REST API입니다.

## 주요 기능

- 로그인/refresh/logout
- 현재 교대조 조회
- handoff card 목록/상세/수정
- handoff action 기록
- alert ingest
- audit trail 기록

## 기술 스택

- Flask
- Tortoise ORM 모델 구조
- 모듈 기반 라우팅
- seeded in-memory repository for local demo

## 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.main run --port 5001
```

## 검증

```bash
python -m compileall app tests
pytest
```

## API

- `POST /api/v1/auth/signin`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/shifts/current`
- `GET /api/v1/handoff-cards`
- `GET /api/v1/handoff-cards/<id>`
- `PATCH /api/v1/handoff-cards/<id>`
- `POST /api/v1/handoff-cards/<id>/actions`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/ingest`

## 프로젝트 포인트

Flask 모듈 구조로 auth, alerts, handoff, shifts, audit를 분리했습니다. DB 모델은 PostgreSQL/TimescaleDB 확장을 고려한 Tortoise ORM 형태로 남겼습니다.
