import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from app.data.industries import INDUSTRIES


class FilterService:

    # -----------------------------
    # Business Events (Positive)
    # -----------------------------

    HIGH_VALUE_EVENTS = {

        "acquisition": 15,
        "acquire": 15,
        "acquired": 15,
        "merger": 15,

        "investment": 12,
        "invest": 12,
        "funding": 12,

        "factory": 12,
        "plant": 12,
        "manufacturing": 10,
        "production": 10,

        "expansion": 10,
        "capacity": 10,
        "facility": 10,

        "earnings": 10,
        "results": 10,
        "quarter": 10,
        "profit": 10,
        "revenue": 10,

        "launch": 8,
        "product": 8,

        "partnership": 8,
        "collaboration": 8,

        "government": 8,
        "policy": 8,
        "regulation": 8,

        "approval": 8,
        "export": 8,
        "import": 8,

        "supply chain": 8,
        "distribution": 8,
        "logistics": 8,

        "automation": 8,
        "artificial intelligence": 8,
        "ai": 8,

        "sustainability": 6,

        "pricing": 6,
        "consumer": 6,
        "retail": 6,
        "market": 6
    }

    # -----------------------------
    # Low Value Articles
    # -----------------------------

    NEGATIVE_WORDS = {

        "football": 20,
        "soccer": 20,
        "cricket": 20,
        "ipl": 20,
        "nba": 20,
        "nfl": 20,
        "golf": 20,
        "lpga": 20,

        "movie": 20,
        "film": 20,
        "actor": 20,
        "actress": 20,
        "celebrity": 20,
        "music": 20,
        "album": 20,
        "concert": 20,

        "recipe": 20,
        "travel": 20,
        "weather": 20,
        "lottery": 20,
        "horoscope": 20,

        "wedding": 20,
        "dating": 20,

        "price target": 15,
        "buy rating": 15,
        "sell rating": 15,
        "hold rating": 15,
        "analyst": 12,

        "webinar": 20,
        "masterclass": 20,
        "course": 20,
        "register": 20,
        "conference": 10,

        "top 10": 10,
        "top 20": 10,

        "opinion": 10,
        "editorial": 10
    }

    # -----------------------------
    # Trusted Sources
    # -----------------------------

    SOURCE_SCORES = {

        "reuters": 20,
        "bloomberg": 20,
        "financial times": 20,
        "wall street journal": 20,

        "cnbc": 18,

        "economic times": 17,
        "moneycontrol": 17,
        "business standard": 17,
        "mint": 17,
        "livemint": 17,

        "forbes": 15,

        "retail brew": 14,
        "food dive": 14,
        "printweek": 14,
        "packaging south asia": 14,

        "google news": 8
    }

    # ---------------------------------------------------

    def industry_score(self, industry, text):

        score = 0

        profile = INDUSTRIES.get(industry.lower())

        if not profile:
            return score

        if industry.lower() in text:
            score += 20

        for company in profile["companies"]:

            if company.lower() in text:
                score += 8

        for keyword in profile["keywords"]:

            if keyword.lower() in text:
                score += 5

        return score

    # ---------------------------------------------------

    def business_score(self, text):

        score = 0

        for word, value in self.HIGH_VALUE_EVENTS.items():

            if word in text:
                score += value

        return score

    # ---------------------------------------------------

    def negative_score(self, text):

        score = 0

        for word, value in self.NEGATIVE_WORDS.items():

            if word in text:
                score += value

        return score

    # ---------------------------------------------------

    def source_score(self, source):

        source = (source or "").lower()

        for key, value in self.SOURCE_SCORES.items():

            if key in source:
                return value

        return 5

    # ---------------------------------------------------

    def freshness_score(self, published):

        if not published:
            return 0

        try:

            if "T" in published:

                dt = datetime.fromisoformat(
                    published.replace("Z", "+00:00")
                )

            else:

                dt = parsedate_to_datetime(published)

            if dt.tzinfo is None:

                dt = dt.replace(
                    tzinfo=timezone.utc
                )

            days = (
                datetime.now(timezone.utc) - dt
            ).days

            if days == 0:
                return 20

            if days <= 1:
                return 18

            if days <= 3:
                return 15

            if days <= 7:
                return 12

            if days <= 14:
                return 8

            if days <= 30:
                return 5

            return 0

        except:

            return 0

    # ---------------------------------------------------

    def score_article(self, industry, article):

        title = article.get("title") or ""

        description = article.get("description") or ""

        text = (title + " " + description).lower()

        score = 0

        score += self.industry_score(
            industry,
            text
        )

        score += self.business_score(text)

        score += self.source_score(
            article.get("source", "")
        )

        score += self.freshness_score(
            article.get("publishedAt", "")
        )

        score -= self.negative_score(text)

        return score

    # ---------------------------------------------------

    def filter_articles(self, industry, articles):

        scored = []

        seen = set()

        for article in articles:

            title = (article.get("title") or "").strip()

            if len(title) < 10:
                continue

            normalized = re.sub(
                r"[^a-z0-9]",
                "",
                title.lower()
            )

            if normalized in seen:
                continue

            seen.add(normalized)

            score = self.score_article(
                industry,
                article
            )

            article["relevance_score"] = score

            if score >= 35:

                scored.append(article)

        scored.sort(

            key=lambda x: (
                x["relevance_score"],
                x.get("publishedAt", "")
            ),

            reverse=True

        )

        print(f"Rule Filter : {len(scored)}")

        return scored[:20]