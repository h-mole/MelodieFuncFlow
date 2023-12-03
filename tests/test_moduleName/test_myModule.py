from ModuleTemplate.ModuleName import sum_two_numbers


def test_sum_two_numbers() -> None:
    # Arrange
    n1: int = 10
    n2: int = 20

    # Act
    expected: int = sum_two_numbers(n1, n2)

    # Assert
    assert expected == 30
