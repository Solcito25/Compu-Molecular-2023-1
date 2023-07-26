import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

def dot_plot(seq1, seq2, root):
    matrix = [[0] * len(seq2) for _ in range(len(seq1))]

    # Construir la matriz de puntos
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                matrix[i][j] = '*'
            else:
                matrix[i][j] = ' '

    # Crear un ttk.LabelFrame para agrupar las etiquetas
    label_frame = ttk.LabelFrame(root, text="Matriz de Puntos")
    label_frame.grid(row=5, column=0, columnspan=len(seq2)+1, padx=10, pady=10)

    # Agregar los encabezados de secuencia en la primera fila de la matriz
    for j, char in enumerate(seq2):
        label_header = ttk.Label(label_frame, text=char, width=3, relief="solid")
        label_header.grid(row=0, column=j+1, padx=1, pady=1)

    # Crear las etiquetas para cada posición de la matriz dentro del LabelFrame
    for i in range(len(seq1)):
        label_header = ttk.Label(label_frame, text=seq1[i], width=3, relief="solid")
        label_header.grid(row=i+1, column=0, padx=1, pady=1)

        for j in range(len(seq2)):
            value = matrix[i][j]
            if value != 0:
                label = ttk.Label(label_frame, text=str(value), width=3, relief="solid")
                if value == '*':
                    if i+1 < len(seq1) and j+1 < len(seq2) and matrix[i+1][j+1] == "*":
                        label.configure(background="green")
                    elif i-1 >= 0 and j-1 >= 0 and matrix[i-1][j-1] == "*":
                        label.configure(background="green")
                    else:
                        label.configure(background="yellow")
                label.grid(row=i+1, column=j+1, padx=1, pady=1)

def visualizar_matriz_puntos(root, entry_seq1, entry_seq2):
    seq1 = entry_seq1.get()
    seq2 = entry_seq2.get()

    # Eliminar los valores de las entradas después de usarlos
    entry_seq1.delete(0, tk.END)
    entry_seq2.delete(0, tk.END)

    # Llamar a dot_plot para mostrar la matriz de puntos en root
    dot_plot(seq1, seq2, root)

def alineamiento_matriz_puntos():
    root = ThemedTk(theme="breeze")  # Tema "arc" de ttkthemes
    root.configure(bg=root.cget('background'))
    root.geometry("690x720")
    root.title("Visualización de Matriz de Puntos")

    title_label = ttk.Label(root, text="Alineamiento con Matriz de Puntos", font=("Arial", 30, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=(40, 20))

    frame = ttk.Frame(root, width=500, height=200)
    frame.grid(row=1, column=0)

    label_seq1 = ttk.Label(frame, text="Secuencia 1:")
    label_seq1.grid(row=0, column=0)

    entry_seq1 = ttk.Entry(frame, width=50, font=("Arial", 12))
    entry_seq1.grid(row=1, column=0)

    label_seq2 = ttk.Label(frame, text="Secuencia 2:")
    label_seq2.grid(row=2, column=0)

    entry_seq2 = ttk.Entry(frame, width=50, font=("Arial", 12))
    entry_seq2.grid(row=3, column=0)

    button_align = ttk.Button(root, text="Alinear", command=lambda: visualizar_matriz_puntos(root, entry_seq1, entry_seq2))
    button_align.grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()

