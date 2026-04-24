import pytest
from datetime import date
from dateutil.relativedelta import relativedelta
from core.models import Ratio
from core.handlers import calculate_gains


# 1. Определяем фикстуру для Ratio
@pytest.fixture
def r_obj():
    return Ratio(1)


# 2. Определяем фикстуру для параметров
# ВАЖНО: мы передаем r_obj как аргумент, и pytest подставит сюда результат Ratio(1)
@pytest.fixture
def default_params(r_obj):
    return {
        'start_date': date(2024, 1, 1),
        'end_date': date(2025, 1, 1),
        'initial': 100000,
        'payment': 10000,
        'rate': 10,
        'period_payment': relativedelta(months=1),
        'period_profit': relativedelta(months=1),
        'tax_enabled': False,
        'inf_enabled': False,
        'ratio': r_obj  # Здесь теперь лежит объект Ratio, а не функция
    }


def test_calculate_gains_with_real_ratio(default_params):
    # Вызываем функцию расчета
    # Если в default_params['ratio'] лежит функция, будет AttributeError: ... 'down'
    result = calculate_gains(**default_params)

    assert result['current_balance'] > 100000
    assert isinstance(result['current_balance'], int)


@pytest.mark.parametrize("initial, rate, expected_min", [
    (100000, 10, 110000),
    (0, 0, 120000),
])
def test_calculate_gains_logic(default_params, initial, rate, expected_min):
    params = default_params.copy()
    params['initial'] = initial
    params['rate'] = rate

    # Если начальный капитал 0, пополняем по 10к
    if initial == 0:
        params['payment'] = 10000
    else:
        params['payment'] = 0

    result = calculate_gains(**params)
    assert result['current_balance'] >= expected_min
