import json
import re
import requests

from app.config import OPENROUTER_API_KEY
from app.config import OPENROUTER_MODEL


class AIService:

    URL = "https://openrouter.ai/api/v1/chat/completions"

    # ---------------------------------------------------------
    # Generic Chat Method
    # ---------------------------------------------------------

    def chat(self, prompt, temperature=0, max_tokens=3500):

        print("\n================ OPENROUTER REQUEST ================")
        print("Model :", OPENROUTER_MODEL)
        print("API Key :", OPENROUTER_API_KEY[:20] + "...")
        print("====================================================\n")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """
You are an Executive Competitive Intelligence Analyst.

Your audience is CEOs, CXOs and Strategy Teams.

Always prioritize:

- Business impact
- Competitor moves
- Manufacturing
- Investments
- Supply Chain
- Regulations
- Product Launches
- AI Adoption
- Financial Results

Never invent facts.

Whenever JSON is requested,
return ONLY valid JSON.
"""
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:

            response = requests.post(
                self.URL,
                headers=headers,
                json=payload,
                timeout=180,
            )

            print("\n============= OPENROUTER RESPONSE =============")
            print("Status Code :", response.status_code)
            print(response.text)
            print("===============================================\n")

            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:

            print("\nHTTP ERROR")
            print(e)

            try:
                print(response.json())
            except:
                print(response.text)

            raise

        except Exception as e:

            print("\nUnexpected Error")
            print(e)

            raise

    # ---------------------------------------------------------
    # Article Analysis
    # ---------------------------------------------------------

    def analyze_articles(self, industry, articles):

        article_text = ""

        for i, article in enumerate(articles, start=1):

            article_text += f"""
Article {i}

Title:
{article.get("title","")}

Description:
{article.get("description","")}

Source:
{article.get("source","")}

Published:
{article.get("publishedAt","")}

URL:
{article.get("url","")}

------------------------------------------------------------
"""

        prompt = f"""
You are the Head of Corporate Strategy for a Fortune 500 company.

Industry:
{industry}

Your job is to decide whether each article deserves to appear
on an Executive Intelligence Dashboard.

Approve ONLY articles about

• Investments
• Funding
• Acquisitions
• Mergers
• Product launches
• Manufacturing
• Supply Chain
• Logistics
• Pricing
• Consumer demand
• Technology
• AI
• Digital Transformation
• Partnerships
• Government policy
• Regulation
• Sustainability
• ESG
• Market Reports
• Industry Reports
• Financial Results

Reject

• Sports
• Movies
• Entertainment
• Celebrity
• Lifestyle
• Recipes
• Stock recommendations
• Editorials
• Opinion pieces
• Generic company pages

For EVERY article return

show_on_dashboard
dashboard_score
company
country
category
importance
summary
business_impact
recommended_action
confidence

Return ONLY VALID JSON.

Example

[
{{
"article_number":1,
"show_on_dashboard":true,
"dashboard_score":95,
"company":"Nestlé",
"country":"India",
"category":"Manufacturing",
"importance":"High",
"summary":"Nestlé announced a new manufacturing facility.",
"business_impact":"Production capacity increases.",
"recommended_action":"Monitor expansion.",
"confidence":97
}}
]

Articles

{article_text}
"""

        text = self.chat(prompt)

        print("\n=============== AI RAW RESPONSE =================")
        print(text)
        print("=================================================\n")

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()

        try:

            data = json.loads(text)

        except Exception as e:

            print("\nJSON Parsing Error")
            print(e)
            print(text)

            return []

        if isinstance(data, dict):

            return data.get("articles", [])

        return data