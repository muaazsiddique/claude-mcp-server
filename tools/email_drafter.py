"""
Tool 3 — Email Drafter
Uses OpenAI to generate personalized cold outreach emails.
"""

import os
import json
from openai import OpenAI


def draft_email_data(
    company_name: str, industry: str, context: str = ""
) -> dict:
    """Generate a personalized cold outreach email using OpenAI."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "error": "OPENAI_API_KEY not configured. Add it to config/.env",
            "company": company_name,
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""You are an expert B2B cold email copywriter for an AI automation agency.

Write a personalized cold outreach email to:

Company: {company_name}
Industry: {industry}
Additional Context: {context or "None provided"}

The email should:
1. Have a compelling, short subject line (under 8 words)
2. Open with something specific about THEIR company (not generic)
3. Highlight ONE specific pain point in their industry that AI can solve
4. Briefly mention what your agency does (AI automation, custom AI tools, workflow optimization)
5. End with a soft CTA (not pushy — suggest a quick chat)
6. Be under 150 words
7. Sound human, not salesy

Respond in this exact JSON format and nothing else:
{{
    "subject_line": "<subject>",
    "email_body": "<the full email>",
    "follow_up_note": "<one sentence tip for follow-up timing>"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)
        result["company"] = company_name
        return result

    except json.JSONDecodeError:
        return {
            "company": company_name,
            "email_body": content,
            "error": "Could not parse structured response",
        }
    except Exception as e:
        return {"error": f"OpenAI request failed: {str(e)}", "company": company_name}