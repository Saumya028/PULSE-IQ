from services.executive_brief_service import ExecutiveBriefService
from models.intelligence import Intelligence

articles = []

a = Intelligence()

a.headline = "PepsiCo opens ₹1,266 crore plant in India"
a.summary = "PepsiCo expanded manufacturing."
a.company = "PepsiCo"
a.country = "India"
a.category = "Manufacturing"
a.priority = "High"
a.business_impact = "Increased production capacity."
a.recommended_action = "Monitor competitors."

articles.append(a)

brief = ExecutiveBriefService().generate(
    "FMCG",
    articles
)

print(brief)