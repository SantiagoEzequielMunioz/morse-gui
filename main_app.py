from tkinter import DISABLED, LEFT, Button, Frame, Label, Text, Tk, Toplevel, IntVar, LabelFrame, Radiobutton, NORMAL, Menu, filedialog, messagebox
from morse import convertir_a_morse,velocidad,dict_to_list
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
        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=1)

        # config visual
        self.config(bg='#D1B295',padx=10)
        self.pack(fill='both', expand=1,anchor='center') 
        self.fondo_negro=ImageTk.PhotoImage(Image.open('media/fondo-negro.png'))
        self.imagen_lamp=ImageTk.PhotoImage(Image.open('media/lamp-expanded.png'))
        
        # Barra Menú
        filemenu=Menu(barra_menu,tearoff=0)
        barra_menu.add_cascade(label='Menu',menu=filemenu)
        filemenu.add_command(label='Abrir',command=self.menu_abrir)
        filemenu.add_command(label='Guardar',command=self.menu_guardar)
        filemenu.add_command(label='Convertir a Morse',command=self.conversion)
        filemenu.add_command(label='Borrar campos',command=self.borrado)
        filemenu.add_command(label='Cerrar',command=root.destroy)
        
        infomenu=Menu(barra_menu,tearoff=0)
        barra_menu.add_cascade(label='Info',menu=infomenu)
        infomenu.add_command(label='Manual',command=self.instrucciones)
        infomenu.add_command(label='Código Morse',command=self.codigo_morse)

        aboutmenu=Menu(barra_menu,tearoff=0)
        barra_menu.add_cascade(label='Acerca de',menu=aboutmenu)
        aboutmenu.add_command(label='Acerca de',command=self.menu_acerca)

        # ---WIDGETS---
        # cuadros conversores Morse
        self.caja_ent=Text(self,width=50,height=15,font='C')
        self.boton_convertir=Button(self,text='CONVERTIR A MORSE',width=20,command=self.conversion)
        self.boton_ejercicio=Button(self,text='EJERCICIO',width=20,command=self.seg_ventana)
        self.boton_borrar=Button(self,text='BORRAR CAMPOS',width=20,command=self.borrado)
        self.caja_sal=Text(self,width=50,height=14,font=('C',15))
        
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
    
    # MÉTODOS DE VENTANA PRINCIPAL

    # Funciones del Menú

    # Método para abrir un archivo de texto y posicionarlo en la caja de entrada
    def menu_abrir(self):
        abierto=filedialog.askopenfile(title='Abrir archivo de texto',
        initialdir='/',
        filetypes=(('Archivos de texto (.txt)','*.txt'),)
        )
        texto=''.join(abierto.readlines())
        self.borrado()
        return self.caja_ent.insert('1.0',texto)

    # Método que guarda el contenido de la caja de salida
    def menu_guardar(self):
        contenido=self.caja_sal.get('1.0','end-2c')
        archivo=filedialog.asksaveasfile(title='Guardar Archivo',filetypes=[('Archivos de texto','*.txt')],defaultextension='.txt')

        if archivo:
            archivo.write(contenido)
            archivo.close()

    def menu_acerca(self):
        win_instrucciones=Toplevel()
        win_instrucciones.minsize(700,350)
        win_instrucciones.title('Acerca de...')
        texto='''
Sobre mí...

Hola! Me llamo Santiago, tengo 33 años y estudio programación de manera autodidacta. Comenzó 
como un hobbie, donde le dedicaba tiempo en mis ratos libres despues del trabajo. Empecé con 
Python hace un año y ahora estoy aprendiendo Django.

Sobre el programa...

Éste programa me llevó bastante tiempo al no disponer de la práctica y conocimientos suficientes
en programación, pero finalmente pude plasmar mi idea inicial a código. Traté de realizarlo de manera
eficiente, acotando lo que pudiera pero no llevándolo a un extremo para que no se vuelva demasiado
complejo y/o inentendible en un primer vistazo.
La idea nació debido a que pertenezco a las Fuerzas Armadas, orientado en Comunicaciones y 
habitualmente realizamos ejercitaciones en Morse. 
Esta app la acoplaré a mi futuro portfolio como mi primer proyecto importante.

Puedes encontrar el repositorio en https://github.com/SantiagoEzequielMunioz/morse-gui

Muchas gracias por tu atención!       
        '''
        Label(win_instrucciones,font=('Verdana',10),text=texto,justify='left',relief='groove').pack(expand=True,fill='both')

    def codigo_morse(self):

        winmanual=Toplevel()
        winmanual.resizable(False,False)

        winmanual.title('Código Morse')
        # var es una tupla con dos listas ([keys],[values])
        var=dict_to_list()
        # separo las listas para trabajar cada una con un loop diferente
        letras,morse=var[0],var[1]
        for index,value in enumerate(letras):
            # diferencio los rangos del index para que cada 10 valores pase a otra columna
            if index < 10:
                Label(winmanual,text=value,font=('Verdana',20),fg='red').grid(row=index,column=0,padx=(15,1),pady=10)
            elif 10 <= index < 20:
                Label(winmanual,text=value,font=('Verdana',20),fg='red').grid(row=index-10,column=2,padx=(15,1),pady=10)
            elif 20 <= index < 30:
                Label(winmanual,text=value,font=('Verdana',20),fg='red').grid(row=index-20,column=4,padx=(15,1),pady=10)
            else:
                Label(winmanual,text=value,font=('Verdana',20),fg='red').grid(row=index-30,column=6,padx=(15,1),pady=10)
            
        for index,value in enumerate(morse):
            if index < 10:
                Label(winmanual,text=value,font=('Verdana',20)).grid(row=index,column=1,padx=(1,15),pady=10)
            elif 10 <= index < 20:
                Label(winmanual,text=value,font=('Verdana',20)).grid(row=index-10,column=3,padx=(1,15),pady=10)
            elif 20 <= index < 30:
                Label(winmanual,text=value,font=('Verdana',20)).grid(row=index-20,column=5,padx=(1,15),pady=10)
            else:
                Label(winmanual,text=value,font=('Verdana',20)).grid(row=index-30,column=7,padx=(1,15),pady=10)
    
    def instrucciones(self):
        win_instrucciones=Toplevel()
        win_instrucciones.minsize(700,200)
        win_instrucciones.title('Instrucciones')
        texto='''
1) Escriba el texto a traducir en Morse. También puede abrirlo desde la barra de menú. 
   Recuerde que sólo son válidos los documentos de extensión 'txt'.

2) Una vez ingresado el texto, conviértalo con el botón CONVERTIR o desde la barra de menú.

3) Seleccione la velocidad a transmitir por el programa.

4) Pulse EJERCICIO habiendo cumplido con los pasos anteriores.

5) Pulse el botón COMENZAR, y luego de transcurrida la cuenta regresiva comenzará el ejercicio.
'''
        Label(win_instrucciones,font=('Verdana',10),text=texto,justify='left').pack(expand=True,fill='both')

    # Funciones de pantalla general
    # Método para convertir de texto a morse desde la caja de entrada a la de salida
    def conversion(self):
        # limpia lo que haya quedado en el cuadro texto
        self.caja_sal.delete('1.0','end-1c')
        salida = convertir_a_morse(self.caja_ent.get('1.0','end-1c'))
        if '#' in salida:
            messagebox.showwarning('Caracteres inválidos','Algún caracter no es válido. Estará señalado con una "#"')
        return self.caja_sal.insert('1.0',salida)
    
    # Método para borrar el contenido en ambas cajas de texto
    def borrado(self):
        self.caja_sal.delete('1.0','end-1c')
        self.caja_ent.delete('1.0','end-1c')

    # SEGUNDA VENTANA (EJERCICIO)
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
        
        # label de la ventana ejercicio que contiene a la imagen
        self.lbl_img = Label(self.win,text='',bg='black')
        self.lbl_img.grid(row=0,column=0,columnspan=3,padx=10,pady=10,sticky='nswe')
        
        # variable de control para detener el ejercicio
        # la uso en los métodos cuenta_regresiva y espera
        self.ejecutando=False

        boton_volver=Button(self.win,text='VOLVER',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.win.destroy)
        self.boton_parada=Button(self.win,text='PARAR',width=15,height=1,activebackground='white',bg='grey',fg='white',state=DISABLED,command=self.comenzar)
        self.boton_comenzar=Button(self.win,text='COMENZAR',width=15,height=1,activebackground='white',bg='grey',fg='white',command=self.comenzar)
        boton_volver.grid(row=1,column=0,ipadx=15,ipady=10)
        self.boton_parada.grid(row=1,column=1,ipadx=15,ipady=10)
        self.boton_comenzar.grid(row=1,column=2,ipadx=15,ipady=10)

    # captura de error general con la secuencia
    try:
        # Método de chequeo inicial una vez que se oprime COMENZAR
        def comenzar(self):
            if self.vel.get() == 0:
                messagebox.showerror('Manipulador Morse','Antes de comenzar el ejercicio debe seleccionar una velocidad en la ventana anterior.')
                return self.win.destroy()

            # condicional por si quedó algun caracter invalido para transmitir
            captura=self.caja_sal.get('1.0','end-1c')
            if '#' in captura: 
                messagebox.showerror('Manipulador Morse','Existen caractéres inválidos en el texto a transmitir. Por favor modifique las "#" y vuelva a intentarlo.')
                return self.win.destroy()

            if self.ejecutando: # si esto cumple quiere decir que se ordenó detener el programa
                self.ejecutando = False
                self.boton_comenzar.config(state=NORMAL)
                self.boton_parada.config(state=DISABLED)
                # self.lbl_img['image']=''
                self.lbl_img.config(image='',text='CANCELADO')
                return
            else:
            # si es la 1ra vez que comienza el ejercicio, self.ejecutando estaría en False por defecto
            # esto cambia a True y hace refresh sobre los botones, luego comienza la cuenta regresiva -> secuencia
                self.ejecutando = True
                self.boton_comenzar.config(state=DISABLED)
                self.boton_parada.config(state=NORMAL)
                self.cuenta_regresiva()

        # Método de cuenta regresiva antes de lanzar el ejercicio
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

        # Método de separacion entre caracter y caracter (tiempo humano)
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

        # Secuencia principal, lo + complicado en lógica
        # toma la velocidad de transmisión para el ejercicio y el código morse en la caja de salida
        # el argumento remain hace de contador para identar sobre cada char del string morse
        def secuencia(self,remain=0):
            self.lbl_img['text']=''
            #nos aseguramos que se vuelva negro el fondo en cada loop recursivo
            self.lbl_img['image']=self.fondo_negro

            codigo = self.caja_sal.get('1.0','end-1c')
            tiempo = velocidad(self.vel.get())
            if remain < len(codigo):
                # verifico char x char si existe en las keys del dict velocidad importado
                if (codigo[remain]) in tiempo.keys():
                    # if para que si no hay un espacio o una espera, prenda la lampara
                    if codigo[remain] == '-'or codigo[remain] == '.':
                        self.lbl_img['image']=self.imagen_lamp
                    remain += 1
                    
                    # remain-1 es para que tome desde el index 0 que equivale al 1er char
                    # otra forma era tomar a remain inicial = -1 como defecto de argumento en esta fc
                    self.win.after(tiempo[codigo[remain-1]],self.espera,remain)
                else:
                    messagebox.showerror('Error',f'El caracter "{codigo[remain]}" no es un caracter morse válido.')
                    return self.win.destroy()
            # ya en este punto, remain supera len(codigo) y por eso reestablecemos los botones
            else:
                self.boton_comenzar.config(state=NORMAL)
                self.boton_parada.config(state=DISABLED)
                self.ejecutando = False
                self.lbl_img['image']=''
                return
    except:
        messagebox.showerror('Manipulador Morse','Ha ocurrido un error inesperado, revise su código morse y vuelva a intentarlo.')

               
if __name__ == '__main__':

    root=Tk()
    root.title('Manipulador Morse')
    barra_menu=Menu(root)
    root.config(menu=barra_menu)
    root.geometry('700x580+0+0')
    root.minsize(700,580)
    root.maxsize(900,720)
    app = Aplicacion(root)
    app.mainloop()


