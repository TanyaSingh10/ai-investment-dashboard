import os
import json
import yfinance as yf
from openai import OpenAI

# Initialize client SAFELY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_stock_data(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "price": info.get("currentPrice", info.get("regularMarketPrice")),
            "industry": info.get("industry"),
            "website": info.get("website"),
            "source": f"yfinance ({symbol})"
        }
    except Exception as e:
        return {"error": str(e), "source": "yfinance"}


def search_knowledge_base(query: str):
    return {
        "content": "Recent earnings show a 12% YoY growth. Operating margins improved.",
        "source": "Q3 Filing"
    }


def get_news(company: str):
    return [
        {"title": f"{company} launches AI features", "sentiment": "positive", "source": "Finance Weekly"},
        {"title": f"Analysts upgrade {company}", "sentiment": "positive", "source": "Market Watch"}
    ]


def analyze_query(query: str):

    if not os.getenv("OPENAI_API_KEY"):
        raise Exception("OPENAI_API_KEY not found")

    try:
        messages = [
            {"role": "system", "content": "You are an AI investment analyst. Return JSON only."},
            {"role": "user", "content": query}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",   # ✅ UPDATED MODEL
            messages=messages
        )

        content = response.choices[0].message.content

        return {
            "result": content
        }

    except Exception as e:
        print("AI ERROR:", str(e))
        raise e