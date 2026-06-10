# 데일리 브리핑

매일 아침 06:00(KST), GitHub·HN·GeekNews·Reddit에서 개발 소식 10개를 선별해 텔레그램으로 전송하는 봇.

## 데이터 소스

| 소스 | 방법 | 수집량 |
|------|------|--------|
| GitHub Trending | HTML 파싱 | 상위 25개 |
| Hacker News | 공식 API | Top 30 |
| GeekNews | RSS | 최근 24시간 |
| Reddit | praw (공식 API) | 서브레딧당 10개 |

Reddit 서브레딧: `LocalLLaMA`, `ClaudeAI`, `SaaS`

## 실행 환경

GitHub Actions (서버리스, 무료)

## 설치 및 실행

```bash
pip install -r requirements.txt
python main.py
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | BotFather에서 발급 |
| `TELEGRAM_CHAT_ID` | 텔레그램 채팅방 ID |
| `REDDIT_CLIENT_ID` | reddit.com/prefs/apps |
| `REDDIT_CLIENT_SECRET` | 〃 |

## 메시지 예시

```
좋은 아침이에요! 오늘도 좋은 하루 되세요 ☀️

📰 데일리 브리핑 (2026-06-10 06:00)

1. ⭐ [GitHub] unsloth/unsloth — 2x faster fine-tuning
   https://github.com/...

2. 🔶 [HN] Why RAG beats fine-tuning in prod
   https://...

3. 🇰🇷 [GeekNews] Claude Code 사용 패턴 정리
   https://...

4. 💬 [Reddit·LocalLLaMA] Llama 4 benchmark
   https://...
```
