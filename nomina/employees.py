"""Entidades de dominio para los distintos tipos de empleado."""
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def to_money(value: Decimal | int | float | str, field_name: str) -> Decimal:
    """Convierte un valor a dinero y rechaza entradas negativas o no numéricas."""
    try:
        amount = Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} debe ser un valor numérico válido") from None
    if amount < 0:
        raise ValueError(f"{field_name} no puede ser negativo")
    return amount


def to_rate(value: Decimal | int | float | str, field_name: str) -> Decimal:
    """Valida una tasa expresada como fracción (por ejemplo, 0.10 representa 10 %)."""
    try:
        rate = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} debe ser una tasa numérica válida") from None
    if rate < 0 or rate > 1:
        raise ValueError(f"{field_name} debe estar entre 0 y 1")
    return rate


class Employee(ABC):
    """Contrato común: cada subtipo calcula su salario bruto de manera propia."""

    def __init__(self, employee_id: str, name: str, years_of_service: int = 0) -> None:
        if not employee_id.strip() or not name.strip():
            raise ValueError("El identificador y el nombre son obligatorios")
        if years_of_service < 0:
            raise ValueError("Los años de servicio no pueden ser negativos")
        self.employee_id = employee_id.strip()
        self.name = name.strip()
        self.years_of_service = years_of_service

    @abstractmethod
    def gross_salary(self) -> Decimal:
        """Devuelve el salario bruto del periodo, redondeado a centavos."""

    @property
    def is_permanent(self) -> bool:
        return False

    @property
    def qualifies_for_savings_fund(self) -> bool:
        return False

    @property
    def accepts_savings_fund(self) -> bool:
        return False


class SalariedEmployee(Employee):
    """Empleado permanente con salario fijo y bono por antigüedad."""

    def __init__(self, employee_id: str, name: str, monthly_salary: Decimal | int | float | str,
                 years_of_service: int = 0) -> None:
        super().__init__(employee_id, name, years_of_service)
        self.monthly_salary = to_money(monthly_salary, "El salario mensual")

    @property
    def is_permanent(self) -> bool:
        return True

    def bonus(self) -> Decimal:
        if self.years_of_service > 5:
            return (self.monthly_salary * Decimal("0.10")).quantize(CENT, rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    def gross_salary(self) -> Decimal:
        return self.monthly_salary + self.bonus()


class HourlyEmployee(Employee):
    """Empleado pagado por horas; las horas semanales sobre 40 son extra."""

    def __init__(self, employee_id: str, name: str, hourly_rate: Decimal | int | float | str,
                 hours_worked: Decimal | int | float | str, years_of_service: int = 0,
                 accepts_savings_fund: bool = False) -> None:
        super().__init__(employee_id, name, years_of_service)
        self.hourly_rate = to_money(hourly_rate, "La tarifa por hora")
        self.hours_worked = to_money(hours_worked, "Las horas trabajadas")
        self._accepts_savings_fund = accepts_savings_fund

    @property
    def accepts_savings_fund(self) -> bool:
        return self._accepts_savings_fund

    @property
    def qualifies_for_savings_fund(self) -> bool:
        return self.years_of_service > 1 and self.accepts_savings_fund

    @property
    def regular_pay(self) -> Decimal:
        regular_hours = min(self.hours_worked, Decimal("40"))
        return (regular_hours * self.hourly_rate).quantize(CENT, rounding=ROUND_HALF_UP)

    @property
    def overtime_pay(self) -> Decimal:
        overtime_hours = max(self.hours_worked - Decimal("40"), Decimal("0"))
        return (overtime_hours * self.hourly_rate * Decimal("1.5")).quantize(CENT, rounding=ROUND_HALF_UP)

    def gross_salary(self) -> Decimal:
        return self.regular_pay + self.overtime_pay


class CommissionEmployee(Employee):
    """Empleado permanente con salario base, comisión y bono por ventas."""

    BONUS_SALES_THRESHOLD = Decimal("20000000.00")
    BONUS_RATE = Decimal("0.03")

    def __init__(self, employee_id: str, name: str,
                 base_salary: Decimal | int | float | str,
                 sales: Decimal | int | float | str,
                 commission_rate: Decimal | int | float | str,
                 years_of_service: int = 0) -> None:
        super().__init__(employee_id, name, years_of_service)
        self.base_salary = to_money(base_salary, "El salario base")
        self.sales = to_money(sales, "Las ventas")
        self.commission_rate = to_rate(commission_rate, "La tasa de comisión")

    @property
    def commission(self) -> Decimal:
        return (self.sales * self.commission_rate).quantize(CENT, rounding=ROUND_HALF_UP)

    @property
    def bonus(self) -> Decimal:
        if self.sales > self.BONUS_SALES_THRESHOLD:
            return (self.sales * self.BONUS_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    @property
    def is_permanent(self) -> bool:
        return True

    def gross_salary(self) -> Decimal:
        return self.base_salary + self.commission + self.bonus


class TemporaryEmployee(Employee):
    """Empleado temporal con salario fijo y fecha de fin de contrato."""

    def __init__(self, employee_id: str, name: str,
                 monthly_salary: Decimal | int | float | str,
                 contract_end: date, years_of_service: int = 0) -> None:
        super().__init__(employee_id, name, years_of_service)
        if not isinstance(contract_end, date):
            raise ValueError("La fecha de fin del contrato debe ser una fecha válida")
        self.monthly_salary = to_money(monthly_salary, "El salario mensual")
        self.contract_end = contract_end

    def gross_salary(self) -> Decimal:
        return self.monthly_salary
