from models.loan import Loan

FINE_RATE_PER_DAY = 0.25   # €/день
MAX_FINE = 20.0             # максимальный штраф €
GRACE_PERIOD_DAYS = 1       # 1 день без штрафа


def calculate_fine(loan: Loan) -> float:
    billable_days = max(0, loan.overdue_days - GRACE_PERIOD_DAYS)
    return min(billable_days * FINE_RATE_PER_DAY, MAX_FINE)


def fine_report(loan: Loan) -> str:
    fine = calculate_fine(loan)
    status = "✅ сдана" if loan.return_date else "🔴 не сдана"
    fine_str = f"💰 Пеня: {fine:.2f} €" if fine > 0 else "✅ Пени нет"
    return (
        f"📚 «{loan.book_title}» | 👤 {loan.user_name}\n"
        f"   Срок: {loan.due_date} | Статус: {status}\n"
        f"   Просрочено: {loan.overdue_days} дн. | {fine_str}"
    )
