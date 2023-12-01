"""
Утилита со всеми функциями для ПУМа (pum_def_9_1)
"""


from pum_def_9_1.binary import print_binary
from pum_def_9_1.linear import print_linear
from pum_def_9_1.sort import print_sort
from pum_def_9_1.clear import clear
from sys import exit


def check(str, num):
    if str in num:
        clear()
        return str
    elif str == 'exit':
        exit()
    elif str == 'main':
        start()
    elif str.isalpha() and str != 'exit' and str != 'main':
        clear()
        print("Неправильная команда. Допустимые команды: 'exit', 'main'\n")
        return 'restart'
    elif str.isnumeric() and str not in num:
        clear()
        print(f"Неправильное число. Допустимые числа: {num}\n")
        return 'restart'
    else:
        clear()
        print('Ошибка ввода. Неправильный ввод\n')
        return 'restart'


def start():
    print("Введите цифру интересующей вас темы\n"
          "1. Линейный поиск\n"
          "2. Бинарный поиск\n"
          "3. Сортировки\n"
          "Для завершения работы введите 'exit'\n")
    select = input()
    correctNumbers = ['1', '2', '3']

    chechResult = check(select, correctNumbers)
    if chechResult == '1':
        print_linear()
    if chechResult == '2':
        print_binary()
    if chechResult == '3':
        print_sort()
    if chechResult == 'restart':
        start()

start() #первичный запуск кода