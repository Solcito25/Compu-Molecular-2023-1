import tkinter as tk
from tkinter import ttk
import AlineamientoProteinas
from ttkthemes import ThemedTk

label_seq1 = None
label_seq2 = None
label_score = None
label_num_alineamientos = None
alignment_frames = []

def sequence_type(seq):
    if 'T'in seq:
        return "ADN"
    elif 'U' in seq:
        return "ARN"
    else:
        return "Proteina"


def clear_results():
    global label_seq1, label_seq2, label_score, label_num_alineamientos, alignment_frames
    if label_seq1:
        label_seq1.destroy()
    if label_seq2:
        label_seq2.destroy()
    if label_score:
        label_score.destroy()
    if label_num_alineamientos:
        label_num_alineamientos.destroy()
    for alignment_frame in alignment_frames:
        alignment_frame.destroy()
    alignment_frames = []

def visualizar_secuencias_proteinas_blosum(root, entry_seq1, entry_seq2):
    clear_results()

    seq1 = entry_seq1.get()
    seq2 = entry_seq2.get()
    global label_seq1, label_seq2
    type_seq1=sequence_type(seq1)
    type_seq2=sequence_type(seq2)
    if type_seq1=="Proteina"and type_seq2 == "Proteina" and type_seq1 == type_seq2:
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
        label_num_alineamientos = ttk.Label(root, text="Número de alineamientos: ")
        label_num_alineamientos.grid(row=7, column=0)

        # Obtener los resultados de alineamiento después de asignar valores a las secuencias
        score, num_alineamientos, alineamientos = AlineamientoProteinas.get_results_proteinas_blosum(seq1, seq2)

        # Actualizar las etiquetas de resultados con los valores obtenidos
        label_score.config(text="Score: " + str(score))
        label_score.grid(row=8, column=0)
        label_num_alineamientos.config(text="Número de alineamientos: " + str(num_alineamientos))
        label_num_alineamientos.grid(row=7, column=0)

        # Crear etiquetas para cada alineamiento y aplicar los colores correspondientes
        row = 35
        for alignment in alineamientos:
            alignment1_text = tk.StringVar()
            alignment2_text = tk.StringVar()
            alignment1_text.set("".join(alignment[0]))
            alignment2_text.set("".join(alignment[1]))

            alignment_frame = tk.LabelFrame(root, padx=5, pady=5)  # Contenedor del alineamiento
            alignment_frame.grid(row=row, column=0, columnspan=2)
            
            alignment1_labels = []
            alignment2_labels = []
            for char1, char2 in zip(alignment[0], alignment[1]):
                if char1 == char2:
                    label1 = ttk.Label(alignment_frame, text=char1, foreground="green")
                    label2 = ttk.Label(alignment_frame, text=char2, foreground="green")
                elif char1 == "-" or char2 == "-":
                    label1 = ttk.Label(alignment_frame, text=char1, foreground="blue")
                    label2 = ttk.Label(alignment_frame, text=char2, foreground="blue")
                else:
                    label1 = ttk.Label(alignment_frame, text=char1, foreground="red")
                    label2 = ttk.Label(alignment_frame, text=char2, foreground="red")
                alignment1_labels.append(label1)
                alignment2_labels.append(label2)

            for i in range(len(alignment1_labels)):
                alignment1_labels[i].grid(row=0, column=i, sticky="w")
                alignment2_labels[i].grid(row=1, column=i, sticky="w")

            alignment_frames.append(alignment_frame)
            row += 1

            # Agregar una etiqueta vacía para separar los alineamientos
            empty_label = ttk.Label(root, text="")
            empty_label.grid(row=row, column=0, columnspan=2)
            row += 1
    else:
        label_type_error = ttk.Label(root,text="Solo se pueden alinear proteinas")
        label_type_error.grid(row=3, column=0)

def alineamiento_proteinas_blosum():
    root = ThemedTk(theme="breeze")  # Tema "arc" de ttkthemes
    root.configure(bg=root.cget('background'))
    root.geometry("650x720")
    root.title("Visualización de Alineamiento de Proteinas")

    title_label = ttk.Label(root, text="Alineamiento Global de Proteinas", font=("Arial", 30, "bold"))
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

    button_align = ttk.Button(root, text="Alinear", command=lambda: visualizar_secuencias_proteinas_blosum(root, entry_seq1, entry_seq2))
    button_align.grid(row=2, column=0, pady=20)

    root.mainloop()

