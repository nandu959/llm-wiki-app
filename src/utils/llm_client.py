from dotenv import load_dotenv
from openai import OpenAI

import os

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

load_dotenv()


#MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")
client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key=os.getenv("OLLAMA_API_KEY", "ollama")
)

def normalize_ollama_host(host: str | None) -> str:
    host = (host or "http://127.0.0.1:11434").strip()

    if not host.startswith(("http://", "https://")):
        host = f"http://{host}"

    if host.startswith("http://0.0.0.0:"):
        host = host.replace("http://0.0.0.0:", "http://127.0.0.1:", 1)

    host = host.rstrip("/")
    if not host.endswith("/v1"):
        host = f"{host}/v1"

    return host

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text