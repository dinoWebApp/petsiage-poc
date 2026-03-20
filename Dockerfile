# 1. Base Image (uv가 설치된 가벼운 이미지 사용)
FROM python:3.13-slim

# 2. 시스템 의존성 설치 및 uv 환경 구축
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치 (캐시 활용)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 4. 소스 코드 복사
COPY . .

# 5. 실행 환경 설정 (Gunicorn)
# 운영 환경에서는 DEBUG=False 권장
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 8000 포트 개방
EXPOSE 8000

# 서버 실행 (uv run을 통한 가상환경 실행)
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
