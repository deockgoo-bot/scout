# CLAUDE.md — DevBrief

> 1인 개발자를 위한 데일리 기술 브리핑 봇.
> 매일 아침 06:00(KST), 4개 소스에서 개발 소식 10개를 선별해 텔레그램으로 전송한다.

---

## 프로젝트 개요

- **프로젝트명**: DevBrief (서브 프로젝트)
- **목적**: 1인 개발자의 정보 격차 해소. 직접 돌아다니지 않아도 핵심 기술 소식이 매일 아침 도착.
- **사용자**: 개발자 본인 1명
- **개발 시간 제한**: 2시간 이내 MVP
- **실행 환경**: GitHub Actions (서버리스, 무료, 데스크탑 불필요)

---

## 핵심 동작

```
매일 06:00 KST (GitHub Actions cron)
  → 4개 소스 수집
  → 키워드 필터링
  → 점수 기반 상위 10개 선별
  → 텔레그램 봇으로 1개 메시지 전송
```

---

## 데이터 소스 (4개)

### 1. GitHub Trending
- URL: `https://github.com/trending?since=daily`
- 방법: HTML 파싱 (beautifulsoup4)
- 필드: repo명, 설명, star 총수, 오늘 증가분, 언어, URL
- 수집량: 상위 25개

### 2. Hacker News
- API: `https://hacker-news.firebaseio.com/v0/topstories.json` (공식, 무료, 키 불필요)
- 각 항목: `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- 필드: 제목, URL, 점수, 댓글수
- 수집량: Top 30

### 3. GeekNews
- RSS: `https://feeds.feedburner.com/geeknews-feed` (또는 `https://news.hada.io/rss/news`)
- 방법: feedparser
- 필드: 제목, URL, 게시일
- 수집량: 최근 24시간 전체

### 4. Reddit
- 라이브러리: praw (공식 API)
- 서브레딧: `LocalLLaMA`, `ClaudeAI`, `SaaS`
- 정렬: hot, 최근 24시간
- 필드: 제목, URL, 업보트, 서브레딧명
- 수집량: 서브레딧당 10개

---

## 필터 & 랭킹

### 키워드 필터 (제목+설명에 1개 이상 매칭, 대소문자 무시)

```python
KEYWORDS = [
    # AI/ML
    "llm", "rag", "fine-tuning", "agent", "agentic", "vision", "ocr",
    "transformer", "embedding", "gpt", "claude", "gemini", "llama",
    "openai", "anthropic", "mcp",
    # 개발
    "python", "typescript", "rust", "swift", "open source",
    "developer", "cli", "sdk", "api", "framework", "library",
    # 인프라
    "docker", "deploy", "serverless", "database", "postgresql", "vector",
    # 비즈니스
    "saas", "startup", "pricing", "seed", "solo founder", "indie",
    # 생산성
    "automation", "workflow", "editor", "document", "parsing",
]
```

- GeekNews는 한국어라 키워드 필터 **면제** (전부 후보로, 최신순)

### 점수 계산

```python
score = popularity * (1 + keyword_hits * 0.3)
# popularity: GitHub star증가분 / HN점수 / Reddit업보트
# GeekNews는 최신순 정렬 (점수 없음)
```

### 선별 규칙 (총 10개)

- GitHub 최소 3개
- HN 최소 2개
- GeekNews 최소 2개
- Reddit 최소 2개
- 나머지 1개는 전체 점수순

---

## 텔레그램 메시지 포맷

하나의 메시지로 전송 (10개 항목):

```
☀️ DevBrief (2026-06-11)

1. ⭐ [GitHub] unsloth/unsloth — 2x faster fine-tuning ★12.3k (+342)
   https://github.com/...

2. 🔶 [HN] Why RAG beats fine-tuning in prod (583pts)
   https://news.ycombinator.com/...

3. 🇰🇷 [GeekNews] Claude Code 사용 패턴 정리
   https://news.hada.io/...

4. 💬 [Reddit·LocalLLaMA] Llama 4 70B coding benchmark (↑2.1k)
   https://reddit.com/...

...

10. ...
```

- 제목은 80자에서 자르기
- HTML parse_mode 사용, 링크는 평문 URL
- 메시지가 4096자 초과 시 2개로 분할

---

## 파일 구조

```
devbrief/
├── main.py              # 수집→필터→선별→전송 (엔트리포인트)
├── collectors/
│   ├── __init__.py
│   ├── github.py
│   ├── hackernews.py
│   ├── geeknews.py
│   └── reddit.py
├── filter.py            # 키워드 필터 + 점수 + 선별
├── sender.py            # 텔레그램 전송 (requests로 직접 호출)
├── config.py            # 키워드, 선별 규칙, 상수
├── requirements.txt
├── .github/workflows/briefing.yml
└── README.md
```

---

## 환경 변수 (GitHub Secrets)

| 변수 | 설명 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | BotFather에서 발급 |
| `TELEGRAM_CHAT_ID` | getUpdates로 확인 |
| `REDDIT_CLIENT_ID` | reddit.com/prefs/apps |
| `REDDIT_CLIENT_SECRET` | 〃 |

코드에 키 하드코딩 금지. 전부 `os.environ`으로.

---

## GitHub Actions Workflow

```yaml
name: DevBrief Daily
on:
  schedule:
    - cron: '0 21 * * *'   # UTC 21:00 = KST 06:00
  workflow_dispatch:        # 수동 실행 버튼 (테스트용)

jobs:
  briefing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
```

---

## requirements.txt

```
requests
beautifulsoup4
feedparser
praw
```

---

## 개발 원칙 (Claude Code 지침)

1. **심플하게.** MVP다. 클래스 남발 금지, 함수형으로 짧게.
2. **에러는 소스 단위로 격리.** Reddit이 죽어도 나머지 3개는 전송돼야 한다. try/except로 각 collector 감싸고, 실패한 소스는 건너뛴다.
3. **외부 의존 최소화.** python-telegram-bot 안 쓰고 requests로 Bot API 직접 호출.
4. **테스트는 수동 실행으로.** workflow_dispatch로 즉시 실행해서 텔레그램 수신 확인하면 끝.
5. **로깅은 print로 충분.** Actions 로그에서 보면 된다.
6. **중복 제거는 v2.** 지금은 안 한다.

---

## 완료 기준 (Definition of Done)

- [ ] `workflow_dispatch` 수동 실행 시 텔레그램에 10개 항목 메시지 도착
- [ ] 4개 소스 모두 수집 확인 (로그에 소스별 수집 개수 출력)
- [ ] 1개 소스 강제 실패시켜도 나머지로 메시지 전송됨
- [ ] cron 등록 완료 (다음날 06:00 자동 수신 확인)

---

## v2 백로그 (지금 안 함)

- LLM 한줄 요약 추가
- 중복 제거 (전송 이력 저장)
- 텔레그램 명령어로 키워드 추가/삭제
- 주간 요약 리포트
- 클릭 기반 관심사 학습
