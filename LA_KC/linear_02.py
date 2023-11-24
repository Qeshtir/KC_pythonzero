import numpy as np

# Тестовые данные 3х3
A = np.array([[1., 3., 8.],
              [4., 2., 0.],
              [7., 1., 9.]])

def singular_decomposition(matrix):
    # Матрицы для левых и правых сингулярных векторов
    AAT = np.dot(matrix, matrix.T)
    ATA = np.dot(matrix.T, matrix)
    # Найдем собственные значения и векторы матриц
    eigenvalues_left, eigenvectors_left = np.linalg.eigh(AAT)
    eigenvalues_right, eigenvectors_right = np.linalg.eigh(ATA)

    # Сортировка нужна, только чтобы сличать результат с np.linalg.svd. Матрица собирается и без этого действия
    sorted_indices = np.argsort(eigenvalues_left)[::-1]
    eigenvalues_left = eigenvalues_left[sorted_indices]
    eigenvectors_left = eigenvectors_left[:, sorted_indices]

    sorted_indices = np.argsort(eigenvalues_right)[::-1]
    eigenvalues_right = eigenvalues_right[sorted_indices]
    eigenvectors_right = eigenvectors_right[:, sorted_indices]

    # Соберём сингулярные числа (любые - правые или левые, они равны)
    singular_values = np.sqrt(eigenvalues_right)

    # region Отладка
    # Это набор отладочных принтов. Весь блок может быть закомментирован исключительно ради красоты вывода
    # print("Сингулярные значения:\n")
    # for i, eigenvalue in enumerate(singular_values):
    #     print(f"λ{i + 1} = {eigenvalue}\n")

    # print("Левые сингулярные векторы:\n")
    # for i, eigenvector in enumerate(eigenvectors_left.T):
    #     print(f"V{i + 1} = {eigenvector}\n")
    #
    # print("Правые сингулярные векторы:\n")
    # for i, eigenvector in enumerate(eigenvectors_right.T):
    #     print(f"V{i + 1} = {eigenvector}\n")
    #
    # endregion

    # Костыль с изменением знака второго вектора. В реализации необходим, т.к. по невыясненным причинам np.linalg.eigh
    # для матрицы ААТ 3х3 возвращает неверный знак для второго левого сигнулярного вектора

    for i, eigenvector in enumerate(eigenvectors_left.T):
        eigenvectors_left[i][1] = eigenvectors_left[i][1] * (-1)
    print(eigenvectors_left)

    # Собственные значения составляют диагональ матрицы сигма
    L_matrix = np.diag(singular_values)
    #
    # Сингулярные векторы составляют матрицу U и транспонированную V
    U_matrix = eigenvectors_left
    V_matrix = eigenvectors_right
    T_V_matrix = V_matrix.T
    print("U_matrix \n", U_matrix)
    print("L_matrix \n", L_matrix)
    print("VT_matrix \n", T_V_matrix)
    #
    # Проверим, что произведение компонент разложения равно исходной матрице
    temp = np.dot(U_matrix, L_matrix)
    result = np.dot(temp, T_V_matrix)
    #
    print('Произведение компонент разложения: \n')
    print(result)


singular_decomposition(A)

# вызов аналогичной функции из numpy
for i in np.linalg.svd(A):
    print(i)

