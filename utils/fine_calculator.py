from typing import Optional

from abstractions.protocols import FinePolicy
from models.loan import Loan

FINE_RATE_PER_DAY = 0.25
MAX_FINE = 20.0
GRACE_PERIOD_DAYS = 1


class StandardFinePolicy:
    """Default overdue fine rules (OCP: new rules = new FinePolicy implementation)."""

    def calculate(self, loan: Loan) -> float:
        billable_days = max(0, loan.overdue_days - GRACE_PERIOD_DAYS)
        return min(billable_days * FINE_RATE_PER_DAY, MAX_FINE)


_DEFAULT_POLICY = StandardFinePolicy()


def calculate_fine(loan: Loan) -> float:
    return _DEFAULT_POLICY.calculate(loan)


def fine_report(loan: Loan, policy: Optional[FinePolicy] = None) -> str:
    active = policy or _DEFAULT_POLICY
    fine = active.calculate(loan)
    status = "✅ returned" if loan.return_date else "🔴 not returned"
    fine_str = f"💰 Fine: {fine:.2f} €" if fine > 0 else "✅ No fine"
    return (
        f"📚 «{loan.book_title}» | 👤 {loan.user_name}\n"
        f"   Due date: {loan.due_date} | Status: {status}\n"
        f"   Overdue: {loan.overdue_days} days | {fine_str}"
    )
