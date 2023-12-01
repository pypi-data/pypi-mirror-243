from pum_def_9_1.__init__ import check


def print_binary():
    print("Бинарный поиск. Введите цифру интересующего алгоритма\n"
          "1. Бинарный поиск слева направо\n"
          "2. Бинарный поиск справа налево\n"
          "Для выхода в главное меню введите 'main'\n"
          )
    correctNumbers = ['1', '2']
    answer = input()
    checkResult = check(answer, correctNumbers)
    if checkResult == '1':
        print(
        "Бинарный поиск слева направо\n"
        "Элемент, массив -> индекс элемента\n\n"

        "def left_bound(element, massive):\n"
        "    left = -1\n"
        "    right = len(massive)\n"
        "    while right - left > 1:\n"
        "        middle = (left + right) // 2\n"
        "        if massive[middle] < element:\n"
        "            left = middle\n"
        "        else:\n"
        "            right = middle\n"
        "    return left + 1\n"
        )
        print_binary()
    elif checkResult == '2':
        print(
        "Бинарный поиск справа налево\n"    
        "Элемент, массив -> индекс элемента\n"
        "def right_bound(element, massive):\n"
        "    left = -1\n"
        "    right = len(element)\n"
        "    while right - left > 1:\n"
        "        middle = (left + right) // 2\n"
        "        if element[middle] <= massive:\n"
        "            left = middle\n"
        "        else:\n"
        "            right = middle\n"
        "    return right - 1\n"
        )
        print_binary()
    elif checkResult == 'restart':
        print_binary()
