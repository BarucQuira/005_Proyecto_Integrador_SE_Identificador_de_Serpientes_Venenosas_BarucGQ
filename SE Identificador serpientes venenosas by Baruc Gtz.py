# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:17:58 2023

@author: Baruc Gutiérrez Quirarte
"""

import json

import tkinter as tk
from PIL import Image, ImageTk

from tkinter import simpledialog, messagebox

from difflib import get_close_matches



class MiVentana:
    def __init__(self, master, VenIm):
        self.VenIm = VenIm
        self.master = master
        self.serpientes = self.cargar_serpientes()
        self.respuestas = []
        self.serpiente_inferida = None
        self.contador = 0
        
        
        self.respuestas_par_dicc = []
        


        # Botones Sí y No
        self.boton_si = tk.Button(self.master, text="Sí", command=lambda: self.registrar_respuesta(True))
        self.boton_si.pack(side=tk.LEFT, padx=10)
        self.boton_si.config(bg="green", fg="black")

        self.boton_no = tk.Button(self.master, text="No", command=lambda: self.registrar_respuesta(False))
        self.boton_no.pack(side=tk.LEFT, padx=10)
        self.boton_no.config(bg="red", fg="black")

        # Etiqueta de pregunta
        self.lbl_preg = tk.Label(self.master, text="Selecciona una característica:")
        self.lbl_preg.pack()

        self.caracteristicas = list(self.serpientes["Serpiente_de_Cascabel_(Crotalus)_SI_es_VENENOSA"].keys())
        self.caracteristica_actual = self.caracteristicas[0]

        self.actualizar_pregunta()

    def cargar_serpientes(self):
        try:
            with open("serpientes.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"":""}
                

    def guardar_serpientes(self):
        with open("serpientes.json", "w") as file:
            json.dump(self.serpientes, file, indent=4)

    def registrar_respuesta(self, respuesta):
        caracteristica = self.caracteristica_actual
        self.respuestas.append((caracteristica, respuesta))
        
        
        self.respNB = str(respuesta)
        self.respuestas_par_dicc.append(self.respNB)

        self.contador += 1

        if self.contador == len(self.caracteristicas):
            self.inferir_serpiente()
        else:
            self.caracteristica_actual = self.caracteristicas[self.contador]
            self.actualizar_pregunta()
    
    def convertir_a_dicc(self):
        
        self.diccionario_respuestas = {caracteristica: None for caracteristica in self.serpientes["Serpiente_de_Cascabel_(Crotalus)_SI_es_VENENOSA"]}

        # Itera sobre las serpientes en el diccionario principal
        for serpiente, caracteristicas in self.serpientes.items():
            # Itera sobre las claves de las características
            for caracteristica, respuesta in caracteristicas.items():
                # Añade la respuesta del usuario al diccionario
                if self.respuestas_par_dicc:
                    self.diccionario_respuestas[caracteristica] = self.respuestas_par_dicc.pop(0)
                else:
                    break
                
        return(self.diccionario_respuestas)
    
    
    def aprox_close(self):
        
        def obtener_caracteristicas(key, diccionario):
            """Obtiene las características de un key específico en un nuevo diccionario."""
            if key in diccionario:
                return {k: v for k, v in diccionario[key].items()}
            else:
                return {}

        def encontrar_mejor_coincidencia(respuestas_usuario, diccionario_serpientes):
            max_similarity = 0
            best_match = None

            for key in diccionario_serpientes:
                caracteristicas_serpiente = obtener_caracteristicas(key, diccionario_serpientes)
                similarity = len(set(respuestas_usuario.items()) & set(caracteristicas_serpiente.items())) / float(len(set(respuestas_usuario.items()) | set(caracteristicas_serpiente.items())))

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = key

            return best_match

       

        mejor_coincidencia = encontrar_mejor_coincidencia(self.diccionario_resp_usuario, self.serpientes)

        if mejor_coincidencia:
            return (mejor_coincidencia)
        else:
            return "No se encontró ninguna coincidencia cercana."
    
    
    
    
    

    def inferir_serpiente(self):
        for serpiente, caracteristicas in self.serpientes.items():
            coincide = all(caracteristicas[caracteristica] == str(respuesta) for caracteristica, respuesta in self.respuestas)
            if coincide:
                self.serpiente_inferida= serpiente
                break

        if self.serpiente_inferida is None:
            print("Ninguna serpiente exactamente con esas características coincide con las contenidas dentro de la base de conocimiento.")
           
            messagebox.showinfo("Advertencia", "Ninguna serpiente exactamente con esas características coincide con las contenidas dentro de la base de conocimiento.")
           
            self.diccionario_resp_usuario = self.convertir_a_dicc()
            
            print(self.diccionario_resp_usuario)
            
            
            self.posible_serpiente = self.aprox_close()
            
            
            resp= messagebox.askyesno("Mostrar posible close", f"El resultado mas cercano a tus respuestas es {self.posible_serpiente}\n¿Deseas agregar una nueva serpiente con tus caracteristicas?")
            if resp:
                nueva_serpiente = self.agregar_nueva_serpiente()
                if nueva_serpiente:
                    self.serpientes[nueva_serpiente] = {caracteristica: str(respuesta) for caracteristica, respuesta in self.respuestas}
                    self.guardar_serpientes()
                    print(f"Se ha agregado la {nueva_serpiente} a la base de conocimiento.")
                
            else:
                respuesta = messagebox.askyesno("Consultar de nuevo", "¿Deseas volver a hacer otra consultar?")
                if respuesta:
                    self.reiniciar_consulta()
                else:
                    self.VenIm.destroy()
                    self.master.destroy()
            
            
            
        else:
            serpiente_inferida_formateada = self.serpiente_inferida.replace('_', ' ')
            print(f"La base datos de conocimiento arroja que es {serpiente_inferida_formateada}")
            respuesta = messagebox.askyesno("Consultar de nuevo", f"La base datos de conocimiento arroja que es {serpiente_inferida_formateada}\n¿Deseas volver a hacer otra consultar?")
        if respuesta:
            self.reiniciar_consulta()
        else:
            self.VenIm.destroy()
            self.master.destroy()

    def agregar_nueva_serpiente(self):
        nueva_serpiente = simpledialog.askstring("Nueva Serpiente", "Ninguna serpiente coincide. Ingresa un nuevo nombre:")
        return nueva_serpiente

    def reiniciar_consulta(self):
        self.respuestas = []
        self.serpiente_inferida = None
        self.contador = 0
        self.caracteristicas = list(self.serpientes["Serpiente_de_Cascabel_(Crotalus)_SI_es_VENENOSA"].keys())
        self.caracteristica_actual = self.caracteristicas[0]
        self.actualizar_pregunta()
        
        
        self.respuestas_par_dicc = []
        

    def actualizar_pregunta(self):
        caracteristica_formateada = self.caracteristica_actual.replace('_', ' ')
        self.lbl_preg.config(text=f"¿{caracteristica_formateada}?", font=("Arial Bold", 20), fg="Pink", bg="black")
        

def iniciar_programa(venIm):
    ventana = tk.Tk()
    ventana.title("Preguntas sobre la especie")
    ventana.geometry("1200x100+80+550")
    ventana.config(bg="black")
    mi_ventana = MiVentana(ventana,venIm)
    ventana.mainloop()


    
    





class Ventana1_MostrarPers:
    def __init__(self, master):
        self.master = master

        #Etiquetas
        
        self.lbl_title = tk.Label(master, text="¡Bienvenido a tu Sistema Experto identificador de serpientes!")
        self.lbl_title.config(font=("Arial Bold", 20))
        self.lbl_title.config(fg="blue")
        self.lbl_title.place(x=250,y=10)
        
        self.lbl_title2 = tk.Label(master, text="Visualiza la serpiente a identificar")
        self.lbl_title2.config(font=("Arial Bold", 16))
        self.lbl_title2.config(fg="purple")
        self.lbl_title2.place(x=450,y=60)
        
        
        #Imagenes
        
        img_principal = Image.open("The_snakes.jpg")  
        img_principal_tk = ImageTk.PhotoImage(img_principal)
        self.lbl_img_principal = tk.Label(master, image=img_principal_tk)
        self.lbl_img_principal.image = img_principal_tk
        self.lbl_img_principal.pack()
        self.lbl_img_principal.place(x=200,y=95)
        
        
        
        #Botones
        
        self.boton_cerrar = tk.Button(master, text="Siguiente", command=self.cerrar_ventana)
        self.boton_cerrar.config(font=("Arial", 20))
        self.boton_cerrar.config(bg="red", fg="black")
        self.boton_cerrar.place(x= 850, y = 600)

    def cerrar_ventana(self):
        self.master.destroy()
        nueva_ventana = Ventana2_RondaPreg()

class Ventana2_RondaPreg:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("1200x500+80+1")
        self.master.title("Hacer preguntas sobre la especie")
        
        #Imagenes
            
        img_principal = Image.open("Serpiss.jpg")  
        img_principal_tk = ImageTk.PhotoImage(img_principal)
        self.lbl_img_principal = tk.Label(self.master, image=img_principal_tk)
        self.lbl_img_principal.image = img_principal_tk
        self.lbl_img_principal.pack()
        self.lbl_img_principal.place(x=170,y=50)
                         
        #Etiquetas
        
        self.lbl_tPers = tk.Label(self.master, text="Serpientes")
        self.lbl_tPers.config(font=("Arial Bold", 20))
        self.lbl_tPers.config(fg="green")
        self.lbl_tPers.pack()
        
        
        
        iniciar_programa(self.master)   
        
        self.master.mainloop()
    
    def cerrar_ventana(self):
        self.master.destroy()
        

    

if __name__ == "__main__":
    
    # Crear la ventana inicio
    ventana_inicio = tk.Tk()
    ventana_inicio.geometry("1200x700+80+1")
    ventana_inicio.title("Serpientes")
 

    # Crear una instancia de VentanaAnterior
    ventana = Ventana1_MostrarPers(ventana_inicio)

    ventana_inicio.mainloop()

    

