import tkinter as tk
from tkinter import ttk
import Selection.util.generic as utl
from Login.forms.login.form_login import FormLogin
from Login.forms.login.Part_form_login import PartForm
from Login.forms.login.Org_form_login import OrgLogin

class FormLoginDesigner():
        
    def verificar(self):
        pass
    
    def userRegister(self):
        pass
    
    def adminAction(self):
        self.ventana.destroy()
        FormLogin()

    def PartAction(self):
        self.ventana.destroy()
        PartForm()

    def OrgAction(self):
        self.ventana.destroy()
        OrgLogin()
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)

        logo = utl.leer_imagen("./Selection/imagenes/IPN.png", (200, 200))
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300,
                              relief=tk.SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0,
                              relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # frame_form

        # frame_form_top
        frame_form_top = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill
        frame_form_fill = tk.Frame(
            frame_form, height=50,  bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        inicio = tk.Button(frame_form_fill, text="Administrador", font=(
            'Times', 15), bg='#fcfcfc', bd=0, fg="#3a7ff6", command=self.adminAction)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.adminAction()))
        
        inicio = tk.Button(frame_form_fill, text="Organizador", font=(
            'Times', 15), bg='#fcfcfc', bd=0, fg="#3a7ff6", command=self.OrgAction)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.OrgAction()))
        
        inicio = tk.Button(frame_form_fill, text="Participante", font=(
            'Times', 15), bg='#fcfcfc', bd=0, fg="#3a7ff6", command=self.PartAction)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.PartAction()))

        # end frame_form_fill
        self.ventana.mainloop()