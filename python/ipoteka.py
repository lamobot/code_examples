#import telebot
import calendar
import locale
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# Variables
ostatok_dolga = 1110111
percents = 8.25
last_payment = datetime(2033, 11, 25)
first_payment = datetime(2018, 9, 25)
in_months = 0
#bot = telebot.TeleBot('');

# Functions
def get_days_of_month(in_months):
    if (datetime.now().month + in_months) > 12:
        in_months = (datetime.now().month + in_months) % 12
        in_year = datetime.now().year + (datetime.now().month + in_months) // 12
    else:
        in_year = datetime.now().year
        in_months = datetime.now().month + in_months
    return calendar.monthrange(in_year, in_months)[1]

def get_days_of_year():
    if calendar.isleap(date.today().year) == True:
        return 366
    else:
        return 365

def get_sum_payment(percents):
    month_percents = percents / 12 / 100
    k = (month_percents * (1 + month_percents) ** get_months(last_payment)) / ((1 + month_percents) **
                                                                               get_months(last_payment) - 1)
    return round(k * ostatok_dolga)

def get_months(last_payment):
    now = datetime.now()
    i = 0
    while now < last_payment:
        now = now + relativedelta(months=+1)
        i += 1
    return i - 1

def ostatok_dolga_in_months(ostatok_dolga, in_months):
    i = 0
    if in_months == 0:
        return ostatok_dolga
    while i < in_months:
        sum_of_percents = ostatok_dolga * ((percents * get_days_of_month(in_months)) / (100 * get_days_of_year()))
        sum_k_pogasheniyu = get_sum_payment(percents) - sum_of_percents
        ostatok_dolga = ostatok_dolga - sum_k_pogasheniyu
        i += 1
    return round(ostatok_dolga)


# Action
sum_of_percents = round(ostatok_dolga * ((percents * get_days_of_month(in_months)) / (100 * get_days_of_year())))
sum_k_pogasheniyu = get_sum_payment(percents) - sum_of_percents

# Print
if in_months == 0:
    print('Остаток долга: ' + str(locale.format_string('%d', ostatok_dolga, grouping=True)) + ' руб:', end='\n\n')
    print('Сумма платежа составляет ' + str(locale.format_string('%d', get_sum_payment(percents), grouping=True)) + ' руб:')
    print(' - Из них платеж по процентам - ' + str(locale.format_string('%d', sum_of_percents, grouping=True)) + ' руб:')
    print(' - Погашение основного долга - ' + str(locale.format_string('%d', sum_k_pogasheniyu, grouping=True)) + ' руб:')
else:
    print()
    print('Через ' + str(in_months) + ' месяцев при сумме платежа ' +
          str(locale.format_string('%d', get_sum_payment(percents), grouping=True)) + ' рублей остаток долга составляет '
          + str(locale.format_string('%d', ostatok_dolga_in_months(ostatok_dolga, in_months), grouping=True)) + ' рублей')
