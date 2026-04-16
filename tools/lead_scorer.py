"""
Tool 2 — Lead Scorer
Uses OpenAI to analyze a company profile and score it as a B2B lead.
"""

import os
import json
from openai import OpenAI


def score_lead_data(
    company_name: str, industry: str, size: str, website: str = ""
) -> dict:
    """Use OpenAI to score a lead based on company profile."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "error": "OPENAI_API_KEY not configured. Add it to config/.env",
            "company": company_name,
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""You are a B2B lead scoring expert for an AI automation agency.

Score the following company as a potential client on a scale of 1-10.

Company: {company_name}
Industry: {industry}
Size: {size}
Website: {website or "Not provided"}

Consider these factors:
1. Industry fit — Does this industry benefit from AI/automation? (tech, finance, healthcare, e-commerce = high)
2. Company size — Mid-size to enterprise companies (50+ employees) have bigger budgets
3. Digital maturity — Companies with websites and tech presence are more likely buyers
4. Pain points — Industries with repetitive processes, data entry, customer support = high potential

Respond in this exact JSON format and nothing else:
{{
    "score": <number 1-10>,
    "confidence": "<high/medium/low>",
    "reasoning": "<2-3 sentence explanation>",
    "key_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
    "recommended_approach": "<one sentence on how to pitch them>"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )

        content = response.choices[0].message.content.strip()
        # Clean markdown code fences if present
        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)
        result["company"] = company_name
        return result

    except json.JSONDecodeError:
        return {
            "company": company_name,
            "score": 5,
            "reasoning": content,
            "error": "Could not parse structured response",
        }
    except Exception as e:
        return {"error": f"OpenAI request failed: {str(e)}", "company": company_name}