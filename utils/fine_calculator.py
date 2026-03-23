from models.loan import Loan

FINE_RATE_PER_DAY = 0.25
MAX_FINE = 20.0
GRACE_PERIOD_DAYS = 1


def calculate_fine(loan: Loan) -> float:
    billable_days = max(0, loan.overdue_days - GRACE_PERIOD_DAYS)
    return min(billable_days * FINE_RATE_PER_DAY, MAX_FINE)


def fine_report(loan: Loan) -> str:
    fine = calculate_fine(loan)
    status = "✅ returned" if loan.return_date else "🔴 not returned"
    fine_str = f"💰 Fine: {fine:.2f} €" if fine > 0 else "✅ No fine"
    return (
        f"📚 «{loan.book_title}» | 👤 {loan.user_name}\n"
        f"   Due date: {loan.due_date} | Status: {status}\n"
        f"   Overdue: {loan.overdue_days} days | {fine_str}"
    )
