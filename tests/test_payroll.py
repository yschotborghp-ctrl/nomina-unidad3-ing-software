"""Pruebas unitarias con unittest (no requieren dependencias externas)."""
import unittest
from datetime import date
from decimal import Decimal

from nomina import (
    CommissionEmployee,
    HourlyEmployee,
    PayrollCalculator,
    SalariedEmployee,
    TemporaryEmployee,
)


class EmployeeRulesTests(unittest.TestCase):
    def test_salaried_bonus_only_after_more_than_five_years(self):
        exactly_five = SalariedEmployee("1", "A", "1000000", 5)
        over_five = SalariedEmployee("2", "B", "1000000", 6)
        self.assertEqual(exactly_five.gross_salary(), Decimal("1000000.00"))
        self.assertEqual(over_five.gross_salary(), Decimal("1100000.00"))

    def test_hourly_overtime_is_paid_at_one_and_a_half(self):
        employee = HourlyEmployee("1", "A", "10000", "45")
        self.assertEqual(employee.regular_pay, Decimal("400000.00"))
        self.assertEqual(employee.overtime_pay, Decimal("75000.00"))
        self.assertEqual(employee.gross_salary(), Decimal("475000.00"))

    def test_commission_and_sales_bonus_above_threshold(self):
        employee = CommissionEmployee("1", "A", "1000000", "21000000", "0.10")
        self.assertEqual(employee.commission, Decimal("2100000.00"))
        self.assertEqual(employee.bonus, Decimal("630000.00"))
        self.assertEqual(employee.gross_salary(), Decimal("3730000.00"))

    def test_commission_bonus_not_paid_at_exact_threshold(self):
        employee = CommissionEmployee("1", "A", "1000000", "20000000", "0.10")
        self.assertEqual(employee.bonus, Decimal("0.00"))

    def test_temporary_employee_has_no_meal_benefit(self):
        employee = TemporaryEmployee("1", "A", "2000000", date(2026, 12, 31))
        slip = PayrollCalculator("0.01").calculate(employee)
        self.assertEqual(slip.employer_meal_benefit, Decimal("0.00"))

    def test_permanent_employee_gets_employer_paid_meal_benefit(self):
        employee = SalariedEmployee("1", "A", "2000000")
        slip = PayrollCalculator("0.01").calculate(employee)
        self.assertEqual(slip.employer_meal_benefit, Decimal("1000000.00"))
        self.assertEqual(slip.net_salary, Decimal("1900000.00"))


class PayrollCalculatorTests(unittest.TestCase):
    def test_mandatory_deductions_and_configurable_arl(self):
        employee = SalariedEmployee("1", "A", "1000000")
        slip = PayrollCalculator("0.01").calculate(employee)
        self.assertEqual(slip.social_security_and_pension, Decimal("40000.00"))
        self.assertEqual(slip.arl, Decimal("10000.00"))
        self.assertEqual(slip.net_salary, Decimal("950000.00"))

    def test_savings_fund_requires_more_than_one_year_and_consent(self):
        eligible = HourlyEmployee("1", "A", "10000", "40", 2, True)
        exactly_one_year = HourlyEmployee("2", "B", "10000", "40", 1, True)
        calculator = PayrollCalculator("0")
        self.assertEqual(calculator.calculate(eligible).savings_fund, Decimal("8000.00"))
        self.assertEqual(calculator.calculate(exactly_one_year).savings_fund, Decimal("0.00"))

    def test_negative_hours_and_sales_are_rejected(self):
        with self.assertRaises(ValueError):
            HourlyEmployee("1", "A", "10000", "-1")
        with self.assertRaises(ValueError):
            CommissionEmployee("2", "B", "1000000", "-1", "0.05")

    def test_net_salary_cannot_be_negative(self):
        employee = SalariedEmployee("1", "A", "1000000")
        with self.assertRaisesRegex(ValueError, "neto no puede ser negativo"):
            PayrollCalculator("1.00").calculate(employee)

    def test_invalid_employee_name_is_rejected(self):
        with self.assertRaises(ValueError):
            SalariedEmployee("1", "  ", "1000000")


if __name__ == "__main__":
    unittest.main()
