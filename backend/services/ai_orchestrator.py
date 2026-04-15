import os
import json
import yfinance as yf
from openai import OpenAI

def get_stock_data(symbol: str):
    """Fetch current stock data using yfinance."""
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
        return {"error": f"Failed to fetch stock data: {str(e)}", "source": "yfinance"}

def search_knowledge_base(query: str):
    """Simulates searching a document knowledge base for earnings/filings."""
    # In a real app, you would read from data/ or query a vector DB like Supabase/FAISS
    return {
        "content": "Recent earnings show a 12% YoY growth. Operating margins improved by 200 bps.",
        "source": "Q3 10-Q Filing Extract"
    }

def get_news(company: str):
    """Simulate getting recent news for a company."""
    # In a real app, you would call NewsAPI or AlphaVantage
    return [
        {"title": f"{company} launches new AI features", "sentiment": "positive", "source": "Finance Weekly"},
        {"title": f"Analysts upgrade {company} stock target", "sentiment": "positive", "source": "Market Watch"}
    ]

def analyze_query(query: str):
    """
    Main orchestration function.
    Uses OpenAI function calling to gather data, then generates structured JSON response.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Development fallback
        return {
            "company_overview": {"name": "Example Corp", "sector": "Technology"},
            "stock_data": {"price": 100.5, "change": "+5.2%", "source": "Mock Data"},
            "news": [{"title": "API Key Missing - Mock News", "sentiment": "neutral", "link": "#", "source": "Local System"}],
            "risk_analysis": "This is a mock response because OPENAI_API_KEY is not set.",
            "sources": ["Mock System"]
        }

    client = OpenAI(api_key=api_key)
    
    # We define tools the LLM can use
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_data",
                "description": "Get current stock price and fundamental data for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "The stock ticker symbol, e.g., AAPL"}
                    },
                    "required": ["symbol"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_news",
                "description": "Get recent news and sentiment for a company.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string", "description": "The name of the company"}
                    },
                    "required": ["company"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": "Search local documents like earnings reports and 10-Q filings.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query related to earnings or financials"}
                    },
                    "required": ["query"]
                }
            }
        }
    ]

    # Initial call to LLM
    system_prompt = """
    You are an expert AI Investment Analyst. 
    Use the provided tools to gather data if needed.
    Always output your final answer as JSON matching this schema:
    {
      "company_overview": {"name": "...", "sector": "..."},
      "stock_data": {"price": ..., "change": "...", "source": "..."},
      "news": [{"title": "...", "sentiment": "positive/negative/neutral", "link": "...", "source": "..."}],
      "risk_analysis": "...",
      "sources": ["source1", "source2"]
    }
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        
        available_functions = {
            "get_stock_data": get_stock_data,
            "get_news": get_news,
            "search_knowledge_base": search_knowledge_base,
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            function_response = function_to_call(**function_args)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response),
            })

        # Second call to get final JSON
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )
        return json.loads(second_response.choices[0].message.content)

    # If no tool calls, just ask for JSON output
    fallback_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        response_format={"type": "json_object"}
    )
    return json.loads(fallback_response.choices[0].message.content)
