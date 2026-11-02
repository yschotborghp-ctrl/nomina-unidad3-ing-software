"""Servicio de cálculo de nómina separado de las entidades de empleados."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from .employees import Employee

CENT = Decimal("0.01")


def percentage(amount: Decimal, rate: Decimal) -> Decimal:
    return (amount * rate).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Payslip:
    employee_id: str
    employee_name: str
    gross_salary: Decimal
    social_security_and_pension: Decimal
    arl: Decimal
    savings_fund: Decimal
    net_salary: Decimal
    employer_meal_benefit: Decimal


class PayrollCalculator:
    """Calcula recibos usando tasas configurables; no depende de un tipo concreto."""

    SOCIAL_SECURITY_AND_PENSION_RATE = Decimal("0.04")
    MEAL_BENEFIT = Decimal("1000000.00")
    SAVINGS_FUND_RATE = Decimal("0.02")

    def __init__(self, arl_rate: Decimal | int | float | str) -> None:
        try:
            self.arl_rate = Decimal(str(arl_rate))
        except Exception:
            raise ValueError("La tasa de ARL debe ser numérica") from None
        if self.arl_rate < 0 or self.arl_rate > 1:
            raise ValueError("La tasa de ARL debe estar entre 0 y 1")

    def calculate(self, employee: Employee) -> Payslip:
        """Genera un recibo; las prestaciones pagadas por empresa se separan del neto."""
        gross = employee.gross_salary().quantize(CENT, rounding=ROUND_HALF_UP)
        social = percentage(gross, self.SOCIAL_SECURITY_AND_PENSION_RATE)
        arl = percentage(gross, self.arl_rate)
        savings = Decimal("0.00")
        if employee.qualifies_for_savings_fund:
            savings = percentage(gross, self.SAVINGS_FUND_RATE)
        net = gross - social - arl - savings
        if net < 0:
            raise ValueError("El salario neto no puede ser negativo")
        meal_benefit = self.MEAL_BENEFIT if employee.is_permanent else Decimal("0.00")
        return Payslip(
            employee_id=employee.employee_id,
            employee_name=employee.name,
            gross_salary=gross,
            social_security_and_pension=social,
            arl=arl,
            savings_fund=savings,
            net_salary=net,
            employer_meal_benefit=meal_benefit,
        )
