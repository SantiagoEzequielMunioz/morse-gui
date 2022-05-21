from tkinter import Button, Frame, Label, Text, Tk, Toplevel, IntVar, LabelFrame, Radiobutton
from morse import convertir_a_morse,velocidad
from PIL import ImageTk, Image

# la clase 'Aplicacion' hereda de la clase 'Frame' perteneciente a tkinter
class Aplicacion(Frame):
# Frame tiene de arg obligatorio el nombre del root donde estaría contenido el frame que creamos
# root es el objeto de la ventana principal // root=Tk() // frame1=Frame(root,*args)
    def __init__(self,master=None):
# con super llamo al constructor de la clase Frame(padre)
        super().__init__(master)
        self.master = master
        
        self.grid_rowconfigure((0,1,2,3,4),weight=1)
        # self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=1)

        # config visual
        self.config(bg='#D1B295',padx=10)
        self.pack(fill='both', expand=1,anchor='center') 
        # variable donde estará asociada a la imagen para la Rx
        self.imagen_nolamp=ImageTk.PhotoImage(Image.open('media/bombilla.jpg'))
        self.imagen_lamp=ImageTk.PhotoImage(Image.open('media/lamp-expanded.png'))

        # ---WIDGETS---
        # cuadros conversores Morse
        self.caja_ent=Text(self,width=60,height=15,font='C')
        self.boton_convertir=Button(self,text='CONVERTIR A MORSE',width=20,command=self.conversion)
        self.boton_ejercicio=Button(self,text='EJERCICIO',width=20,command=self.seg_ventana)
        self.boton_borrar=Button(self,text='BORRAR CAMPOS',width=20,command=self.borrado)
        self.caja_sal=Text(self,width=60,height=15,font='C')
        
        # variable cambiante relacionada a la velocidad a recibir
        self.vel=IntVar()
        # estas son las opciones para que el user elija la velocidad a utilizar en la recepcion Morse
        self.lb_vel=LabelFrame(self,text="Velocidad de Recepción",labelanchor='n')        
        self.boton_veloc1=Radiobutton(self.lb_vel,text='Velocidad: 8 grupos',variable=self.vel,value=1)
        self.boton_veloc2=Radiobutton(self.lb_vel,text='Velocidad: 10 grupos',variable=self.vel,value=2)
        self.boton_veloc3=Radiobutton(self.lb_vel,text='Velocidad: 12 grupos',variable=self.vel,value=3)

        # ubicaciones de widgets conversores
        self.caja_ent.grid(row=0,column=0,rowspan=4,pady=10,padx=10,sticky='nsew')
        self.boton_convertir.grid(row=1,column=1,pady=10)
        self.boton_borrar.grid(row=2,column=1,pady=10) 
        self.boton_ejercicio.grid(row=3,column=1,pady=10)
        self.caja_sal.grid(row=4,column=0,pady=10,padx=10,sticky='nsew')

        # ubicaciones de widgets velocidad
        self.lb_vel.grid(row=4,column=1,pady=10,padx=1)
        self.boton_veloc1.pack(anchor='w')
        self.boton_veloc2.pack(anchor='w')
        self.boton_veloc3.pack(anchor='w')
    
    def conversion(self):
        # limpia lo que haya quedado en el cuadro texto
        self.caja_sal.delete('1.0','end-1c')
        try:
            salida = convertir_a_morse(self.caja_ent.get('1.0','end-1c'))
        except:
            print("ALGUN CARACTER FUE NO VÁLIDO")
        return self.caja_sal.insert('1.0',salida)
    
    def borrado(self):
        self.caja_sal.delete('1.0','end-1c')
        self.caja_ent.delete('1.0','end-1c')

    def seg_ventana(self):
        # self.master.withdraw() ESTO NO LO USO PORQUE CUANDO VOLVÍA NO PARABA LA EJECUCION
        self.win=Toplevel()
        # win.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
        self.win.geometry('1100x680+10+10')
        self.win.config(bg='black')
        self.win.title('Señales visuales')

        # relacion de aspecto para hacerla medianamente responsive
        # lbl_img se expande con grid(sticky='nswe')
        self.win.grid_rowconfigure(0,weight=4)
        self.win.grid_rowconfigure(1,weight=1)
        self.win.grid_columnconfigure((0,1),weight=1)
        
        self.lbl_img = Label(self.win,image=self.imagen_nolamp,bg='black')
        self.lbl_img.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky='nswe')

        self.codigo = '-.-'
        self.tiempo = velocidad(60)
        boton_volver=Button(self.win,text='VOLVER',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.win.destroy)
        self.boton_comenzar=Button(self.win,text='COMENZAR',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.espera)
        boton_volver.grid(row=1,column=0,ipadx=15,ipady=10)
        self.boton_comenzar.grid(row=1,column=1,ipadx=15,ipady=10)

    def actualizar_img(self):
        self.lbl_img['image']=self.imagen_lamp
        
    
    def tiempo_muerto(self):
        self.lbl_img['image']=self.imagen_nolamp

    # def secuencia(self):
    #     codigo = '-.-'  #self.caja_sal.get('1.0','end-1c')
    #     en_curso=True
    #     # logica de opcion de velocidad
    #     # ...
    #     tiempo = velocidad(60)
    #     while en_curso:
    #         self.boton_comenzar['text']='DETENER'
    #         for c in codigo:
    #             self.win.after(5000,self.actualizar_img)
    #             self.win.after(int(tiempo[c]),self.tiempo_muerto)
    #         en_curso=False
    #     self.boton_comenzar['text']='COMENZAR'
    #     # interrumpe el proceso
    #     # ...

    # probar con decorador
    def espera(self):
        self.win.after(500,self.secuencia)


    def secuencia(self,codigo=str('-.-')):
        
        tiempo = velocidad(60)  # tiempo = {'-':1000,'.':300,' ':3000}
        self.boton_comenzar['text']='DETENER'
        for c in codigo:
            codigo=codigo.pop(0)
            self.win.after(int(tiempo[c]),self.secuencia,codigo)
            
            self.boton_comenzar['text']='COMENZAR'
    
if __name__ == '__main__':

    root=Tk()
    root.title('Manipulador Morse')
    root.geometry('700x580+0+0')
    root.minsize(700,580)
    root.maxsize(900,720)
    app = Aplicacion(root)
    app.mainloop()

