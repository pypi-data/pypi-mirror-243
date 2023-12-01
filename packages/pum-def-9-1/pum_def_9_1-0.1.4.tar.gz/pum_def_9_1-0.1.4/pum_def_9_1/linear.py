from pum_def_9_1.__init__ import check


def print_linear():
    print("Линейный поиск. Введите цифру интересующего алгоритма\n"
          "1. Поиск количества повторений заданного элемента\n"
          "2. Проверка встречается ли элемент в массиве\n"
          "3. Поиск максимального элемента\n"
          "4. Поиск минимального элемента\n"
          "5. Поиск индекса максимального элемента\n"
          "6. Поиск индекса минимального элемента")
    answer = input()
    correctNumbers = ['1', '2', '3', '4', '5', '6']

    checRusult = check(answer, correctNumbers)
    if checRusult == '1':
        print("""\n
Пример линейного поиска количества повторений элемента
Что ищем, массив -> Количество повторений

    def lin_amount(element, massive):
    counter = 0
    for i in range(len(massive)):
        if massive[i] == element:
            counter += 1
    return counter
    \n""")
        print_linear()

    elif checRusult == '2':
        print("""\n
Проверка встречается ли элемент в массиве
Что ищем, массив -> YES или NO
        
    def lin_flag(element, massive): 
    flag = 'NO'  
    for i in range(len(massive)):
        if massive[i] == element:
        flag = 'YES'
    return flag
    \n""")
        print_linear()

    elif checRusult == '3':
        print("""\n
Поиск максимального элемента
Массив -> Цифра максимального элемента
        
    def mx(massive):
        max_element = massive[0]
        for i in range(len(massive)):
            if massive[i] > max_element:
                max_element = massive[i]
        return max_element
        \n""")
        print_linear()
    elif checRusult == '4':
        print("""\n
Поиск минимального элемента
Массив -> Цифра минимального элемента
        
    def mn(massive):
        min_element = massive[0]
        for i in range(len(massive)):
            if massive[i] < min_element:
                min_element = massive[i]
        return min_element
        \n""")
        print_linear()
    elif checRusult == '5':
        print("""\n
Поиск индекса максимального элемента
Массив -> Индекс максимального элемента
        
    def mx_i(massive):
        max_index = 0
        for i in range(len(massive)):
            if massive[i] > massive[max_index]:
                max_index = i
        return max_index
        \n""")
        print_linear()
    elif checRusult == '6':
        print("""\n
Поиск индекса минимального элемента
Массив -> Индекс минимального элемента
        
    def mn_i(massive):
        min_index = 0
        for i in range(len(massive)):
            if massive[i] < massive[min_index]:
                min_index = i
        return min_index
        \n""")
        print_linear()
    elif checRusult == 'restart':
        print_linear()
