import tkinter as tk
from tkinter import ttk
import SmithWaterman
from ttkthemes import ThemedTk

label_seq1 = None
label_seq2 = None
label_score = None
label_subsecuencia = None
alignment_frames = []

def sequence_type(seq):
    if 'T'in seq or 't' in seq:
        return "ADN"
    elif 'U' in seq or 'u' in seq:
        return "ARN"
    else:
        return "Proteina"


def clear_results():
    global label_seq1, label_seq2, label_score, label_subsecuencia, alignment_frames
    if label_seq1:
        label_seq1.destroy()
    if label_seq2:
        label_seq2.destroy()
    if label_score:
        label_score.destroy()
    if label_subsecuencia:
        label_subsecuencia.destroy()
    for alignment_frame in alignment_frames:
        alignment_frame.destroy()
    alignment_frames = []

def visualizar_secuencias_local(root, entry_seq1, entry_seq2):
    clear_results()

    seq1 = entry_seq1.get()
    seq2 = entry_seq2.get()
    global label_seq1, label_seq2
    type_seq1=sequence_type(seq1) 
    type_seq2=sequence_type(seq2)
    if type_seq1 == type_seq2:
        label_type = ttk.Label(root,text="Tipo de la Secuencia 1: "+type_seq1)
        label_type.grid(row=3, column=0)
        label_type = ttk.Label(root,text="Tipo de la Secuencia 2: "+type_seq2)
        label_type.grid(row=4, column=0)
        label_seq1 = ttk.Label(root, text="Secuencia 1: " + seq1)
        label_seq1.grid(row=5, column=0)
        label_seq2 = ttk.Label(root, text="Secuencia 2: " + seq2)
        label_seq2.grid(row=6, column=0)

        # Mostrar los resultados en etiquetas en la ventana
        label_score = ttk.Label(root, text="Score: ")
        label_score.grid(row=7, column=0)

        # Crear la etiqueta label_subsecuencia antes de configurar su texto y ubicación
        label_subsecuencia = ttk.Label(root, text="Subsecuencia: ")
        label_subsecuencia.grid(row=8, column=0)

        # Obtener los resultados de alineamiento después de asignar valores a las secuencias
        max_value, alignments, pos_maxvalue = SmithWaterman.get_results_local(seq1, seq2)

        # Actualizar las etiquetas de resultados con los valores obtenidos
        label_score.config(text="Score: " + str(max_value))
        label_score.grid(row=9, column=0)

        row = 10
        for i in range(len(alignments)):
            alignment_frame = tk.LabelFrame(root, padx=5, pady=5)  # Contenedor del alineamiento
            alignment_frame.grid(row=row, column=0, columnspan=2)
            label_subsecuencia.config(text="Subsecuencia: " + str(alignments[i]) + " Posicion: " + "[" + str(pos_maxvalue[i][0]) + "," + str(pos_maxvalue[i][1]) + "]")
            label_subsecuencia.grid(row=row, column=0)
            alignment_frames.append(alignment_frame)
            row += 1

    else:
        label_type_error = ttk.Label(root,text="No se pueden alinear dos secuencias de tipos distintos")
        label_type_error.grid(row=3, column=0)
  


def alineamiento_local():
    root = ThemedTk(theme="breeze")  # Tema "arc" de ttkthemes
    root.configure(bg=root.cget('background'))
    root.geometry("690x720")
    root.title("Visualización de Alineamiento Local de Secuencias")

    title_label = ttk.Label(root, text="Alineamiento Local de Secuencias", font=("Arial", 30, "bold"))
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

    button_align = ttk.Button(root, text="Alinear", command=lambda: visualizar_secuencias_local(root, entry_seq1, entry_seq2))
    button_align.grid(row=2, column=0, pady=20)

    root.mainloop()

