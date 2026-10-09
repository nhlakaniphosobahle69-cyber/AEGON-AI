# AEGON AI Finance Assistant
# A single-file Python app for personal finance analysis and AI-style recommendations.

from __future__ import annotations

import json
from typing import Dict, List


class FinancialInsightAI:
    """Simple rule-based AI assistant for finance management."""

    def __init__(self, name: str = "AEGON"):
        self.name = name

    def analyze_budget(self, income: float, expenses: Dict[str, float]) -> Dict[str, object]:
        total_expenses = sum(expenses.values())
        savings = income - total_expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        category_breakdown = {
            category: round((amount / total_expenses) * 100, 2) if total_expenses > 0 else 0
            for category, amount in expenses.items()
        }

        risks = []
        if savings < 0:
            risks.append("Your expenses exceed your income. Consider reducing discretionary spending.")
        if savings_rate < 10:
            risks.append("Savings rate is below a healthy benchmark. Increase emergency savings or cut non-essential costs.")

        suggestions = []
        if "housing" in expenses and expenses["housing"] > income * 0.35:
            suggestions.append("Housing costs are high. Review rent or mortgage costs and look for lower-cost alternatives.")
        if "food" in expenses and expenses["food"] > income * 0.15:
            suggestions.append("Food spending is elevated. Set a grocery budget and reduce impulse purchases.")
        if savings > 0:
            suggestions.append("Your positive cash flow is healthy. Consider investing a portion in emergency savings or low-risk assets.")

        if not suggestions:
            suggestions.append("Your financial behavior is balanced. Continue tracking spending and review costs monthly.")

        return {
            "income": income,
            "total_expenses": total_expenses,
            "savings": savings,
            "savings_rate_percent": round(savings_rate, 2),
            "category_breakdown_percent": category_breakdown,
            "financial_health": "Strong" if savings_rate >= 20 else "Moderate" if savings_rate >= 10 else "At Risk",
            "risks": risks,
            "suggestions": suggestions,
        }

    def summarize(self, result: Dict[str, object]) -> str:
        health = result["financial_health"]
        income = result["income"]
        savings = result["savings"]
        rate = result["savings_rate_percent"]
        return (
            f"AEGON AI Summary: Based on an income of ${income:.2f}, your monthly savings are "
            f"${savings:.2f} with a savings rate of {rate:.2f}%. Overall health status: {health}."
        )


def ask_for_monthly_budget() -> Dict[str, float]:
    print("\nAEGON Financial Assessment")
    print("Enter your monthly expenses by category. Use numbers only.")

    categories = ["housing", "food", "transport", "utilities", "insurance", "health", "entertainment", "shopping", "debt", "other"]
    values: Dict[str, float] = {}

    for category in categories:
        raw = input(f"{category.title()} amount: ").strip()
        try:
            values[category] = float(raw)
        except ValueError:
            values[category] = 0.0

    return values


def main() -> None:
    print("Welcome to AEGON AI")
    print("Your personal finance intelligence dashboard\n")

    try:
        monthly_income = float(input("Monthly income: ").strip())
    except ValueError:
        monthly_income = 0.0

    expenses = ask_for_monthly_budget()
    ai = FinancialInsightAI("AEGON")
    report = ai.analyze_budget(monthly_income, expenses)

    print("\n--- AI Financial Report ---")
    print(ai.summarize(report))
    print(f"Total expenses: ${report['total_expenses']:.2f}")
    print(f"Savings: ${report['savings']:.2f}")
    print(f"Savings rate: {report['savings_rate_percent']:.2f}%")
    print(f"Financial health: {report['financial_health']}")

    print("\nCategory breakdown (% of total expenses):")
    for category, percent in report["category_breakdown_percent"].items():
        if percent > 0:
            print(f"- {category.title()}: {percent}%")

    if report["risks"]:
        print("\nRisks:")
        for risk in report["risks"]:
            print(f"- {risk}")

    print("\nRecommendations:")
    for suggestion in report["suggestions"]:
        print(f"- {suggestion}")

    print("\nJSON output:")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
