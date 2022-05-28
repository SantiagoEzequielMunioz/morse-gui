from tkinter import DISABLED, Button, Frame, Label, Text, Tk, Toplevel, IntVar, LabelFrame, Radiobutton, NORMAL
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
        self.fondo_negro=ImageTk.PhotoImage(Image.open('media/fondo-negro.png'))
        self.imagen_lamp=ImageTk.PhotoImage(Image.open('media/lamp-expanded.png'))
        # variable donde estará asociada a la imagen para la Rx
        

        # ---WIDGETS---
        # cuadros conversores Morse
        self.caja_ent=Text(self,width=60,height=15,font='C')
        self.boton_convertir=Button(self,text='CONVERTIR A MORSE',width=20,command=self.conversion)
        self.boton_ejercicio=Button(self,text='EJERCICIO',width=20,command=self.seg_ventana)
        self.boton_borrar=Button(self,text='BORRAR CAMPOS',width=20,command=self.borrado)
        self.caja_sal=Text(self,width=60,height=15,font='C')
        
        # variable cambiante relacionada a la velocidad a recibir
        self.vel=IntVar()
        # estas son las opciones para que el usuario elija la velocidad a utilizar en la recepcion Morse
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
        
        self.win=Toplevel()
        
        self.win.geometry('1100x680+10+10')
        self.win.config(bg='black')
        self.win.title('Señales visuales')

        # relacion de aspecto para hacerla medianamente responsive
        # lbl_img se expande con grid(sticky='nswe')
        self.win.grid_rowconfigure(0,weight=4)
        self.win.grid_rowconfigure(1,weight=1)
        self.win.grid_columnconfigure((0,1,2),weight=1)
        
        self.lbl_img = Label(self.win,text='',bg='black')
        
        self.lbl_img.grid(row=0,column=0,columnspan=3,padx=10,pady=10,sticky='nswe')

        # creo la variable inicial que tomará la opcion de velocidad
        self.velocidad=int
        
        # variable de control para detener el ejercicio
        self.ejecutando=False

        boton_volver=Button(self.win,text='VOLVER',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.win.destroy)
        self.boton_parada=Button(self.win,text='PARAR',width=15,height=1,activebackground='white',bg='grey',fg='white',state=DISABLED,command=self.comenzar)
        self.boton_comenzar=Button(self.win,text='COMENZAR',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.comenzar)
        boton_volver.grid(row=1,column=0,ipadx=15,ipady=10)
        self.boton_parada.grid(row=1,column=1,ipadx=15,ipady=10)
        self.boton_comenzar.grid(row=1,column=2,ipadx=15,ipady=10)

    # utilizo variable de control self.ejecutando para que corte con los ciclos after()
    def comenzar(self):
        print (self.lbl_img['image'])
        if self.vel.get() == None:
            # cartel advertencia de que no se eligió una velocidad
            return
        self.velocidad = self.vel.get()    

        if self.ejecutando: # si esto cumple quiere decir que se ordenó detener el programa
            self.ejecutando = False
            self.boton_comenzar.config(state=NORMAL)
            self.boton_parada.config(state=DISABLED)
            self.lbl_img['image']=self.fondo_negro
            return
        else:
        # si es la 1ra vez que comienza el ejercicio, self.ejecutando estaría en False por defecto
        # esto cambia a True y hace refresh sobre los botones, luego comienza la cuenta regresiva -> secuencia
            self.ejecutando = True
            self.boton_comenzar.config(state=DISABLED)
            self.boton_parada.config(state=NORMAL)
            self.cuenta_regresiva()


    # cuenta regresiva ejecutada por el boton comenzar
    def cuenta_regresiva(self,restante=0):
        # condicional en caso de que el usuario haya detenido el ejercicio
        # durante la cuenta regresiva
        if self.ejecutando == False:
            return
        contador = 3 + restante
        if contador <= 0:
            self.lbl_img.config(text='YA!',fg='white',font=('Verdana',100))
            self.after(1000,self.secuencia)
        else:
            self.lbl_img.config(text=f'{contador}',fg='white',font=('Verdana',100))
            restante -= 1
            self.after(1000,self.cuenta_regresiva,restante)

    # metodo de separacion entre caracter y caracter (tiempo humano)
    def espera(self,remain):
        # condicional en caso de que el usuario haya detenido el ejercicio
        # durante la espera
        if self.ejecutando == False:
            return

        # espera es la variable donde asigno el value de la key 'espera', 
        # que corresponde a la velocidad que se eligio en los radiobuttons
        espera=velocidad(self.vel.get())['espera']

        self.lbl_img['image']=self.fondo_negro
        self.win.after(espera,self.secuencia,remain)


    def secuencia(self,remain=0):
        self.lbl_img['text']=''
        #nos aseguramos que se vuelva negro el fondo en cada loop recursivo
        self.lbl_img['image']=self.fondo_negro
        try:
            codigo = self.caja_sal.get('1.0','end-2c')
        except:
            #cartel advertencia
            pass

        tiempo = velocidad(self.vel.get())
        if remain < len(codigo):
            # verifico char x char si existe en las keys del dict velocidad importado
            if (codigo[remain]) in tiempo.keys():
                # if para que si no hay un espacio o una espera, prenda la lampara
                if codigo[remain] == '-'or codigo[remain] == '.':
                    self.lbl_img['image']=self.imagen_lamp
                    print(codigo[remain],remain)
                remain += 1
                
                # remain-1 es para que tome desde el index 0 que equivale al 1er char
                # otra forma era tomar a remain inicial = -1 como defecto de argumento en esta fc
                self.win.after(tiempo[codigo[remain-1]],self.espera,remain)
            else:
                remain += 1
                self.win.after(2000,self.espera,remain)

        else:
            self.boton_comenzar.config(state=NORMAL)
            self.boton_parada.config(state=DISABLED)
            print (self.lbl_img['image'])
            self.lbl_img['image']=None
            print (self.lbl_img['image'])
            self.ejecutando = False
            return
            
            
    
if __name__ == '__main__':

    root=Tk()
    root.title('Manipulador Morse')
    root.geometry('700x580+0+0')
    root.minsize(700,580)
    root.maxsize(900,720)
    app = Aplicacion(root)
    app.mainloop()
