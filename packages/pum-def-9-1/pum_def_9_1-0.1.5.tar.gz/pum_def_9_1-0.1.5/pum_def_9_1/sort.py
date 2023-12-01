"""
Сортировки
"""


from pum_def_9_1.error_check import check


def print_sort():
    print("Сортировки. Введите цифру интересующего алгоритма\n"
          "Сложность O(n^2):\n"
          "1. Пузырёк\n"
          "2. Вставка\n"
          "3. Выбор\n"
          "Сложность О(n):\n"
          "4. Подсчет\n"
          "5. Слияние\n"
          "Сложность О(log(n)):\n"
          "6. Быстрая"
          )
    answer = input()
    correct_numbers = ['1', '2', '3', '4', '5', '6']

    check_result = check(answer, correct_numbers)
    if check_result == '5':
        print("""\n
Сортировка слиянием
Массив -> Отсортированный масcив
def merge(A, B):
    res = []
    i = 0
    j = 0
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            res.append(A[i])
            i += 1
        else:
            res.append(B[j])
            j += 1
    res += A[i:] + B[j:]
    return res

def merge_sort(massive):
    if len(massive) <= 1:
        return(massive)
    else:
        l = massive[:len(massive)//2]
        r = massive[len(massive)//2:]
    return (
        merge(merge_sort(l), merge_sort(r)))
print(*merge_sort(a))
\n""")
        print_sort()

    elif check_result == '3':
        print("""\n
Сортировка выбором максимума
Массив -> Отсортированный массив

def select_sort(massive):
    for i in range(len(massive)-1):
        x = massive[i]
        m = i
        for j in range(i+1, len(massive)):
            if a[j] < x:
                x = massive[j]
                m = j
        massive[m], massive[i] = massive[i], massive[m]
    print(*massive)
        \n""")
        print_sort()

    elif check_result == '2':
        print("""\n
Сортировка вставкой
Массив -> Отсортированный массив

def insertion_sort(massive):
    for i in range(1,len((massive))):
        temp = massive[i]
        j = i - 1
        while (j >= 0 and temp < massive[j]):
            massive[j+1] = massive[j]
            j = j - 1
        massive[j+1] = temp
    return massive
print(*insertion_sort(a))
         \n""")
        print_sort()

    elif check_result == '1':
        print("""\n
Сортировка пузырьком
Массив -> Отсортированный массив

def buble_sort(massive):
    for i in range(len(massive)-1):
        for j in range(len(massive)-i-1):
            if massive[j+1] < massive[j]:
                massive[j], massive[j+1] = massive[j+1], massive[j]
    print(*massive)
             \n""")
        print_sort()

    elif check_result == '4':
        print("""\n
Сортировка подсчетом
Массив -> Отсортированный массив
    
def mx(massive):
    max_element = massive[0]
    for i in range(len(massive)):
        if massive[i] > max_element:
            max_element = massive[i]
    return max_element


def mn(massive):
    min_element = massive[0]
    for i in range(len(massive)):
        if massive[i] < min_element:
            min_element = massive[i]
    return min_element
    

def count_sort(massive):
    count = defaultdict(int)

    for i in massive:
        count[i] += 1
    result = []
    for j in range(mn(massive), (mx(massive)+1)):
        if count.get(j) is not None:
            for i in range(count.get(j)):
                result.append(j)
    return result
print(*count_sort(a))
             \n""")
        print_sort()

    elif check_result == '6':
        print("""\n
    Быстрая сортировка
    Массив -> Отсортированный массив
    
import random
a = list(map(int, input().split()))
def quick_sort(massive):
    if len(massive)<= 1:
        return massive
    else:
        q = random.choice(massive)
        l_nums = [n for n in massive if n < q]
        e_nums = [q]
        r_nums = [n for n in massive if n > q]
        return quick_sort(l_nums) + e_nums + quick_sort(r_nums)

print(*quick_sort(a))
             \n""")
        print_sort()
    elif check_result == 'restart':
        print_sort()
    elif check_result == 'return_main':
        return