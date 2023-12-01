"""
Проверка на наличие ошибок в воде
"""


from pum_def_9_1.clear import clear


def check(str, num):
    if str in num:
        clear()
        return str
    elif str == 'exit':
        exit()
    elif str == 'main':
        clear()
        return 'return_main'
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