from services.news_service import NewsService

service = NewsService()

articles = service.fetch_news("FMCG Nestle")

print()

print("=" * 80)

print(f"FINAL ARTICLES : {len(articles)}")

print("=" * 80)

for article in articles[:10]:

    print()

    print(article["title"])

    print(article["source"])

    print(article["publishedAt"])

    print(article["url"])

    print("-" * 80)