from services.news_service import NewsService
from services.ai_service import AIService

news = NewsService()
ai = AIService()

articles = news.fetch_news("FMCG")

# Only first 5 for now
articles = articles[:5]

results = ai.analyze_articles("FMCG", articles)

print("\n\nFINAL RESULT\n")

for result in results:

    print("=" * 80)

    print(result)