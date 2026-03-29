# Navidrome Python Statistics

## Setup

```bash
# 1. Utwórz i aktywuj venv
python -m venv .venv && source .venv/bin/activate

# 2. Zainstaluj zależności
pip install -e .

# 3. Skopiuj .env.example i uzupełnij dane
cp .env.example .env
```

## Uruchamianie

```bash
uvicorn main:app --app-dir src --reload
```

## Zmienne środowiskowe (`.env`)

| Zmienna              | Opis               |
|----------------------|--------------------|
| `NAVIDROME_URL`      | Adres serwera      |
| `NAVIDROME_USER`     | Login              |
| `NAVIDROME_PASSWORD` | Hasło              |
