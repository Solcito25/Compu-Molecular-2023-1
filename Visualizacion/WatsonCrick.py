import numpy as np
min_value = 0
pos_minvalue = []
def calculate_min_score(m_scores, i, j):
    list_min_score = []
    for k in range(i+1, j):
        list_min_score.append(m_scores[i][k] + m_scores[k+1][j])
    if len(list_min_score) == 0:
        return 0
    else:
        return min(list_min_score)

def complemento(i, j, seq):
    comp = seq[i] + seq[j]
    if comp == "GC" or comp == "CG" or comp == "AU" or comp == "UA":
        return -1
    else:
        return 0

def scores(m_scores, m_dir, i, j, seq):
    global min_value
    global pos_minvalue

    a = [m_scores[i+1][j], "a"]  # abajo
    b = [m_scores[i][j-1], "l"]  # left
    c = [m_scores[i+1][j-1] + complemento(i, j, seq), "d"]  # diagonal
    d = [calculate_min_score(m_scores, i, j), None]  # ninguna

    list_score = [a, b, c, d]
    min_score = min(list_score, key=lambda x: x[0])
    m_scores[i][j] = min_score[0]
    # Copiar las direcciones de donde viene el max score
    list_dir = []
    list_only_score = []
    for score, direction in list_score:
        list_only_score.append(score)
        if score == min_score[0] and direction!= None:
            list_dir.append(direction)
    #print("i",i,"j",j,"list_only_score ",list_only_score)
    if sum(list_only_score) != 0:
        m_dir[i][j] = list_dir
    else:
        m_dir[i][j] = ["a"]
    # Guardar la direccion de valor minimo
    if len(pos_minvalue) == 0:
        min_value = min_score[0]
        pos_minvalue.append((i, j))
    elif min_value > min_score[0]:
        min_value = min_score[0]
        pos_minvalue.clear()
        pos_minvalue.append((i, j))
    elif min_value == min_score[0]:
        pos_minvalue.append((i, j))

def get_predictions(seq, i, j, m_dir, m_scores):
    if i > j:
        return [""]
    if i == j:
        return [seq[i]]

    predicciones = []

    directions = m_dir[i][j]
    if directions is not None:  # Verificar si directions no es None
        for direction in directions:
            prediccion = ""
            if direction == "d":
                prediccion += seq[i] + seq[j] + "-"
                sub_predicciones = get_predictions(seq, i + 1, j - 1, m_dir, m_scores)
                for sub_prediccion in sub_predicciones:
                    predicciones.append(prediccion + sub_prediccion)

            elif direction == "a":
                prediccion += seq[i] + "-"
                sub_predicciones = get_predictions(seq, i + 1, j, m_dir, m_scores)
                for sub_prediccion in sub_predicciones:
                    predicciones.append(prediccion + sub_prediccion)
    return predicciones


def get_results_watsoncrick(seq1):
    len_seq = len(seq1)
    # Matriz de scores
    m_scores = np.zeros((len_seq, len_seq))
    # Matriz de direcciones
    m_dir = [[None] * len_seq for _ in range(len_seq)]

    # Iterar sobre la matriz en diagonales
    for d in range(1, len_seq):
        for i in range(len_seq - d):
            j = i + d
            scores(m_scores, m_dir, i, j, seq1)

    predicciones = get_predictions(seq1, pos_minvalue[0][0], pos_minvalue[0][1], m_dir, m_scores)

    return min_value,len(predicciones),predicciones #score, num_predicciones, predicciones

