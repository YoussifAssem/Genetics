
from unicodedata import name
import pandas as pd
from Models.User import User
from Models.relevance import Relevance
from Models.whole import wholeGenome
from tkinter import  StringVar, Tk, Label, Button, Text, END, Toplevel, Label, Entry,  messagebox
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
    global message
    message = StringVar()
    Label(viewScreen,text="Chat " + Sender, bg="darkblue", fg='white', width="300", height="2", font=("Calibri", 20, 'underline'), pady=50).pack()
    Label(viewScreen,text='Please, Type Message Here \t' + Sender, font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=850)
    send = Text(viewScreen, height=25, width=40, bg='white', fg='black', font='Helvetica 18 bold')
    send.tag_config('titleColor', foreground='red', font=("Calibri", 20, 'underline'))
 
    
    send.insert(END,  Sender + ' Messages\n', 'titleColor')
    for i in  obj.getSenderMessages(Sender, sys.argv[1].replace(" ","")):
      send.insert(END, '\n' + i)
      send.tag_configure("tag_name", justify='center')
    send.tag_configure("tag_name", justify='center')
    send.config(state='disabled')
    send.place(x=50,y=200)
    receive = Text(viewScreen, height=25, width=40, bg='white', fg='black', font='Helvetica 18 bold')
    receive.tag_config('titleColor', foreground='red', font=("Calibri", 20, 'underline'))
    receive.insert(END,  sys.argv[1].replace(' ', '') + ' Messages\n', 'titleColor')
    for i in  obj.getReceiverMessages(sys.argv[1].replace(" ",""), Sender):
      receive.insert(END, '\n' + i)
     
    receive.tag_configure("tag_name", justify='center')
    receive.config(state='disabled')
    receive.place(x=1030,y=200)
   
    me = Text(viewScreen, height=100, width=80, bg='white', fg='black', font='Helvetica 18 bold')
    me.place(x=0, y=900)
    btn = Button(viewScreen, text= 'Send Message', command= lambda: runChat(Sender, me.get("1.0","end-1c"))
    ,background='darkblue',fg='white')
    btn.config(padx=100, pady=30)
    btn.place(x= 1300, y=960)
   
def runChat(Sender, message):
  if(message == ''):
    messagebox.showerror('Error', 'Please Type Message Here To Send It')
    return
  else:  
    obj.sendMessage(sys.argv[1].replace(" ", ''), Sender, message)
    messagebox.showinfo('Done', 'Message Send Successfully')
     
btn_list = []
def onClick(idx):
    chatScreen(btn_list[idx].cget("text"))
     


def viewSendersScreen():
    viewScreen = Toplevel(root)
    viewScreen.title("Senders")
    viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) 
    x = 100
    btn = []
    Label(viewScreen,text="Messages", bg="darkblue", fg='white', width="300", height="2", font=("Calibri", 20, 'underline'), pady=50).pack()
    for i in range(len(obj.getSenders())):
      btn = Button(viewScreen, text=obj.getSenders()[i], command = lambda idx = i: onClick(idx), background='darkblue',fg='white')
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
   viewScreen = Toplevel(root)
   viewScreen.title("Report")
   viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
      
   if 'relevance' in file.name:
      relevance = Relevance(file.name)
      done = relevance.getDone()
      Label(viewScreen, text="Report Relevances", bg="darkblue", fg='white', width="300", height="2", font=("Calibri", 20, 'underline'), pady=50).pack()
      
      T = Text(viewScreen, height=400, width=200, bg='white', fg='black', font='Helvetica 18 bold')
      T.tag_configure("tag_name", justify='center')
      T.tag_config('related', foreground='Green')
      
      T.tag_config('warningColor', foreground='red')
        
      T.insert(END, '\n\n\n\nSimilar ID: {}'.format(done['similarID'][0:5]), 'related')
      T.insert(END, '\nNOT Similar ID: {}'.format(done['notSimilarID'][0:5]))
      T.insert(END, '\nNo of people Related to this Family: {}'.format(len(done['similarID'])), 'warningColor')
      T.insert(END, '\nNo of people is Not Related to this Family: {}'.format(len(done['notSimilarID'])), 'warningColor')
      T.insert(END, '\nProbability of relative: {}'.format(relevance.getProbability()), 'warningColor')
      T.tag_add("tag_name", "1.0", "end")
      T.config(state='disabled')
      T.pack(pady=200, padx=500)
      
   else:
        data = pd.read_csv(file.name)
        obj.Test(data['father'], data['mother'], data['child2'], data['combine'], data['chromosome'])
        report = obj.getPaternityResults()
        
        
        
   
        
        report['rsNumberSimilar'] = list(dict.fromkeys(report['rsNumberSimilar']))
        report['fatherNotSimilarRs'] = list(dict.fromkeys(report['fatherNotSimilarRs']))
        report['motherNotSimilarRs'] = list(dict.fromkeys(report['motherNotSimilarRs']))
        report['chromosomeFitFather'] = list(dict.fromkeys(report['chromosomeFitFather']))
        report['chromosomeFitMother'] = list(dict.fromkeys(report['chromosomeFitMother']))
        report['chromosomeNotFitFather'] = list(dict.fromkeys(report['chromosomeNotFitFather']))
        report['chromosomeNotFitMother'] = list(dict.fromkeys(report['chromosomeNotFitMother']))
      
       
        Label(viewScreen, text="Report Rs Numbers", bg="darkblue", fg='white', width="300", height="2", font=("Calibri", 20, 'underline'), pady=50).pack()
        global nationalID, caseNumber
        nationalID = StringVar()
        caseNumber = StringVar()
        Label(viewScreen,text='Please, Enter Father National ID', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=200)
        ID = Entry(viewScreen, textvariable=nationalID, width=50, borderwidth=20)
        ID.place(x=0, y=250)
        
        Label(viewScreen,text='Please, Enter Case Number', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=330)
        case = Entry(viewScreen, textvariable=caseNumber, width=50, borderwidth=20)
        case.place(x=0, y=380)
        
        btnSave = Button(viewScreen, text= 'Save Results', command = saveResults,  background='darkblue',fg='white')
        btnSave.config(padx=100, pady=20)
        btnSave.place(x=0, y=500)
        
        T = Text(viewScreen, height=400, width=200, bg='white', fg='white', font='Helvetica 18 bold')
        T.tag_configure("tag_name", justify='center')
        T.tag_config('warningColor', foreground='red')
        T.tag_config('safeColor', foreground='green')
        T.tag_config('probColor', foreground='black')
       
        
        T.insert(END, "The Number of rsNumbers: {}".format(len(report['rsNumberSimilar'])+ len(report['fatherNotSimilarRs'])+len(report['motherNotSimilarRs'])), 'warningColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of Chromosomes fit the rule: {}".format(len(report['chromosomeFitFather'])+ len(report['chromosomeFitMother'])), 'safeColor')
        T.insert(END, "\nFather Chromosomes: {}".format(report['chromosomeFitFather'][0:5]), 'safeColor')
        T.insert(END, "\nMother Chromosomes: {}".format(report['chromosomeFitMother'][0:5]), 'safeColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of  Chromosomes Not fit the rule: {}".format(len(report['chromosomeNotFitFather'])+ len(report['chromosomeNotFitMother'])), 'warningColor')
        T.insert(END, "\nFather Chromosomes: {}".format(report['chromosomeNotFitFather'][0:5]), 'warningColor')
        T.insert(END, "\nMother Chromosomes: {}".format(report['chromosomeNotFitMother'][0:5]), 'warningColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of rsNumbers fit the rule: {}".format(len(report['rsNumberSimilar'])), 'safeColor')
        T.insert(END, "\nRs Numbers: {}".format(report['rsNumberSimilar'][0:5]), 'safeColor')
        
        T.insert(END, "\nFather: {}".format(report['father'][0:5]), 'safeColor')
        T.insert(END, "\nChild: {}".format(report['child'][0:5]), 'safeColor')
        T.insert(END, "\nMother: {}".format(report['mother'][0:5]), 'safeColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of rsNumbers does not fit the rule child with father: {}".format(len(report['fatherNotSimilarRs'])), 'warningColor')
        T.insert(END, "\nDf rsNumber: {}".format(report['fatherNotSimilarRs'][0:5]), 'warningColor')
        T.insert(END, "\nDf Father: {}".format(report['notFather'][0:5]), 'warningColor')
        T.insert(END, "\nDf Child: {}".format(report['chFather'][0:5]), 'warningColor')
       
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nThe Number of rsNumbers does not fit the rule child with mother: {}".format(len(report['motherNotSimilarRs'])), 'warningColor')
        T.insert(END, "\nDf rsNumber: {}".format(report['motherNotSimilarRs'][0:5]), 'warningColor')
        T.insert(END, "\nDf Mother: {}".format(report['notMother'][0:5]), 'warningColor')
        T.insert(END, "\nDf Child: {}".format(report['chMother'][0:5]), 'warningColor')
        
        T.insert(END, "\n----------------------------------------")
        
        T.insert(END, "\nSo, The Probability this may be the father: {}".format(obj.calculateProbability()[0]), 'probColor')
        T.insert(END, "\nSo, The Probability this may Not be the father: {}".format(obj.calculateProbability()[1]), 'probColor')
        T.tag_add("tag_name", "1.0", "end")
        T.config(state='disabled')
        T.pack(pady=200, padx=500)
        
        
def viewWholeGenome(seq):
        viewScreen = Toplevel(root)
        viewScreen.title("Report")
        viewScreen.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) 
        Label(viewScreen, text="Report Whole Genome", bg="darkblue", fg='white', width="300", height="2", font=("Calibri", 20, 'underline'), pady=50).pack()
        global nationalID, caseNumber
        nationalID = StringVar()
        caseNumber = StringVar()
        Label(viewScreen,text='Please, Enter Father National ID', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=200)
        ID = Entry(viewScreen, textvariable=nationalID, width=50, borderwidth=20)
        ID.place(x=0, y=250)
        
        Label(viewScreen,text='Please, Enter Case Number', font=("Calibri", 17, 'underline'), fg='black').place(x=0, y=330)
        case = Entry(viewScreen, textvariable=caseNumber, width=50, borderwidth=20)
        case.place(x=0, y=380)
        
        btnSave = Button(viewScreen, text= 'Save Results', command = saveResults,  background='darkblue',fg='white')
        btnSave.config(padx=100, pady=20)
        btnSave.place(x=0, y=500)
        
        T = Text(viewScreen, height=100, width=600, bg='white', fg='black', font='Helvetica 18 bold')
        T.tag_configure("tag_name", justify='center')
        T.tag_config('titleColor', foreground='green')
        T.insert(END, seq, 'titleColor')
        T.tag_add("tag_name", "1.0", "end")
        T.config(state='disabled')
        T.pack(pady=200, padx=500)
        
def wholeGenome():
  file = askopenfile(mode ='r', filetypes =[('Python Files', '*.txt')])
  wG = wholeGenome()
  if file is not None:
    wG.selectedFile(file.name)
  doc = wG.getwholeGenome()
  wG.reInitialize()
  file2 = askopenfile(mode ='r', filetypes =[('Python Files', '*.txt')]) 
  if file2 is not None:
    wG.selectedFile(file2.name)
  viewWholeGenome(wG.getResults(doc))
if __name__ == "__main__":
  obj = User()
  root = Tk(className='Python Examples - Window Color')  
  root.title('paternityTest')
  root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
  root.eval('tk::PlaceWindow . center')
  load = Image.open("Images/family-law.png")
  render = ImageTk.PhotoImage(load) 
  img = Label(image=render)
  img.image = render
  Label(text='Welcome In Genetics', bg='darkblue', fg='white', font='Helvetica 20 bold').place(x=820, y=110)
  Label(text='Welcome ' + sys.argv[1].replace(" ", ''), bg='darkblue', fg='white', font='Helvetica 20 bold').place(x=860, y=150)
  img.place(x=700, y=100)
  btn = Button(root, text= 'Browse',  command= lambda:open_file(), background='darkblue',fg='white')
  btn.config(padx=100, pady=20)
  btn.place(x= 830, y=720)
  btnWG = Button(root, text= 'Upload Whole Genome',  command= lambda: wholeGenome(), background='darkblue',fg='white')
  btnWG.config(padx=50, pady=20)
  btnWG.place(x= 830, y=820)
  btnChat = Button(root, text= 'view Messages',  command= viewSendersScreen, background='darkblue',fg='white')
  btnChat.config(padx=75, pady=20)
  btnChat.place(x= 830, y=920)
  btnDestroy = Button(root, text= 'Finish Work',  command= destroyScreens, background='darkblue',fg='white')
  btnDestroy.config(padx=100, pady=30)
  btnDestroy.place(x= 1500, y=760)

  root.mainloop()  
  



    
