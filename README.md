# Sistema académico de nómina — Unidad 3

## Requisitos y ejecución

- Python 3.10 o superior.
- No requiere paquetes externos.

Desde la carpeta raíz:

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

## Reglas implementadas

- **Asalariado:** salario mensual fijo; bono del 10 % si tiene **más de cinco años** de antigüedad.
- **Por horas:** hasta 40 horas semanales a tarifa normal; las horas por encima de 40 a 1,5 veces la tarifa.
- **Por comisión:** salario base más comisión sobre ventas; bono del 3 % de las ventas cuando estas superan $20.000.000.
- **Temporal:** salario mensual fijo y fecha de fin de contrato, sin bono ni bono de alimentación.
- A todos los tipos se les calcula una deducción combinada de seguridad social y pensión del 4 % del salario bruto y una deducción de ARL.
- Los empleados asalariados y por comisión reciben un bono de alimentación de $1.000.000 financiado por la empresa. Se informa por separado y **no se resta del salario neto ni se suma al salario bruto**
- El empleado por horas puede aceptar el fondo de ahorro si tiene más de un año de servicio. El 2 % se registra como descuento del neto y aporte al fondo.
- El sistema rechaza montos negativos y evita emitir un recibo con salario neto negativo.

## Decisiones 

La consigna no indica el porcentaje de ARL. Por eso el sistema recibe `arl_rate` como configuración obligatoria en `PayrollCalculator`. El programa de demostración usa `0.00522` (0,522 %) 

La consigna tampoco aclara si el 4 % de seguridad social/pensión es combinado o si aplica 4 % a cada concepto. Se implementó como **4 % combinado**, tal como está escrito. Se asume que la base para ARL es el salario bruto.

El umbral de 40 horas se interpreta como horas trabajadas en una semana. El fondo de ahorro se trata como descuento voluntario del empleado que se deposita en su cuenta de ahorro. El bono de alimentación se trata como costo/beneficio asumido por la empresa, no como dinero en efectivo del neto.

Los valores se manejan con `Decimal`, no con `float`, para evitar errores de precisión típicos en cálculos monetarios.

## Diseño orientado a objetos y SOLID

- `Employee` define el contrato común y es abstracta. Cada subtipo implementa `gross_salary()` con su propia regla; esto usa abstracción y polimorfismo.
- `PayrollCalculator` calcula deducciones y el recibo sin tener que preguntar qué clase concreta está procesando. Cada clase tiene una responsabilidad enfocada (**SRP**).
- Los tipos concretos heredan de `Employee` y pueden sustituirlo donde se requiere un empleado (**LSP**).
- Las tasas y reglas se inyectan/configuran en vez de mezclarse con las entidades, facilitando ampliar el sistema (**OCP/DIP**, en una escala de prototipo).
- El alcance pequeño no necesita interfaces separadas para cada campo del recibo; se evita agregar abstracciones innecesarias (**ISP**).

## Organización

```text
nomina/
  __init__.py
  employees.py       # Entidades y reglas específicas por tipo
  payroll.py         # Cálculo común de deducciones y recibos
main.py              # Demostración por consola
 tests/
  test_payroll.py    # Pruebas unitarias
```

## Pruebas

Las pruebas verifican bono por antigüedad, horas extra, comisión y umbral de ventas, beneficios de empleados permanentes, deducciones, ahorro voluntario, entradas negativas y salario neto no negativo. Están escritas con `unittest`, incluido en Python.

## Metodología de desarrollo para presentar

Se trabajó de forma **iterativa e incremental**, inspirada en Scrum para el proyecto académico:

1. Identificar actores, tipos de empleado, reglas y datos faltantes.
2. Modelar entidades y responsabilidades con clases.
3. Implementar el cálculo para un tipo de empleado y ejecutar pruebas.
4. Añadir los demás tipos y refactorizar el cálculo común.
5. Verificar casos límite con pruebas automatizadas.
6. Documentar y preparar la demostración.

## Control de versiones en GitHub

Para crear el repositorio local y dejar evidencia incremental, ejecute desde la carpeta:

```bash
git init
git add README.md nomina/__init__.py nomina/employees.py
git commit -m "feat: modelar tipos de empleados"
git add nomina/payroll.py main.py
git commit -m "feat: calcular recibos de nómina"
git add tests/test_payroll.py
 git commit -m "test: agregar pruebas unitarias de nómina"
git add README.md
git commit -m "docs: explicar supuestos y metodología"
```

Luego cree un repositorio vacío en GitHub, copie su URL y publique la rama `main`:

```bash
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
 git push -u origin main
```

