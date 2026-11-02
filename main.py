"""Demostración ejecutable del cálculo de nómina."""
from datetime import date

from nomina import (
    CommissionEmployee,
    HourlyEmployee,
    PayrollCalculator,
    SalariedEmployee,
    TemporaryEmployee,
)


def format_currency(amount):
    return f"${amount:,.2f}"


def main():
    # Tasa académica ilustrativa: reemplazar por la que indique el curso/empresa.
    calculator = PayrollCalculator(arl_rate="0.00522")
    employees = [
        SalariedEmployee("E001", "Ana Pérez", "3000000", years_of_service=6),
        HourlyEmployee("E002", "Luis Rojas", "15000", "45", years_of_service=2,
                       accepts_savings_fund=True),
        CommissionEmployee("E003", "Marta Gil", "2500000", "22000000", "0.05"),
        TemporaryEmployee("E004", "Juan Díaz", "2000000", date(2026, 12, 31)),
    ]
    for employee in employees:
        slip = calculator.calculate(employee)
        print(f"\nRecibo de {slip.employee_name} ({slip.employee_id})")
        print(f"  Salario bruto:       {format_currency(slip.gross_salary)}")
        print(f"  Seguridad/pensión:   {format_currency(slip.social_security_and_pension)}")
        print(f"  ARL:                 {format_currency(slip.arl)}")
        print(f"  Fondo de ahorro:     {format_currency(slip.savings_fund)}")
        print(f"  Salario neto:        {format_currency(slip.net_salary)}")
        print(f"  Alimentación empresa:{format_currency(slip.employer_meal_benefit)}")


if __name__ == "__main__":
    main()
