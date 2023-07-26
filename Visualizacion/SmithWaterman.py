import numpy as np
max_value = 0
pos_maxvalue =[]
def scores(m_scores, m_dir, i, j, seq_max, seq_min):
    global max_value 
    global pos_maxvalue
    if seq_max[i - 1] == seq_min[j - 1]:
        a = [1 + m_scores[i - 1][j - 1], "d"]
    else:
        a = [m_scores[i - 1][j - 1] - 1,"d"]
    b = [m_scores[i - 1][j] - 2,"l"] # GAP
    c = [m_scores[i][j - 1] - 2, "u"] # GAP
    d = [0,"s"]
    list_score = [a, b, c, d]
    max_score = max(list_score, key=lambda x: x[0])
    m_scores[i][j]= max_score[0]
    #Copiar las direcciones de donde viene el max score
    list_dir=[]
    for score, direction in list_score:
        if score == max_score[0]:
            list_dir.append(direction)
    m_dir[i][j] = list_dir
    #Guardar el valor maximo la direccion donde se encuentra
    if len(pos_maxvalue)==0:
        max_value=max_score[0]
        pos_maxvalue.append((i,j))
    elif max_value< max_score[0]:
        max_value=max_score[0]
        pos_maxvalue.clear()
        pos_maxvalue.append((i,j))
    elif max_value==max_score[0]:
        pos_maxvalue.append((i,j))
    #return max_value,pos_maxvalue   
    
def get_alignments(m_scores,seq_max, m_dir,pos_maxvalue):
    alignments = []
    for pos in pos_maxvalue:
        alignment = ''
        i, j = pos
        score_maximo=max_value
        while m_dir[i][j] and m_scores[i][j] > 0:
            if score_maximo==m_scores[i][j]:
                alignment = seq_max[i-1] + alignment
                i-=1
                j-=1
                score_maximo-=1
            else:
                break
        if len(alignment)==max_value and m_scores[i][j]==0:
            alignments.append(alignment)        
    return alignments

def get_results_local(seq1,seq2):
    #Comparar cual secuencia es la mas larga
    if len(seq1)>len(seq2):
        max_len=len(seq1)
        min_len=len(seq2)
        seq_max = seq1
        seq_min = seq2
    else:
        max_len=len(seq2)
        min_len=len(seq1)
        seq_max = seq2
        seq_min = seq1

    #Matriz de scores
    m_scores=np.zeros((max_len+1, min_len+1)) 
    #Matriz de direcciones
    m_dir = np.empty((len(seq_max) + 2, len(seq_min) + 2), dtype=object)

    #Completar la matriz de scores y direcciones
    for i in range(1,max_len+1):
        for j in range(1,min_len+1):
            #max_value,posmaxvalue=
            scores(m_scores, m_dir, i, j, seq_max, seq_min)

    # Obtener los alineamientos como strings
    alignments = get_alignments(m_scores,seq_max, m_dir,pos_maxvalue)
    return max_value, alignments, pos_maxvalue



    



