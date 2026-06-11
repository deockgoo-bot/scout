# 강한 신호: 1개만 매칭돼도 통과. 주제 자체가 관심사인 키워드.
KEYWORDS_STRONG = [
    # AI/ML
    "llm", "rag", "fine-tuning", "fine tuning", "agent", "agentic", "ocr",
    "transformer", "embedding", "gpt", "claude", "gemini", "llama",
    "openai", "anthropic", "mcp", "vector",
    # 비즈니스
    "saas", "indie", "solo founder", "micro-saas",
]

# 약한 신호: 단독으로는 너무 흔해서 2개 이상 매칭돼야 통과.
KEYWORDS_WEAK = [
    # 개발
    "python", "typescript", "rust", "swift", "open source", "open-source",
    "developer", "cli", "sdk", "api", "framework", "library",
    # 인프라
    "docker", "deploy", "serverless", "database", "postgresql",
    # 비즈니스
    "startup", "pricing", "seed",
    # 생산성
    "automation", "workflow", "editor", "document", "parsing", "vision",
]

STRONG_BONUS = 0.4
WEAK_BONUS = 0.1

GITHUB_MIN = 2
REDDIT_MIN = 2
HN_MIN = 2
GEEKNEWS_MIN = 1
TOTAL = 7

GITHUB_LIMIT = 25
HN_LIMIT = 30
REDDIT_LIMIT_PER_SUB = 10
REDDIT_SUBREDDITS = ["LocalLLaMA", "ClaudeAI", "SaaS"]
