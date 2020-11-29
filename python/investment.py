import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# Variables
age = 1
month_capital = 33400
percent = 0.12
need = 70000


# Functions
def get_sum(age: int, month_capital: int, percent: float) -> float:
    payment_sum = 0
    i = 0
    cash = 12 * month_capital
    while i < age:
        if i == 0:
            payment_sum = cash * percent + cash
        else:
            payment_sum = (payment_sum + cash) * percent + payment_sum + cash
        i += 1
    return round(payment_sum, 2)


def get_needed_capital(need: int) -> int:
    return round((need * 12) / percent)


def get_save_money() -> int:
    age = 0
    while get_needed_capital(need) > get_sum(age, month_capital, percent):
        get_sum(age, month_capital, percent)
        age += 1
    return age


# Action
print('After {} years on my deposit will be '.format(age) + str(locale.format_string('%d', get_sum(age, month_capital,
                                                                                                   percent),
                                                                                     grouping=True)) + ' rubles')
print('I need ' + str(locale.format_string('%d', get_needed_capital(need), grouping=True)) + ' money on my deposit')
print('It will be after ' + str(get_save_money()) + ' years')
