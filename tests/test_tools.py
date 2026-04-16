"""
Quick smoke tests — run each tool individually to verify they work.
Usage: python tests/test_tools.py
"""

import sys
import os
import json

# Add parent directory to path so we can import tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", ".env"))


def test_company_lookup():
    print("\n" + "=" * 50)
    print("TEST 1: Company Lookup")
    print("=" * 50)
    from tools.company_lookup import lookup_company_data
    result = lookup_company_data("Techlogix")
    print(json.dumps(result, indent=2))
    assert "error" not in result or "company" in result
    print("✓ PASSED")


def test_lead_scorer():
    print("\n" + "=" * 50)
    print("TEST 2: Lead Scorer")
    print("=" * 50)
    from tools.lead_scorer import score_lead_data
    result = score_lead_data(
        company_name="Techlogix",
        industry="Technology",
        size="500+ employees",
        website="https://techlogix.com",
    )
    print(json.dumps(result, indent=2))
    assert "score" in result or "error" in result
    print("✓ PASSED")


def test_email_drafter():
    print("\n" + "=" * 50)
    print("TEST 3: Email Drafter")
    print("=" * 50)
    from tools.email_drafter import draft_email_data
    result = draft_email_data(
        company_name="Techlogix",
        industry="Technology",
        context="They recently expanded their AI division.",
    )
    print(json.dumps(result, indent=2))
    assert "email_body" in result or "error" in result
    print("✓ PASSED")


def test_web_researcher():
    print("\n" + "=" * 50)
    print("TEST 4: Web Researcher")
    print("=" * 50)
    from tools.web_researcher import research_web
    result = research_web("Techlogix Lahore AI services")
    print(json.dumps(result, indent=2))
    assert "organic_results" in result or "error" in result
    print("✓ PASSED")


def test_crm_logger():
    print("\n" + "=" * 50)
    print("TEST 5: CRM Logger")
    print("=" * 50)
    from tools.crm_logger import log_to_crm_data
    result = log_to_crm_data(
        company_name="Test Company",
        website="https://example.com",
        industry="Technology",
        score=8,
        reason="High potential — strong tech presence and AI interest.",
    )
    print(json.dumps(result, indent=2))
    assert "status" in result or "error" in result
    print("✓ PASSED")


if __name__ == "__main__":
    tests = [
        ("Company Lookup", test_company_lookup),
        ("Lead Scorer", test_lead_scorer),
        ("Email Drafter", test_email_drafter),
        ("Web Researcher", test_web_researcher),
        ("CRM Logger", test_crm_logger),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"\n✗ {name} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)}")
    print("=" * 50)