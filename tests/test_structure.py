
from analyzer.structure import analyze_structure


def test_if_elif_else():
    code = """
temperature = 32

if temperature >= 35:
    print("Hot")
elif temperature >= 25:
    print("Warm")
else:
    print("Cool")
"""
    result = analyze_structure(code)

    assert result["valid"] is True
    assert result["if_branches"] == 2
    assert result["for_loops"] == 0


def test_loops():
    code = """
for number in range(5):
    print(number)

while False:
    print("Never runs")
"""
    result = analyze_structure(code)

    assert result["for_loops"] == 1
    assert result["while_loops"] == 1


def test_functions():
    code = """
def calculate_total(price, quantity):
    return price * quantity
"""
    result = analyze_structure(code)

    assert result["functions"] == 1


def test_invalid_syntax():
    code = "if age >= 13\n    print(age)"

    result = analyze_structure(code)

    assert result["valid"] is False
    assert result["if_branches"] is None
    assert result["functions"] is None
