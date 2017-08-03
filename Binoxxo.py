from tkinter import *
from random import randint
import tkinter.messagebox
from math import sqrt

# STATIC VARS
binoxxo_font = ("Comic Sans",10,"bold")
binoxxo_background_color = "black"
binoxxo_save_file = "save.bxo"
binoxxo_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# TEXTS
translations = {
    "title_main":"Binoxxo Solver",
    "title_creator":"Erzeuge Binoxxo",
    "title_creator_generated":"Generiertes Rätsel",
    "title_creator_solution":"Lösung",
    "title_loaded":"Geladenes Rätsel",
    "title_empty":"Leeres Rätsel",
    "button_creator_solution":"Zeige Lösung",
    "button_creator_save":"Speichern",
    "button_play":"Spiele ein Spiel (Generator)",
    "button_solver":"Löse ein Rätsel (Solver)",
    "entry_label_data":"Gib deinen alten Hash ein",
    "copyright":"(c) Matthias & Sven",
    "slider_size":"Grösse",
    "slider_amount":"Anzahl gesetzte",
    "messagebox_hash_title":"Dein Hash",
    "messagebox_hash_content1":"Dein Hash ist ",
    "messagebox_hash_content2":".\nBitte merke ihn gut.",
    "listbox_content1":"Hash",
    "listbox_content2":"mit der Zeit"
    }

# FUNCTIONS
def wechsler(data):
    """spiegle data an der diagonalen"""
    temp = [["" for j in range(len(data))] for i in range(len(data))]
    for x in range(len(data)):
        for y in range(len(data)):
            temp[x][y] = data[y][x]
    temp2 = []
    for i in temp:
        tempstr=""
        for j in i:
            tempstr+=j
        temp2.append(tempstr)
    return temp2
def sichere(data, cont=True, old=None):
    """mache die sicheren züge"""
    temp_data = []
    for i in data:
        i = i.replace(" xx","oxx")
        i = i.replace("xx ","xxo")
        i = i.replace("oo ","oox")
        i = i.replace(" oo","xoo")
        i = i.replace("x x","xox")
        i = i.replace("o o","oxo")
        if(i.count("x")==len(data)/2):
            i = i.replace(" ","o")
        if(i.count("o")==len(data)/2):
            i = i.replace(" ","x")
        temp_data.append(i)
    if cont:
        #wechsle temp_data und mache nochmals die sicheren
        temp_data = wechsler(temp_data)
        return sichere(temp_data,False, temp_data)
    if(old!=None):
        if(temp_data==old):
            return wechsler(temp_data)
        else:
            temp_data=wechsler(temp_data)
            return sichere(temp_data,True,temp_data)
def istVoll(data):
    """hat es noch leere Felder?"""
    voll=True
    for i in data:
        if " " in i:
            voll = False
            break
    return voll
def guess(data):
    """mache einen Zufallsguess"""
    pos = (0,0,"")
    for x in range(len(data)):
        for y in range(len(data)):
            if data[x][y]==" ":
                #leeres Feld gefunden, probiere x
                data[x] = data[x][:y]+"x"+data[x][y+1:]
                data2 = sichere(data)
                if hatFehler(data2):
                    #sehr gut... pos auf o setzen
                    data[x] = data[x][:y]+"o"+data[x][y+1:]
                    return sichere(data)
                else:
                    if istVoll(data2):
                        pos = (x,y,"x")
                    #schlecht. pos auf o und sichere, dann fehler suchen
                    data[x] = data[x][:y]+"o"+data[x][y+1:]
                    data2 = sichere(data)
                    if hatFehler(data2):
                        #pos auf x
                        data[x] = data[x][:y]+"x"+data[x][y+1:]
                        return sichere(data)
                    else:
                        if istVoll("data2"):
                            pos = (x,y,"o")
                        #ganz schlecht. pos auf leer und nächste pos
                        data[x] = data[x][:y]+" "+data[x][y+1:]
    if pos[2]!="":
        data[pos[0]] = data[pos[0]][:pos[1]]+pos[2]+data[pos[0]][pos[1]+1:]
        return sichere(data)
    return False
def hatFehler(data):
    """hat es einen Fehler in data?"""
    for x in data:
        if "xxx" in x or "ooo" in x:
            return True
        if x.count("x")>(len(x)/2) or x.count("o")>(len(x)/2):
            return True
        if data.count(x)>1:
            return True
    data = wechsler(data)
    for x in data:
        if "xxx" in x or "ooo" in x:
            return True
        if x.count("x")>(len(x)/2) or x.count("o")>(len(x)/2):
            return True
        if data.count(x)>1:
            return True
    return False
def printBinoxxo(data):
    """gib das Binoxxo im Main-Frame aus"""
    siz = len(data)
    for x in range(siz):
        for y in range(siz):
            if(data[x][y]!=" "):
                label_liste[x*siz+y].configure(text=data[x][y])
def solveIt(data):
    """löse das Binoxxo,return:solved"""
    data2 = sichere(data)
    fehler = False
    data3 = []
    while True:
        for i in data2:
            if " " in i:
                data3 = guess(data2)
                break
        if data3==[] or data3 == False:
            break
        else:
            data2 = data3
            data3 = []
    if hatFehler(data2):
        return data
    else:
        return data2

def showSol(data):
    """Zeige die Lösung"""
    t2 = Toplevel(master,background=binoxxo_background_color)
    t2.title(translations["title_creator_solution"])
    for x in range(len(data)):
        for y in range(len(data)):
            Label(t2,text=data[x][y],height=2,width=5,font=binoxxo_font).grid(row=x,column=y,padx=1,pady=1)
    
def printGenBinoxxo(data,buttons):
    """zeige das generierte Binoxxo"""
    siz = len(data)
    for x in range(siz):
        for y in range(siz):
            if data[x][y] != " ":
                buttons[x*siz+y].configure(text=data[x][y],state="disabled")
            else:
                buttons[x*siz+y].configure(text=data[x][y])
def changeText(event):
    """Wechsle die Button-beschriftungen"""
    b = event.widget
    if b.cget("state") == "disabled":
        return
    text = b.cget("text")
    if text==" ":
        b.configure(text="x")
    elif text=="x":
        b.configure(text="o")
    else:
        b.configure(text=" ")
    
def generate():
    """Generiere das Rätsel"""
    top = Toplevel(master,background=binoxxo_background_color)
    top.title(translations["title_creator_generated"])
    buttons = []
    for x in range(slide1.get()):
        for y in range(slide1.get()):
            b=Button(top, text="", height=2, width=5, font=binoxxo_font)
            b.bind('<Button-1>',func=changeText)
            b.grid(row=x,column=y, padx=1,pady=1)
            buttons.append(b)
    
    data = []
    for i in range(slide1.get()):
        temp = []
        for j in range(slide1.get()):
            temp.append(" ")
        data.append(temp)

    # setze Punkt. Mache Sichere. Kein Fehler-> nächster Punkt. Fehler->anderer Ort
    for i in range(slide2.get()):
        #so viele Punkte müssen gesetzt werden
        while True:
            laenge = randint(0,slide1.get()-1)
            spalte = randint(0,slide1.get()-1)
            if data[laenge][spalte]==" ":
                data[laenge][spalte]="xo"[randint(0,1)]
                break
        data5 = []
        for i in data:
            tempstr = ""
            for j in i:
                tempstr+=j
            data5.append(tempstr)
        data2 = sichere(data5)
        counter = 0
        while hatFehler(data2) and counter<100:
            #setze punkt neu, bis kein fehler mehr
            data[laenge][spalte]=" "
            while True:
                laenge = randint(0,slide1.get()-1)
                spalte = randint(0,slide1.get()-1)
                if data[laenge][spalte]==" ":
                    data[laenge][spalte]="xo"[randint(0,1)]
                    break
            data5 = []
            for i in data:
                tempstr = ""
                for j in i:
                    tempstr+=j
                data5.append(tempstr)
            data2 = sichere(data5)
            counter+=1
        #next point
    #output data5
    #do things like main form
    data6 = sichere(data5)
    fehler = False
    dat3 = []
    while True:
        for i in data6:
            if " " in i:
                dat3 = guess(data6)
                break
        if dat3==[] or dat3 == False:
            break
        else:
            data6 = dat3
            dat3 = []
    
    if(hatFehler(data6)):
        #falls es einen Fehler drin hat, mache ein neues!
        top.destroy()
        generate()
    else:
        b = Button(top, text=translations["button_creator_solution"])
        b.configure(command=lambda:showSol(data6))
        b.grid(row=x+1,columnspan=int((x+1)/2),column=0)
        b2 = Button(top, text=translations["button_creator_save"])
        b2.configure(command=lambda:writeHash(buttons))
        b2.grid(row=x+1,columnspan=int((x+1)/2),column=int((x+1)/2-1))
        printGenBinoxxo(data5,buttons)
def ListBoxSelected(l,top):
    sel = l.curselection()
    if sel==():
        return
    else:
        sel = sel[0]
        data = l.get(sel,sel)[0]
        e.delete(0,len(e.get()))
        e.insert(0,data.split("\"")[1])
        top.destroy()
        ButtonSolve()
def ButtonSolve():
    """check if hash, löse das vom hash, sonst öffne ein eingegebenes"""
    top = Toplevel(master,background=binoxxo_background_color)
    top.title(translations["title_loaded"])
    if e.get()!="":
        #löse vom hash
        if readHash(e.get())==None:
            #Räsel nicht gefunden.
            #Zeige listbox mit allen einträgen
            all_ = readHash("")
            l = Listbox(top, font=binoxxo_font,height=10,width=50)
            l.bind("<Button-1>",lambda x:ListBoxSelected(l,top))
            for i in range(len(all_)):
                l.insert(i,translations["listbox_content1"]+": "+all_[i][1]+" "+translations["listbox_content2"]+": \""+all_[i][0]+"\"")
            l.pack()
            return
            
        original,data = readHash(e.get())
        buttons = []
        for x in range(len(data)):
            for y in range(len(data)):
                b=Button(top, text="", height=2, width=5, font=binoxxo_font)
                b.bind('<Button-1>',func=changeText)
                b.grid(row=x,column=y, padx=1,pady=1)
                buttons.append(b)
        
        printGenBinoxxo(data,buttons)
        for x in range(len(data)):
            for y in range(len(data)):
                if data[x][y] != " ":
                    buttons[x*len(data)+y].configure(state="normal")
                if original[x][y] != " ":
                    buttons[x*len(data)+y].configure(state="disabled")
        empty = True
        for i in original:
            for j in i:
                if j!=" ":
                    empty = False
        if empty:
            b2 = Button(top, text=translations["button_creator_save"])
            b2.configure(command=lambda:writeHash(buttons))
            b2.grid(row=x+1,columnspan=x)
            return
        b = Button(top, text=translations["button_creator_solution"])
        b.configure(command=lambda:showSol(solveIt(original)))
        b.grid(row=x+1,column=0,columnspan=int(x/2))
        b2 = Button(top, text=translations["button_creator_save"])
        b2.configure(command=lambda:writeHash(buttons))
        b2.grid(row=x+1,column=int(x/2),columnspan=int(x/2))
    else:
        #direkt-eingabe
        top.title(translations["title_empty"])
        buttons = []
        siz = slide1.get()
        for x in range(siz):
            for y in range(siz):
                b=Button(top, text=" ", height=2, width=5, font=binoxxo_font)
                b.bind('<Button-1>',func=changeText)
                b.grid(row=x,column=y, padx=1,pady=1)
                buttons.append(b)
        b = Button(top, text=translations["button_creator_solution"])
        b.configure(command=lambda:showSol(solveIt(ButToData(buttons))))
        b.grid(row=x+1,column=0,columnspan=int(x/2))
        b2 = Button(top, text=translations["button_creator_save"])
        b2.configure(command=lambda:writeHash(buttons))
        b2.grid(row=x+1,column=int(x/2),columnspan=int(x/2))
def ButToData(buttons):
    """generate data from buttons"""
    siz = int(sqrt(len(buttons)))
    out = []
    for x in range(siz):
        tempstr = ""
        for y in range(siz):
            tempstr+=buttons[x*siz+y].cget("text")
        out.append(tempstr)
    return out
def writeHash(buttons):
    """write data to file, return hash"""
    hash_ = ""
    for i in range(4):
        hash_+=chars[randint(0,len(binoxxo_chars)-1)]
    while readHash(hash_)!=None:
        hash_ = ""
        for i in range(4):
            hash_+=chars[randint(0,len(binoxxo_chars)-1)]
    original = []
    data = []
    siz = int(sqrt(len(buttons)))
    for x in range(siz):
        original.append("")
        data.append("")
        for y in range(siz):
            data[x]+=buttons[x*siz+y].cget("text")
            if buttons[x*siz+y].cget("state") == "disabled":
                original[x]+=buttons[x*siz+y].cget("text")
            else:
                original[x]+=" "
    with open(binoxxo_save_file,"a") as writefile:
        writefile.write(hash_+";"+time.strftime("%d.%m.%Y %H:%M;")+str(original)+";"+str(data)+"\n")
    tkinter.messagebox.showinfo(translations["messagebox_hash_title"],translations["messagebox_hash_content1"]+hash_+translations["messagebox_hash_content2"])
    
def readHash(hash_):
    """read all saved ones, if there, return original, data; else return None"""
    try:
        f = open(binoxxo_save_file)
    except:
        f = open(binoxxo_save_file,mode="x")
    data = f.read()
    f.close()
    data = data.split("\n")
    #format:
    #hash; time; original; data
    out = None
    if hash_=="":
        out = []
        for i in data[:-1]:
            j = i.split(";")
            out.append([j[0],j[1]])
        return out
    for i in data:
        if i[:4]==hash_:
            out = i
            break
    if out==None:
        return None
    out = out.split(";")
    return (eval(out[2]),eval(out[3]))
# STARTUP
master = Tk()
master.title(translations["title_main"])
f = Frame(master,background=binoxxo_background_color)
starter = [" x  ox o","        ","BINOXXO-"," SOLVER ","        "," o xx o ","  x o xo","oox  xx "]
label_liste = []
for x in range(8):
    for y in range(8): 
        l = Label(f, text=starter[x][y], height=2, width=5, font=binoxxo_font)
        if x==2 or x==3:
            l.configure(background="yellow")
        l.grid(row=x,column=y, padx=1,pady=1)
        label_liste.append(l)

f2 = Frame(master)
f3 = Frame(master)

b = Button(f2, text=translations["button_play"], height=2, width=30, command=generate)
b2 = Button(f2, text=translations["button_solver"],height=2,width=30, command=ButtonSolve)
e = Entry(f2)
l = Label(f2,text=translations["entry_label_data"])

slide1 = Scale(f3, from_=2, to=14, resolution=2, label=translations["slider_size"],orient="horizontal",command=(lambda x: slide2.configure(to=slide1.get()**2)))
slide1.set(6)
slide2 = Scale(f3, from_=1, to=(slide1.get())**2, resolution=1, label=translations["slider_amount"],orient="horizontal")
slide2.set(10)
    
f.grid(row=0,columnspan=3)
f2.grid(row=1,column=0,columnspan=2)
f3.grid(row=1,column=2)
b.pack()
b2.pack()
l.pack()
e.pack()
slide1.pack()
slide2.pack()
Label(master,text=translations["copyright"]).grid(row=2,column=0,columnspan=3)
master.mainloop()
