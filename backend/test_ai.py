from services.ai_service import AIService

ai = AIService()

response = ai.chat("""
Say hello.

Return JSON only.

{
    "message":"Hello"
}
""")

print(response)