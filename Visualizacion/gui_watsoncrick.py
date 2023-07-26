import tkinter as tk
from tkinter import ttk
import WatsonCrick
from ttkthemes import ThemedTk

label_seq1 = None
label_score = None
label_predicciones = None
label_num_predicciones = None
predicciones_frames = []

def sequence_type(seq):
    if 'T'in seq or 't' in seq:
        return "ADN"
    elif 'U' in seq or 'u' in seq:
        return "ARN"
    else:
        return "Proteina"


def clear_results():
    global label_seq1,label_score, label_num_predicciones,label_predicciones, predicciones_frames
    if label_seq1:
        label_seq1.destroy()
    if label_score:
        label_score.destroy()
    if label_num_predicciones:
        label_num_predicciones.destroy()
    if label_predicciones:
        label_predicciones.destroy()
    for prediccion_frame in predicciones_frames:
        prediccion_frame.destroy()
    predicciones_frames = []

def visualizar_predicciones(root, entry_seq1):
    clear_results()

    seq1 = entry_seq1.get()
    global label_seq1
    type_seq1 = sequence_type(seq1) 
    if type_seq1 == "ARN":
        label_type = ttk.Label(root, text="Tipo de la Secuencia : " + type_seq1)
        label_type.grid(row=3, column=0)
        label_seq1 = ttk.Label(root, text="Secuencia: " + seq1)
        label_seq1.grid(row=4, column=0)

        # Mostrar los resultados en etiquetas en la ventana
        label_score = ttk.Label(root, text="Score: ")
        label_score.grid(row=5, column=0)

        label_num_predicciones = ttk.Label(root, text="Número de Predicciones: ")
        label_num_predicciones.grid(row=6, column=0)

        # Crear la etiqueta label_predicciones antes de configurar su texto y ubicación
        label_predicciones = ttk.Label(root, text="Predicciones: ")
        label_predicciones.grid(row=7, column=0)

        # Obtener los resultados de alineamiento después de asignar valores a las secuencias
        score, num_predicciones, predicciones = WatsonCrick.get_results_watsoncrick(seq1)

        # Actualizar las etiquetas de resultados con los valores obtenidos
        label_score.config(text="Score: " + str(score))
        label_score.grid(row=5, column=0)
        label_num_predicciones.config(text="Número de alineamientos: " + str(num_predicciones))
        label_num_predicciones.grid(row=6, column=0)

        row = 8
        for i in range(len(predicciones)):
            print(i, predicciones[i])
            # Crear una nueva etiqueta para cada predicción
            label_prediccion = ttk.Label(root, text="Predicción: " + str(predicciones[i]))
            label_prediccion.grid(row=row, column=0)
            predicciones_frames.append(label_prediccion)
            row += 1
    else:
        label_type_error = ttk.Label(root, text="Solo se pueden predecir secuencias de ARN")
        label_type_error.grid(row=3, column=0)

  


def prediccion_estructuras_secundarias():
    root = ThemedTk(theme="breeze")  # Tema "arc" de ttkthemes
    root.configure(bg=root.cget('background'))
    root.geometry("750x720")
    root.title("Visualización de Predicción de Estructuras Secundarias")

    title_label = ttk.Label(root, text="Predicción de Estructuras Secundarias", font=("Arial", 30, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=(40, 20))

    frame = ttk.Frame(root, width=500, height=200)
    frame.grid(row=1, column=0)

    label_seq1 = ttk.Label(frame, text="Secuencia:")
    label_seq1.grid(row=0, column=0)

    entry_seq1 = ttk.Entry(frame, width=50, font=("Arial", 12))
    entry_seq1.grid(row=1, column=0)

    button_align = ttk.Button(root, text="Predecir", command=lambda: visualizar_predicciones(root, entry_seq1))
    button_align.grid(row=2, column=0, pady=20)

    root.mainloop()

