import os
import json
import yfinance as yf
from openai import OpenAI

# Initialize client using Groq's free API (OpenAI compatible)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


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

    if not os.getenv("GROQ_API_KEY"):
        raise Exception("GROQ_API_KEY not found in .env")

    messages = [
        {"role": "system", "content": "You are an AI investment analyst. Use the available tools to gather data if needed to answer the query."},
        {"role": "user", "content": query}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_data",
                "description": "Get current stock price and information for a given ticker symbol",
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
                "name": "search_knowledge_base",
                "description": "Search the internal knowledge base for company filings and earnings reports",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_news",
                "description": "Get recent news for a company",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string", "description": "The company name"}
                    },
                    "required": ["company"]
                }
            }
        }
    ]

    try:
        # Step 1: Initial call to let the model decide on tool usage
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)
        
        # Step 2: Handle any tool calls
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except Exception:
                    arguments = {}
                
                if function_name == "get_stock_data":
                    result = get_stock_data(arguments.get("symbol"))
                elif function_name == "search_knowledge_base":
                    result = search_knowledge_base(arguments.get("query"))
                elif function_name == "get_news":
                    result = get_news(arguments.get("company"))
                else:
                    result = {"error": f"Unknown function: {function_name}"}
                    
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(result)
                })
                
        # Step 3: Final call to structure the output as JSON
        messages[0] = {
            "role": "system", 
            "content": """You are an AI investment analyst. Compile the gathered information into a final report.
You MUST return ONLY a JSON object that exactly matches this structure:
{
  "company_overview": {
    "name": "Company Name",
    "sector": "Sector"
  },
  "stock_data": {
    "price": 150.0,
    "change": "+1.5%",
    "source": "Source of data"
  },
  "risk_analysis": "Detailed analysis of risks based on filings and news...",
  "news": [
    {
      "title": "News headline",
      "source": "News source",
      "sentiment": "positive"
    }
  ],
  "sources": ["List of all sources used"]
}"""
        }
        
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            response_format={ "type": "json_object" }
        )
        
        content = final_response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print("AI ERROR:", str(e))
        raise e