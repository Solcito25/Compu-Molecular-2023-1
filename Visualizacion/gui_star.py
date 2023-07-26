import tkinter as tk
from tkinter import ttk
import AlineamientoEstrella
from ttkthemes import ThemedTk

label_seq = []
entry_seq = []
result_labels = []
button_align=0

def clear_results():
    global result_labels
    for label in result_labels:
        label.destroy()
    result_labels = []

def clear_input_fields():
    global label_seq, entry_seq
    for label in label_seq:
        label.destroy()
    for entry in entry_seq:
        entry.destroy()
    label_seq = []
    entry_seq = []

def sequence_type(seq):
    if 'T' in seq or 't' in seq:
        return "ADN"
    elif 'U' in seq or 'u' in seq:
        return "ARN"
    else:
        return "Proteina"


def visualizar_secuencias_star(root, num_seq):
    global button_align
    clear_results()

    seq_matrices = []

    for i in range(num_seq):
        seq = entry_seq[i].get()
        type_seq = sequence_type(seq)

        label_type = ttk.Label(root, text="Tipo de la Secuencia {}: {}".format(i + 1, type_seq))
        label_type.grid(row=i * 4 + 3, column=0)

        label_seq = ttk.Label(root, text="Secuencia {}: {}".format(i + 1, seq))
        label_seq.grid(row=i * 4 + 4, column=0)

        label_empty = ttk.Label(root, text=" ")
        label_empty.grid(row=i * 4 + 5, column=0)

        seq_matrices.append(seq)

    button_align.destroy()

    m_allscores, alg_multp = AlineamientoEstrella.get_results_star(seq_matrices)

    result_label = ttk.Label(root, text="Matiz de Scores:")
    result_label.grid(row=num_seq * 4 + 3, column=0)
    result_labels.append(result_label)

    result_text = ttk.Label(root, text=str(m_allscores))
    result_text.grid(row=num_seq * 4 + 4, column=0)
    result_labels.append(result_text)

    result_label = ttk.Label(root, text="Matrix de Alineamientos:")
    result_label.grid(row=num_seq * 4 + 5, column=0)
    result_labels.append(result_label)

    result_text = ttk.Label(root, text=str(alg_multp))
    result_text.grid(row=num_seq * 4 + 6, column=0)
    result_labels.append(result_text)

    clear_input_fields()


def alineamiento_star():
    global button_align
    root = ThemedTk(theme="breeze")
    root.configure(bg=root.cget('background'))
    root.geometry("700x720")
    root.title("Visualización de Alineamiento Estrella de Múltiples Secuencias")

    title_label = ttk.Label(root, text="Alineamiento Estrella de Secuencias", font=("Arial", 30, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=(40, 20))

    frame = ttk.Frame(root, width=500, height=200)
    frame.grid(row=1, column=0)

    label_num_seq = ttk.Label(frame, text="Número de Secuencias:")
    label_num_seq.grid(row=0, column=0)

    entry_num_seq = ttk.Entry(frame, width=10, font=("Arial", 12))
    entry_num_seq.grid(row=1, column=0)

    def create_input_fields():
        global button_align
        num_seq = int(entry_num_seq.get())
        
        for i in range(num_seq):
            label = ttk.Label(frame, text="Secuencia {}:".format(i + 1))
            label.grid(row=(i+1) * 2, column=0, padx=5, pady=5)
            label_seq.append(label)

            entry = ttk.Entry(frame, width=50, font=("Arial", 12))
            entry.grid(row=(i+1) * 2 + 1, column=0, padx=5, pady=5)
            entry_seq.append(entry)

        empty_label = ttk.Label(frame, text="")
        empty_label.grid(row=num_seq * 2, column=0)

        button_create_fields.destroy()  # Borrar el botón "Crear Campos de Entrada"

        button_align = ttk.Button(root, text="Ingresar Secuencias", command=lambda: visualizar_secuencias_star(root, num_seq))
        button_align.grid(row=num_seq + 3, column=0, pady=20)

    button_create_fields = ttk.Button(frame, text="Crear Campos de Entrada", command=create_input_fields)
    button_create_fields.grid(row=1, column=1, padx=10)

    root.mainloop()



