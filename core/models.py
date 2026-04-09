from datetime import date

from dateutil.relativedelta import relativedelta


class Period:
    __ADDICTION = {
        'ежедневно': relativedelta(days=1),
        'еженедельно': relativedelta(weeks=1),
        'ежемесячно': relativedelta(months=1),
        'ежеквартально': relativedelta(months=3),
        'раз в полгода': relativedelta(months=6),
        'ежегодно': relativedelta(years=1),
    }

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f'{type(self).__name__}={self.__value}'

    def __add__(self, other):
        # Позволяет делать: period + date
        if isinstance(other, date):
            return other + self.__value
        return NotImplemented

    def __radd__(self, other):
        # Позволяет делать: date + period
        return self.__add__(other)

    def __sub__(self, other):
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, date):
            return other - self.__value
        return NotImplemented

    @property
    def duration(self):
        return self.__value

    @classmethod
    def glp(cls, key=''):
        """
        glp = get list periods
        :key: str варианты для начисления процентов и взноса платежей.
        Для процентов нет еженедельно, для пополнений нет ежедневно
        :return: List[Period]
        """
        return (
            [cls(k, v) for k, v in cls.__ADDICTION.items() if k != 'еженедельно'] if key == 'profit' else
            [cls(k, v) for k, v in cls.__ADDICTION.items() if k != 'ежедневно']
        )

    @property
    def year(self):
        return self.__value.years

    @property
    def month(self):
        return self.__value.months

    def get_year_fraction(self):  # частица года
        years = self.year
        months = self.month
        days = self.__value.days
        return years + (months / 12) + (days / 365.25)

    def times_per_year(self):  # количество раз в году
        return int(1 / self.get_year_fraction())


class Ratio:
    __STEPS = [1, 100, 500, 1000]

    def __init__(self, step):
        self.__step = step

    def __str__(self):
        return str(self.__step)

    def __repr__(self):
        return f'{type(self).__name__}={self.__step}'

    def up(self, number):
        return (number + self.__step - 1) // self.__step * self.__step

    def down(self, number):
        return number // self.__step * self.__step

    @classmethod
    def get_steps(cls):
        return [cls(v) for v in cls.__STEPS]

