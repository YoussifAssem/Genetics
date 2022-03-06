from re import X
from matplotlib.pyplot import text
from numpy import insert
import pandas as pd
from Models.User import User
from tkinter import Y, StringVar, Tk, Label, Button, Text, END, Toplevel, Label, Entry, messagebox
from PIL import ImageTk
from PIL import Image  
from tkinter.filedialog import askopenfile 
import hashlib
import sys  

def destroyScreens():
  root.destroy()


def chatScreen(Sender):
    viewScreen = Toplevel(root)
    viewScreen.title("Chatting")
    viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) 
    viewScreen.config(background='black')
    global message
    message = StringVar()
    Label(viewScreen,text='Please, Type Message Here \t' + Sender, font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=800)
    send = Text(viewScreen, height=25, width=40, bg='white', fg='black', font='Helvetica 18 bold')
    send.insert(END, '\tSender Messages')
    for i in  obj.getSenderMessages(Sender, sys.argv[1].replace(" ","")):
      send.insert(END, '\n' + i)
      send.tag_configure("tag_name", justify='center')
    send.tag_configure("tag_name", justify='center')
    send.config(state='disabled')
    send.place(x=50,y=40)
    receive = Text(viewScreen, height=25, width=40, bg='white', fg='black', font='Helvetica 18 bold')
    receive.insert(END, '\tReceiver Messages')
    for i in  obj.getReceiverMessages(sys.argv[1].replace(" ",""), Sender):
      receive.insert(END, '\n' + i)
     
    receive.tag_configure("tag_name", justify='center')
    receive.config(state='disabled')
    receive.place(x=1030,y=40)
   
    me = Text(viewScreen, height=100, width=80, bg='white', fg='black', font='Helvetica 18 bold')
    me.place(x=0, y=900)
    btn = Button(viewScreen, text= 'Send Message', command= lambda: runChat(Sender, me.get("1.0","end-1c"))
    ,background='darkred',fg='white')
    btn.config(padx=100, pady=30)
    btn.place(x= 1300, y=960)
   
def runChat(Sender, message):
  obj.sendMessage(sys.argv[1].replace(" ", ''), Sender, message)
  messagebox.showinfo('Done', 'Message Send Successfully')
     
btn_list = []
def onClick(idx):
    chatScreen(btn_list[idx].cget("text"))
     


def viewSendersScreen():
    viewScreen = Toplevel(root)
    viewScreen.title("Senders")
    viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) 
    viewScreen.config(background='black')
    x = 100
    btn = []
    for i in range(len(obj.getSenders())):
      btn = Button(viewScreen, text=obj.getSenders()[i], command = lambda idx = i: onClick(idx), background='darkred',fg='white')
      btn.config(padx=100, pady=30)
      btn.place(x= 500, y = x + 200)
      x += 100 
      btn_list.append(btn)
      
      
def saveResults():
  ID = nationalID.get()
  case = caseNumber.get()
  if(case == '' and ID == ''):
    messagebox.showerror('Error', 'Please, Enter the Requirements Data')
    return
  elif(ID == ''):
    messagebox.showerror('Error', 'Please, Enter the National ID of Father')
    return
  elif(case == ''):
    messagebox.showerror('Error', 'Please, Enter the Case Number')
    return
 
    
  if(len(ID) == 14 and caseNumber != ''):
    hashed_ID = hashlib.sha256(ID.encode('utf-8')).hexdigest()
    hashed_case = hashlib.sha256(case.encode('utf-8')).hexdigest()
    msg = messagebox.askquestion("Question ?!", "Are you sure?")
    if msg == 'yes':
      if(obj.saveResults(hashed_ID, obj.calculateProbability()[0], obj.calculateProbability()[1], hashed_case, sys.argv[1].replace(" ", ''))):
        messagebox.showerror('Error', 'This National ID OR case Number is already exist')
        return
      else:
       messagebox.showinfo('Done', 'Data Saved Successfully')
       return
    else:
      messagebox.showwarning('Warning', 'Data Is Not Saved')
      return 
  if(len(ID) != 14):
    messagebox.showerror('Error', 'Length of National ID is Not True')
     
def open_file():
   file = askopenfile(mode ='r', filetypes =[('Python Files', '*.csv')]) 
   if file is not None:
        data = pd.read_csv(file.name)
        obj.Test(data['father'], data['mother'], data['child2'], data['combine'], data['chromosome'])
        '''Similar Rs Numbers fit the rule'''
        rsSimilar = obj.getRsNumberSimilar()
        '''Father Rs Numbers that not Matched with the rule'''
        rsFather = obj.getRsNumberFather()
        '''Mothers Rs Numbers that not Matched with the rule'''
        rsMother = obj.getRsNumberMother() 

     
        '''Father Rs Numbers Fit the rule'''
        fatherSimilar =  obj.getFatherSimilar()
        '''Mother Rs Numbers Fit the rule'''
        motherSimilar = obj.getMotherSimilar()
        '''Child Similar with father and mother'''
        childSimilar = obj.getChildSimilar()

        '''Alleles of father not matched with child'''
        father = obj.getFatherNotSimilar()
        '''Alleles of Mother not matched with child'''
        mother = obj.getMotherNotSimilar()
        '''Alleles of Child not matched with Father'''
        chFather = obj.getChildNotSimilarWithFather()
        '''Alleles of Child not matched with Mother'''
        chMother = obj.getChildNotSimilarWithMother()
        '''Chromosomes that fit the rule with Father and child'''
        chroFather = obj.getChromosomesFitFather()
        '''Chromosomes that fit the rule with Mother and child'''
        chroMother = obj.getChromosomesFitMother()
        '''Chromosomes that not fit the rule between Father and child'''
        chroNotFather = obj.getChromosomesNotFitFather()
        '''Chromosomes that not fit the rule between Mother and child'''
        chroNotMother = obj.getChromosomesNotFitMother()
        
        rsSimilar = list(dict.fromkeys(rsSimilar))
        rsFather = list(dict.fromkeys(rsFather))
        rsMother = list(dict.fromkeys(rsMother))
        chroFather = list(dict.fromkeys(chroFather))
        chroMother = list(dict.fromkeys(chroMother))
        chroNotFather = list(dict.fromkeys(chroNotFather))
        chroNotMother = list(dict.fromkeys(chroNotMother))
      
       
        viewScreen = Toplevel(root)
        viewScreen.title("Report")
        viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) 
        viewScreen.config(background='black')
        global nationalID, caseNumber
        nationalID = StringVar()
        caseNumber = StringVar()
        Label(viewScreen,text='Please, Enter Father National ID', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=0)
        ID = Entry(viewScreen, textvariable=nationalID, width=50, borderwidth=20)
        ID.place(x=0, y=50)
        
        Label(viewScreen,text='Please, Enter Case Number', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=140)
        case = Entry(viewScreen, textvariable=caseNumber, width=50, borderwidth=20)
        case.place(x=0, y=200)
        
        btnSave = Button(viewScreen, text= 'Save Results', command = saveResults,  background='darkgreen',fg='white')
        btnSave.config(padx=100, pady=20)
        btnSave.place(x=0, y=300)
        
        T = Text(viewScreen, height=400, width=200, bg='white', fg='white', font='Helvetica 18 bold')
        T.tag_configure("tag_name", justify='center')
        T.tag_config('warningColor', foreground='red')
        T.tag_config('safeColor', foreground='green')
        T.tag_config('probColor', foreground='black')
       
        
        T.insert(END, "The Number of rsNumbers: {}".format(len(rsSimilar)+ len(rsFather)+len(rsMother)), 'warningColor')
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of Chromosomes fit the rule: {}".format(len(chroFather)+ len(chroMother)), 'safeColor')
        T.insert(END, "\nFather Chromosomes: {}".format(chroFather[0:5]), 'safeColor')
        T.insert(END, "\nMother Chromosomes: {}".format(chroMother[0:5]), 'safeColor')
        T.insert(END, "\n----------------------------------------")
        T.insert(END, "\nThe Number of  Chromosomes Not fit the rule: {}".format(len(chroNotFather)+ len(chroNotMother)), 'warningColor')
        T.insert(END, "\nFather Chromosomes: {}".format(chroNotFather[0:5]), 'warningColor')
        T.insert(END, "\nMother Chromosomes: {}".format(chroNotMother[0:5]), 'warningColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of rsNumbers fit the rule: {}".format(len(rsSimilar)), 'safeColor')
        T.insert(END, "\nRs Numbers: {}".format(rsSimilar[0:5]), 'safeColor')
        T.insert(END, "\nFather: {}".format(fatherSimilar[0:5]), 'safeColor')
        T.insert(END, "\nChild: {}".format(childSimilar[0:5]), 'safeColor')
        T.insert(END, "\nMother: {}".format(motherSimilar[0:5]), 'safeColor')
        
        T.insert(END, "\n----------------------------------------")
        T.insert(END, "\nThe Number of rsNumbers does not fit the rule child with father: {}".format(len(rsFather)), 'warningColor')
        T.insert(END, "\nDf rsNumber: {}".format(rsFather[0:5]), 'warningColor')
        T.insert(END, "\nDf Father: {}".format(father[0:5]), 'warningColor')
        T.insert(END, "\nDf Child: {}".format(chFather[0:5]), 'warningColor')
       
        T.insert(END, "\n----------------------------------------")
        T.insert(END, "\nThe Number of rsNumbers does not fit the rule child with mother: {}".format(len(rsMother)), 'warningColor')
        T.insert(END, "\nDf rsNumber: {}".format(rsMother[0:5]), 'warningColor')
        T.insert(END, "\nDf Mother: {}".format(mother[0:5]), 'warningColor')
        T.insert(END, "\nDf Child: {}".format(chMother[0:5]), 'warningColor')
        T.insert(END, "\n----------------------------------------")
        T.insert(END, "\nSo, The Probability this may be the Fathe: {}".format(obj.calculateProbability()[0]), 'probColor')
        T.insert(END, "\nSo, The Probability this may Not be the Father: {}".format(obj.calculateProbability()[1]), 'probColor')
        T.tag_add("tag_name", "1.0", "end")
        T.config(state='disabled')
        T.pack(pady=200, padx=500)
        
        
        #btnResults = Button(root, text= 'Finish Work',  command= destroyScreens, background='darkred',fg='white')
        #btnResults.config(padx=100, pady=20)
        #btnResults.place(x= 1500, y=760)

        print('The Number of rsNumbers', len(rsSimilar)+ len(rsFather)+len(rsMother)-4)
        print("\nThe Number of Chromosomes fit the rule: ", len(chroFather)+ len(chroMother))
        print("\nFather Chromosomes: ", chroFather[0:5])
        print("\nMother Chromosomes: ", chroMother[0:5])
        print("\n\nThe Number of  Chromosomes Not fit the rule: ", len(chroNotFather)+ len(chroNotMother))
        print("\nFather Chromosomes: ", chroNotFather[0:5])
        print("\nMother Chromosomes: ", chroNotMother[0:5])
        print('\n\nThe Number of rsNumbers fit the rule', len(rsSimilar))
        print('The Similar rsNumber', rsSimilar[0:5])  
        print('Father: ', fatherSimilar[0:5])
        print('Child', childSimilar[0:5])
        print('Mother', motherSimilar[0:5])
        print('\n\nDifference between Father and Child')
        print('The Number of rsNumbers does not fit the rule child with father', len(rsFather))
        print('Df rsNumber', rsFather[0:5])
        print('Df Father', father[0:5])
        print('Df Child', chFather[0:5])
        print('\n\nDifference between Mother and Child')
        print('The Number of rsNumbers does not fit the rule child with mother', len(rsMother))
        print('Df rsNumber', rsMother[0:5])
        print('Df Child', chMother[0:5])
        print('Df Mother', mother[0:5])
        '''Returns the probability this may be the father'''
        print("So, The Probability this may be the Father: ", obj.calculateProbability()[0])
        '''Returns the probability this may not be the father'''
        print("So, The Probability this may Not be the Father: ", obj.calculateProbability()[1])

if __name__ == "__main__":
  obj = User()
  root = Tk(className='Python Examples - Window Color')  
  root.title('paternityTest')
  root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
  root.config(bg='black')
  root.eval('tk::PlaceWindow . center')
  load = Image.open("Images/family-law.png")
  render = ImageTk.PhotoImage(load) 
  img = Label(image=render)
  img.image = render
  Label(text='Welcome In Genetics', bg='black', fg='white', font='Helvetica 20 bold').place(x=820, y=210)
  Label(text='Welcome ' + sys.argv[1].replace(" ", ''), bg='black', fg='white', font='Helvetica 20 bold').place(x=860, y=250)
  img.place(x=700, y=200)
  btn = Button(root, text= 'Browse',  command= lambda:open_file(), background='white',fg='black')
  btn.config(padx=100, pady=20)
  btn.place(x= 830, y=720)
  btnChat = Button(root, text= 'view Messages',  command= viewSendersScreen, background='white',fg='black')
  btnChat.config(padx=75, pady=20)
  btnChat.place(x= 830, y=820)
  btnDestroy = Button(root, text= 'Finish Work',  command= destroyScreens, background='darkred',fg='white')
  btnDestroy.config(padx=100, pady=30)
  btnDestroy.place(x= 1500, y=760)

  root.mainloop()  
  



    