def convertir_a_morse(texto_ingresado):

    codigo_morse={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.',
    'F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-',
    'L':'.-..','M':'--','N':'-.','Ñ':'--.--','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-',
    'W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----',
    '2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...',
    '8':'---..','9':'----.','.':'.-.-.-',',':'--..--','/':'-..-.',' ':'  ','\n':'\n'}

    codigo_lis=[]
    codigo_str=''

    text=texto_ingresado.upper()

    for caracter in text:
        if caracter in codigo_morse:
            codigo_lis.append(codigo_morse[caracter])
        else:
            codigo_lis.append('#')
    
    for elemento in codigo_lis:
        codigo_str += (elemento+' ')
    return codigo_str

def velocidad(num_grupos):
    if num_grupos==1:
        tiempos = {'-':1000,'.':500,' ':1500,'espera':800} #miliseg
    elif num_grupos==2:
        tiempos = {'-':700,'.':300,' ':1000,'espera':500} 
    else:
        tiempos = {'-':300,'.':80,' ':600,'espera':200} 
    return tiempos
    
