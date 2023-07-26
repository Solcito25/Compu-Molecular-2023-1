import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import gui_global
import gui_local
import gui_star
import gui_proteinasblosum
import gui_matrizpuntos
import gui_watsoncrick


root_main = ThemedTk(theme="breeze")  
root_main.configure(bg=root_main.cget('background'))
root_main.geometry("555x720")
root_main.title("Visualizador")
title_label = ttk.Label(root_main, text="Visualizador", font=("Arial", 30, "bold"))
title_label.pack(pady=40)

button_frame = ttk.Frame(root_main)
button_frame.pack()

button1 = ttk.Button(button_frame, text="Alineamiento Global", command=gui_global.alineamiento_global)
button1.pack(pady=10)

button2 = ttk.Button(button_frame, text="Alineamiento Local", command=gui_local.alineamiento_local)
button2.pack(pady=10)

button3 = ttk.Button(button_frame, text="Alineamiento Estrella", command=gui_star.alineamiento_star)
button3.pack(pady=10)

button4 = ttk.Button(button_frame, text="Alineamiento de Proteinas", command=gui_proteinasblosum.alineamiento_proteinas_blosum)
button4.pack(pady=10)

button5 = ttk.Button(button_frame, text="Alineamiento con Matriz de Puntos", command=gui_matrizpuntos.alineamiento_matriz_puntos)
button5.pack(pady=10)

button6 = ttk.Button(button_frame, text="Predicción de Estructuras Secundarias", command=gui_watsoncrick.prediccion_estructuras_secundarias)
button6.pack(pady=10)

root_main.mainloop()
