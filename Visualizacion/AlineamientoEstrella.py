import numpy as np
def scores(m_scores, m_dir, i, j, seq_max, seq_min):
    if seq_max[i - 1] == seq_min[j - 1]:
        a = [1 + m_scores[i - 1][j - 1], "d"]
    else:
        a = [m_scores[i - 1][j - 1] - 1,"d"]
    b = [m_scores[i - 1][j] - 2,"l"] # GAP
    c = [m_scores[i][j - 1] - 2, "u"] # GAP
    list_score = [a, b, c]
    max_score = max(list_score, key=lambda x: x[0])
    m_scores[i][j]= max_score[0]
    list_dir=[]
    for score, direction in list_score:
        if score == max_score[0]:
            list_dir.append(direction)
    m_dir[i][j] = list_dir

    
def get_alignments(seq_max, seq_min, m_dir, max_len, min_len):
   
    alignments = [[[] for j in range(min_len+1)] for i in range(max_len+1)]
    alignments[0][0] = [("", "")]

    for i in range(1, max_len+1):
        alignments[i][0] = [(seq_max[:i], "-" * i)]

    for j in range(1, min_len+1):
        alignments[0][j] = [("-" * j, seq_min[:j])]

    for i in range(1, max_len+1):
        for j in range(1, min_len+1):
            if "d" in m_dir[i][j]:
                for alignment in alignments[i-1][j-1]:
                    alignments[i][j].append((alignment[0] + seq_max[i-1], alignment[1] + seq_min[j-1]))
            if "l" in m_dir[i][j]:
                for alignment in alignments[i-1][j]:
                    alignments[i][j].append((alignment[0] + seq_max[i-1], alignment[1] + "-"))
            if "u" in m_dir[i][j]:
                for alignment in alignments[i][j-1]:
                    alignments[i][j].append((alignment[0] + "-", alignment[1] + seq_min[j-1]))

    return alignments[max_len][min_len]


#Funcion que solo retorna el max score de dos alineamientos
def alig_global_score(seq1,seq2):
    #Comparar el tamanio de las secuencias
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
    #crear la matriz de scores con 0s
    m_scores=np.zeros((max_len+1, min_len+1)) - np.inf
    #Completar la primera columna y la primera fila de acuerdo al valor del GAP=-2
    m_scores[0,:] = np.arange(0,-(min_len*2)-2,-2)
    m_scores[:,0] = np.arange(0,-(max_len*2)-2,-2)
    #Matriz de direcciones
    m_dir = np.empty((len(seq_max) + 2, len(seq_min) + 2), dtype=object)
    #Completar la primera columna y la primera fila 
    for i in range(1,max_len+1):
        m_dir[i][0]="l"
        for j in range(1,min_len+1):
             m_dir[0][j]="u"

    #Completar la matriz de scores y direcciones
    for i in range(1,max_len+1):
        for j in range(1,min_len+1):
            scores(m_scores,m_dir,i,j,seq_max,seq_min)
    return m_scores[max_len][min_len]

#Funcion que retorna todos los alineamientos
def alig_global(seq1,seq2):
    #Comparar el tamanio de las secuencias
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
    #crear la matriz de scores con 0s
    m_scores=np.zeros((max_len+1, min_len+1)) - np.inf
    #Completar la primera columna y la primera fila de acuerdo al valor del GAP=-2
    m_scores[0,:] = np.arange(0,-(min_len*2)-2,-2)
    m_scores[:,0] = np.arange(0,-(max_len*2)-2,-2)
    #Matriz de direcciones
    m_dir = np.empty((len(seq_max) + 2, len(seq_min) + 2), dtype=object)
    #Completar la primera columna y la primera fila 
    for i in range(1,max_len+1):
        m_dir[i][0]="l"
        for j in range(1,min_len+1):
             m_dir[0][j]="u"

    #Completar la matriz de scores y direcciones
    for i in range(1,max_len+1):
        for j in range(1,min_len+1):
            scores(m_scores,m_dir,i,j,seq_max,seq_min)
    
    #Obtener alineamientos
    alignments = get_alignments(seq_max, seq_min, m_dir, max_len, min_len)
    return alignments

def get_results_star(seq):
    num_seq = len(seq)
    #Llenamos con ceros la matriz que guardara todos los scores
    m_allscores=np.zeros((num_seq, num_seq))

    #iteramos sobre la matriz como si fuera una matriz trinagular superior, se copia los valores simetricamente
    for i in range(num_seq - 1):  
        for j in range(i + 1,num_seq ):  
            if i==j: continue
            m_allscores[j][i] = m_allscores[i][j]= alig_global_score(seq[i],seq[j])
    #print("Matriz de Scores",m_allscores)

    #Elegir la secuencia que sera el centro 
    suma_mallscores=np.zeros(num_seq)
    for i in range(num_seq):
        suma_mallscores[i]=np.sum(m_allscores[i,:])
    #print("Sumatoria de las filas de m_allscores",suma_mallscores)
    pos_max_sum=np.argmax(suma_mallscores)
    seq_center=seq.pop(pos_max_sum)
    #print("Posicion de la secuencia centro",pos_max_sum)
    #print("Secuencia centro",seq_center)
    alg_seqcenter=[]
    for i in range (len(seq)):
        align=alig_global(seq_center,seq[i])[0]
        alg_seqcenter.append(align)
    #print("Alineamientos con la secuencia centro",alg_seqcenter)

    tam_seqalg=np.zeros(len(alg_seqcenter))
    for i in range (len(alg_seqcenter)):
        #print("alg = ",alg_seqcenter[i][0])
        tam_seqalg[i]=len(alg_seqcenter[i][0])
    pos_max_tam=np.argmax(tam_seqalg)
    max_tam_alig=int(tam_seqalg[pos_max_tam])
    #print(tam_seqalg)

    alg_multp=np.full((num_seq, max_tam_alig), '*')

    if len(seq_center)<max_tam_alig:
        alg_multp[0][:len(alg_seqcenter[pos_max_tam][1])] = list(alg_seqcenter[pos_max_tam][1])
        alg=alg_seqcenter.pop(pos_max_tam)
        alg=alg[0]
        alg_multp[1][:len(alg)] = list(alg)
        ##Copiar los gaps 
        for i in range(max_tam_alig):
            if alg_multp[0][i]=='-':
                for j in range(2,num_seq):
                    alg_multp[j][i]='-'
        #print("Matriz centro y matriz mayor con gaps",alg_multp)
        #cadenas alineadas con la cadena centro de menor longitud que 
        for m in range(len(alg_seqcenter)):
            alg_seqcenter[m]=alg_seqcenter[m][1]
        #print("Cadenas faltantes",alg_seqcenter)
        for k, i in zip(range(len(alg_seqcenter)), range(2, num_seq+1)):
                h=0
                for j in range (max_tam_alig):
                    if alg_multp[i][j] == '-':
                        continue
                    elif j>len(alg_seqcenter[k])-1 and h>len(alg_seqcenter[k]):
                        alg_multp[i][j] = '-'
                    else:
                        alg_multp[i][j] = alg_seqcenter[k][h]
                        h+=1
    else:
        alg_multp[:len(seq_center)] = list(seq_center)
        #cadenas alineadas con la cadena centro 
        for i in range(len(alg_seqcenter)):
            alg_seqcenter[i]=alg_seqcenter[i][1]
        for k, i in zip(range(len(alg_seqcenter)), range(1, num_seq+1)):
                h=0
                for j in range (max_tam_alig):
                    if alg_multp[i][j] == '-':
                        continue
                    elif j>len(alg_seqcenter[k])-1 and h>len(alg_seqcenter[k]):
                        alg_multp[i][j] = '-'
                    else:
                        alg_multp[i][j] = alg_seqcenter[k][h]
                        h+=1

    return m_allscores,alg_multp



