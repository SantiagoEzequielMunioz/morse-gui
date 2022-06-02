codigo_morse={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.',
    'F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-',
    'L':'.-..','M':'--','N':'-.','Ñ':'--.--','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-',
    'W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----',
    '2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...',
    '8':'---..','9':'----.','.':'.-.-.-',',':'--..--','/':'-..-.',' ':'  ','\n':'\n'}

def convertir_a_morse(texto_ingresado):

    codigo_lis=[]
    codigo_str=''

    text=texto_ingresado.upper()

    # loop que crea una lista a partir de los values del dict (morse)
    for caracter in text:
        if caracter in codigo_morse:
            codigo_lis.append(codigo_morse[caracter])
        else:
            codigo_lis.append('#')  # caso de que ese caracter no exista en codigo_morse
    # loop para unir la lista en cadena
    for elemento in codigo_lis:
        # if para que haya un espacio entre caracteres morse, salvo en los espacios
        if elemento != ' ':
            codigo_str += (elemento+' ')
    return codigo_str

# funcion para determinar la velocidad que puede seleccionar el usuario
def velocidad(num_grupos):
    if num_grupos==1:
        tiempos = {'-':1000,'.':500,' ':1500,'espera':800} #miliseg
    elif num_grupos==2:
        tiempos = {'-':700,'.':300,' ':1000,'espera':500} 
    else:
        tiempos = {'-':300,'.':80,' ':600,'espera':200} 
    return tiempos

# este método es para limpiar el dict en 2 listas, que me van a servir para
# la visualizacion del codigo morse en otra ventana
def dict_to_list():
    
    klist=list(codigo_morse.keys()) #lo hago lista
    klist=klist[0:-2]   # acorto la lista y saco los espacios y cambio de linea del final del dict
    vlist=list(codigo_morse.values())
    vlist=vlist[0:-2]
    return(klist,vlist)
