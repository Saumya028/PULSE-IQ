import requests
import feedparser
from urllib.parse import quote_plus

from app.config import NEWS_API_KEY
from app.data.industries import INDUSTRIES
from app.utils.text_utils import remove_duplicate_articles
from app.utils.date_utils import is_recent
from services.filter_service import FilterService


class NewsService:

    NEWS_API_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.filter = FilterService()

    # ---------------------------------------------------------
    # Search Terms
    # ---------------------------------------------------------

    def get_search_terms(self, industry):

        industry = industry.lower()

        if industry in INDUSTRIES:
            data = INDUSTRIES[industry]

            return {
                "keywords": data["keywords"][:6],
                "companies": data["companies"][:8]
            }

        return {
            "keywords": [industry],
            "companies": []
        }

    # ---------------------------------------------------------
    # NewsAPI
    # ---------------------------------------------------------

    def fetch_newsapi(self, industry):

        search = self.get_search_terms(industry)

        queries = []

        queries.extend(search["keywords"])
        queries.extend(search["companies"])

        all_articles = []

        for query in queries:

            params = {
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5,
                "apiKey": NEWS_API_KEY
            }

            try:

                response = requests.get(
                    self.NEWS_API_URL,
                    params=params,
                    timeout=20
                )

                if response.status_code != 200:
                    continue

                data = response.json()

                for article in data.get("articles", []):

                    all_articles.append({

                        "title": article.get("title") or "",

                        "description": article.get("description") or "",

                        "url": article.get("url") or "",

                        "source": article.get("source", {}).get("name", "NewsAPI"),

                        "publishedAt": article.get("publishedAt") or ""

                    })

            except Exception:
                continue

        return all_articles

    # ---------------------------------------------------------
    # Google RSS
    # ---------------------------------------------------------

    def fetch_google_rss(self, industry):

        search = self.get_search_terms(industry)

        company_query = " OR ".join(search["companies"][:5])

        rss_queries = [

            industry,

            f"{industry} India",

            company_query,

            f"{company_query} India"

        ]

        articles = []

        for query in rss_queries:

            if not query.strip():
                continue

            url = (
                "https://news.google.com/rss/search?q="
                + quote_plus(query)
                + "&hl=en&gl=US&ceid=US:en"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries:

                articles.append({

                    "title": entry.get("title") or "",

                    "description": entry.get("summary") or "",

                    "url": entry.get("link") or "",

                    "source": "Google News",

                    "publishedAt": entry.get("published") or ""

                })

        return articles

    # ---------------------------------------------------------
    # Main Fetch
    # ---------------------------------------------------------

    def fetch_news(self, industry):

        print(f"\nSearching worldwide news for {industry}...\n")

        newsapi_articles = self.fetch_newsapi(industry)

        print(f"NewsAPI : {len(newsapi_articles)} articles")

        rss_articles = self.fetch_google_rss(industry)

        print(f"Google RSS : {len(rss_articles)} articles")

        articles = newsapi_articles + rss_articles

        print(f"Combined : {len(articles)}")

        # Debug dates
        if articles:
            print("\nSample Dates:")
            for a in articles[:5]:
                print(a["publishedAt"])

        recent_articles = []

        for article in articles:

            try:
                if is_recent(article.get("publishedAt"), 30):
                    recent_articles.append(article)
            except Exception:
                continue

        print(f"Recent (30 days) : {len(recent_articles)}")

        unique_articles = remove_duplicate_articles(recent_articles)

        print(f"After Deduplication : {len(unique_articles)}")

        filtered = self.filter.filter_articles(
            industry,
            unique_articles
        )

        print(f"After Business Filter : {len(filtered)}")

        return filtered