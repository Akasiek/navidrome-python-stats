# Navidrome Python Statistics

## Python

### Setup

```bash
# 1. Utwórz i aktywuj venv
python -m venv .venv && source .venv/bin/activate

# 2. Zainstaluj zależności
pip install -e .

# 3. Skopiuj .env.example i uzupełnij dane
cp .env.example .env
```

### Development

```bash
uvicorn main:app --app-dir src --reload
```

### Environment Variables

- `NAVIDROME_URL`
- `NAVIDROME_USER`
- `NAVIDROME_PASSWORD`
