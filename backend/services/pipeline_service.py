from sqlalchemy.orm import Session

from models.intelligence import Intelligence
from models.executive_brief import ExecutiveBrief

from services.news_service import NewsService
from services.ai_service import AIService
from services.executive_brief_service import ExecutiveBriefService


class PipelineService:

    def __init__(self):

        self.news = NewsService()

        self.ai = AIService()

        self.executive = ExecutiveBriefService()

    def run_pipeline(self, db: Session, industry: str):

        print(f"\nFetching news for {industry}...\n")

        # --------------------------------------------------
        # STEP 1 : Fetch News
        # --------------------------------------------------

        articles = self.news.fetch_news(industry)

        if not articles:
            return []

        print(f"{len(articles)} news articles fetched.\n")

        # --------------------------------------------------
        # STEP 2 : AI Analysis
        # --------------------------------------------------

        ai_results = []

        BATCH_SIZE = 5

        for i in range(0, len(articles), BATCH_SIZE):

            batch = articles[i:i+BATCH_SIZE]

            results = self.ai.analyze_articles(
                industry,
                batch
            )

            ai_results.extend(results)

        print("\n========== FINAL ARTICLES ==========\n")

        approved_articles = []
        approved_analysis = []

        for article, analysis in zip(articles, ai_results):

            print(
                article["title"],
                " ---> ",
                analysis["show_on_dashboard"]
            )

            if analysis["show_on_dashboard"]:

                approved_articles.append(article)

                approved_analysis.append(analysis)

        print()

        print("Approved :", len(approved_articles))

        print("Rejected :", len(articles) - len(approved_articles))

        print()

        # --------------------------------------------------
        # STEP 3 : Save Intelligence
        # --------------------------------------------------

        dashboard = []

        for article, analysis in zip(
            approved_articles,
            approved_analysis
        ):

            existing = (
                db.query(Intelligence)
                .filter(
                    Intelligence.url == article["url"]
                )
                .first()
            )

            if existing:

                dashboard.append(existing)

                continue

            intelligence = Intelligence(

                industry=industry,

                headline=article["title"],

                summary=analysis["summary"],

                company=analysis.get("company", ""),

                country=analysis.get("country", ""),

                category=analysis["category"],

                priority=analysis["importance"],

                business_impact=analysis.get(
                    "business_impact",
                    ""
                ),

                recommended_action=analysis.get(
                    "recommended_action",
                    ""
                ),

                dashboard_score=analysis["dashboard_score"],

                confidence=analysis["confidence"],

                source=article["source"],

                url=article["url"],

                published_at=article["publishedAt"]

            )

            db.add(intelligence)

            dashboard.append(intelligence)

        db.commit()

        dashboard.sort(
            key=lambda x: x.dashboard_score,
            reverse=True
        )

        print(f"{len(dashboard)} intelligence articles saved.\n")

        # --------------------------------------------------
        # STEP 4 : Executive Brief Generation
        # --------------------------------------------------

        print("Generating Executive Brief...\n")

        brief = self.executive.generate(
            industry,
            dashboard
        )

        if brief:

            executive = ExecutiveBrief(

                industry=industry,

                headline=brief["headline"],

                summary=brief["summary"],

                key_trends="\n".join(
                    brief["key_trends"]
                ),

                recommended_actions="\n".join(
                    brief["recommended_actions"]
                )

            )

            db.add(executive)

            db.commit()

            print("Executive Brief Saved Successfully.\n")

        else:

            print("Executive Brief generation skipped.\n")

        # --------------------------------------------------
        # STEP 5 : Return Dashboard Data
        # --------------------------------------------------

        return dashboard