import os
from abc import ABC,abstractmethod
from kivy.app import App
from kivy.uix.button import ButtonBehavior,Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
import time
d = time.ctime().split(' ')
class Account:
    def __init__(self,balance,acc_type,id):
        Account.balance=balance
        Account.acc_type=acc_type
        Account.id=id
    @staticmethod
    # this method replaces value of balance in details file when user performs any transaction
    # and updates it.
    def work():
        with open(f'{(Account.acc_type).upper()}\\details','r+') as f:
            main=[]
            for lines in f:
                m=lines.strip().split(',')
                main.append(m)
            for i in main:
                if Account.id==i[1]:
                    i[2]=Account.balance
            with open(f'{(Account.acc_type).upper()}\\details','w+') as f:

                for i in main:
                    f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')
    def hide_label(self,l1):
                l1.opacity=0
    ##this method checks the account type update customer_info and details files with user entry
    #make object of that account and set details in its file ,created with convention (user_id)

    def set(self, object):
        # will create and add account holder details in file
        with open(f'{(Account.acc_type).upper()}\\{object.id}', 'a+') as f:
            l = object.info()
            for i in l:
                f.write(str(i) + str(l.get(i)))

    def Account(self,object):

        if object.acc_type == 'CHECKING ACCOUNT':
                with open(f'CHECKING ACCOUNT\\details', 'a+') as f:

                    f.write(Customer.name +','+str(self.id)+','+str(self.balance)+ '\n')

                self.set(object)

        elif object.acc_type == 'LOAN ACCOUNT':

                with open(f'LOAN ACCOUNT\\details', 'a+') as f:
                    f.write(Customer.name+','+str(self.id) + ','+str(self.balance)+'\n')

                self.set(object)
        elif object.acc_type == 'SAVING ACCOUNT':

                with open(f'SAVING ACCOUNT\\details', 'a+') as f:
                    f.write(Customer.name + ','+str(self.id)+','+str(self.balance)+'\n')

                 # this will set info in file made for this account holder
                self.set(object)

    @abstractmethod
    def deposit(self,amount):
        pass


    #this is withdraw method called when user withdraws
    def withdraw(self,amount):
        #checks if withdraw amount is not greater then balance for loan and saving account
        if (self.acc_type == 'saving account') and int(amount) > Account.balance:
            l1 = Label(text='U dont have that much balance!!!', size_hint=(0.3, 0.3), pos_hint={'x': 0.35, 'y': 0.1},
                   font_size=30, color='red')
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
            return(l1)
       #put check on if user asks for more amount then creditlimit
        elif self.acc_type=='checking account' and Account.balance <= -50000:
           l1 = Label(text='U have reached the credit limit!!!', size_hint=(0.3, 0.3), pos_hint={'x': 0.35, 'y': 0.1},
               font_size=30, color='red')
           Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
           return(l1)
        else:

          Account.balance-=int(amount)

        # opens file in folder then enter withdraw amount as record
          with open(f'{(self.acc_type).upper()}\\{self.id}', 'a+') as f:
            s = f'Withdraw:{amount}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
            f.write(s +'\n')
            f.write('Current balance: ' + str(Account.balance)+'\n\n')
          Account.work()

          return 'ok'

    #this method will read file of user_id then prints its transaction
    def balance_enquiry(self):
        l = []
        c = ''
        with open(f'{(self.acc_type).upper()}\\{self.id}','r') as f:
            for lines in f:
                l.append(lines)
            for i in range(0, 9):
                l.pop(0)
        for i in l:
            c += str(i)
        return (c)
class Checking_account(Account):
    def __init__(self,cl=-250000):
        self.creditlimit=cl
        #it will charge some amount as overdraft fees
    def overdraft(self,amount):
        overdraft_fees=10000
        Account.balance=-overdraft_fees

        with open(f'CHECKING ACCOUNT\\{self.id}','a+') as f:
            s = f'Overdraft fees :{overdraft_fees}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
            f.write(s + '\n')
            f.write('Current balance: ' + str(self.balance) + '\n\n')
        Account.work()
        self.withdraw(amount)
    def deposit(self,amount):
        if  self.balance < 0:
            Checking_account.overdraft(self, amount)
        self.dept = int(amount)
        Account.balance += self.dept

        # opens file in folder then add deposited amount of user in his file
        with open(f'{(self.acc_type).upper()}\\{self.id}', 'a+') as f:
            s = f'deposit:{self.dept}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
            f.write(s + '\n')
            f.write('Current balance: ' + str(Account.balance) + '\n\n')
        Account.work()



class Save_account(Account):
    def __init__(self,int_rate=2.5):
        self.interest_rate=int_rate
    def credit_balance(self):
        i=self.interest_rate*1*self.balance

        Account.balance+=i
        # enters credit amount as record
        with open(f'{(self.acc_type).upper()}\\{self.id}','a+') as f:
           s=f'Credit amount:{i}  {str(d[2])+" "+str(d[1])+" "+str(d[4])+" "+str(d[3])}'
           f.write(s+'\n')
           f.write('Current balance: '+str(Account.balance)+'\n\n')
        Account.work()
    def deposit(self,amount):
        self.dept = int(amount)
        Account.balance += self.dept

        # opens file in folder then add deposited amount of user in his file
        with open(f'{(self.acc_type).upper()}\\{self.id}', 'a+') as f:
            s = f'deposit:{self.dept}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
            f.write(s + '\n')
            f.write('Current balance: ' + str(Account.balance) + '\n\n')
        Account.work()
class Loan_account(Account):
    def __init__(self,amount,prin_amt=250000,int_rate=2.5,loan_dur=1):
        self.principle_amount=prin_amt
        self.interest_rate=int_rate
        self.loan_duration=loan_dur
        self.loan=amount
        Loan_account.t=[0,0]
    @staticmethod
    def read_loan():
#this method checks if user had taken loan before or not
        with open(f'LOAN ACCOUNT\\Loan-{Account.id}','r+') as f:
             l = []
             for lines in f:
                 m = lines.strip().split(' ')
                 l.append(m)

             if l[-1][-1].isdigit():

                return (l[-1][-1],True)

             else:
                return (0,False)

    def deposit(self,amount):
       #this checks if there had been taken loan and not paid for 1 month
            m=[]
            with open(f'LOAN ACCOUNT\\{self.id}','r+') as f:
                for lines in f:
                    m.append(lines.strip().split(' '))
                if m[-1][-1].isdigit():
                        t=[]
                        t.append(m[-2][-3])
                        t.append(m[-2][-4])
                        Loan_account.self_call_loan(self,t)

            self.dept=int(amount)
            Account.balance+=self.dept

        #opens file in folder then add deposited amount of user in his file
            with open(f'{(self.acc_type).upper()}\\{self.id}','a+') as f:
               s=f'deposit:{self.dept}  {str(d[2])+" "+str(d[1])+" "+str(d[4])+" "+str(d[3])}'
               f.write(s+'\n')
               f.write('Current balance: '+str(Account.balance)+'\n\n')
            Account.work()

    def apply_loan(self):
        if os.path.isfile(f'LOAN ACCOUNT\\Loan-{Account.id}'):
            with open(f'LOAN ACCOUNT\\Loan-{self.id}', 'a+') as f:
                s = f'Loan taken : {self.loan}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
                f.write(s + '\n')

                m=Loan_account.read_loan()
                if m[-1]:
                    self.loan=int(self.loan)
                    a=int(m[0])
                    self.loan+= a
                    f.write('Total loan: ' + str(self.loan)+'\n')
                else:
                    f.write('Total loan: ' + str(self.loan)+'\n')
        else:
            with open(f'LOAN ACCOUNT\\Loan-{self.id}', 'a+') as f:
                s = f'Loan taken : {self.loan}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
                f.write(s + '\n')
                f.write('Total loan: ' + str(self.loan)+'\n')
    def self_call_loan(self,t):
                if t[0]>=d[2] and t[0]!=d[1]:
                   m=self.read_loan()
                   if m[-1]:
                     n = int(float(self.loan) * self.interest_rate / 12)
                     Account.balance-=n
                     self.loan_receving(n)
                     t[0]=d[2]
                     t[1]=d[1]
                     with open(f'LOAN ACCOUNT\\Loan-{self.id}', 'a+') as f:
                         s = f'Loan receving : {n}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
                         f.write(s + '\n')
                     Account.work()

    def loan_receving(self):
        m=Loan_account.read_loan()

        if m[-1]:
            #

            with open(f'LOAN ACCOUNT\\Loan-{self.id}','a+') as f:
              s = f'Loan receving : {self.loan}  {str(d[2]) + " " + str(d[1]) + " " + str(d[4]) + " " + str(d[3])}'
              f.write(s+'\n')
              b=int(m[0])-int(self.loan)
              if b >0:
                  f.write('Total Loan: '+str(b)+'\n')
              else:
                  c=abs(b)
                  self.deposit(c)
                  f.write('Total Loan:  -'+'\n')

              Account.work()
        else:
            return False
    def set_principle_amount(self,n):
        self.principle_amount=n



class FirstWindow(Screen):
    acc=ObjectProperty(None)
    passw=ObjectProperty(None)
    nameee=ObjectProperty(None)
    def hide_label(self,l1):
                l1.opacity=0
    def pressed(self):


        main=[]
        with open('Customer_info', 'r+') as f:
            for lines in f:
                m = lines.strip().split(',')
                main.append(m)

        n = {}
        for i in main:
            n.update({i[0]:i[1]})
            # so that if u two people have same passwords it will add id before password
            n.update({str(i[0])+str(i[1]):i[2]})


        if self.nameee.text =='shahzad' and self.passw.text == '123' and self.acc.text=='admin':
                 self.manager.current='n14'
                 self.nameee.text=''
                 self.acc.text=''
                 self.passw.text=''
        elif self.nameee.text in n  and n.get(self.nameee.text)==self.passw.text and n.get(self.nameee.text+self.passw.text)==self.acc.text:


            a=(self.acc.text).upper()
            if a=='LOAN ACCOUNT':
                self.manager.current='thirdtime'
            elif a =='SAVING ACCOUNT':
                self.manager.current ='fourtime'
                with open(f'{(self.acc.text).upper()}\\{self.nameee.text}','r') as f:
                    m=[]
                    for lines in f:
                        n=lines.strip().split(' ')
                        m.append(n)
                    a=m[-3][-4]

                    if a=='1' :

                      Save_account.credit_balance(self)
            elif a == 'CHECKING ACCOUNT':
                self.manager.current='sixtime'



            main = []
            dic = {}
            with open(f'{(self.acc.text).upper()}\\details', 'r+') as f:
                for lines in f:
                    m = lines.strip().split(',')
                    main.append(m)
            for i in main:
                dic.update({i[1]: i[2]})

            balance = int(dic.get(self.nameee.text))
            q=Account(balance,self.acc.text,self.nameee.text)
            self.nameee.text=''
            self.acc.text=''
            self.passw.text=''
        else:
            l1=Label(text='Invalid data entered!!',size_hint=(1.01,0.2),pos_hint={'x_center':0.1,'y_bottom':1},font_size=30,color='red')
            self.add_widget(l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)


class SecondWindow(Screen):
    idd = ObjectProperty(None)
    namee = ObjectProperty(None)
    fathername = ObjectProperty(None)
    conc = ObjectProperty(None)
    email = ObjectProperty(None)
    dob = ObjectProperty(None)
    acc_type = ObjectProperty(None)
    dep = ObjectProperty(None)
    password = ObjectProperty(None)
    def get_account(self, textInput:TextInput):
        acc_type= textInput.text
        ThirdWindow.account_type(self,acc_type)
    def hide_label(self,l1):
                l1.opacity=0
        
    def clear(self):
        self.idd.text=''
        self.namee.text=''
        self.fathername.text=''
        self.conc.text=''
        self.email.text=''
        self.dob.text=''
        self.acc_type.text=''
        self.dep.text=''
        self.password.text=''

    def create_cust(self):

        # chexk whether all entries are filled if not this label occurs
          if self.namee.text!=''and self.idd.text!=''and self.fathername.text!=''and self.conc.text!=''\
                and self.email.text!=''and self.dob.text!=''and self.password.text!=''and \
                self.acc_type.text!=''and self.dep.text!='':
                try:

                  c1=Customer(self.namee.text,self.idd.text,self.fathername.text,self.conc.text
                    ,self.email.text,self.dob.text,self.password.text, self.acc_type.text,int(self.dep.text))
                  main=[]

                  #after check main file customerinfo file is read and check wheather this doesnot
                  #contains same id ,id ==unique key
                  with open('Customer_info','r+') as f:
                    for lines in f:
                          m=lines.strip().split(',')   #strip removes \n from end and start

                          main.append(m)

                  n=[]
                  for i in main:
                      n.append(i[0])

                  #in list m element is also list check first elemnet(idd) not same then allow to make customer else label
                  if self.idd.text not in n:
                          #check then create customer
                          c1.add_account()

                          with open('Customer_info','a+') as f:# write customer info in list to customerinfo file
                              l=[self.idd.text,self.password.text,self.acc_type.text]
                              f.write(str(l[0])+','+str(l[1])+','+str(l[2])+'\n')
                          self.clear()
                          self.manager.current='onetime'
                  else:
                          l1=Label(text='User with this ID exists!!!',size_hint=(1,0.3),width=170,height=30,font_size=30,color=(0,0,1,1))
                          SecondWindow.add_widget(self,l1)
                          Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
                except ValueError:
                    l1 = Label(text='Kindly enter correct value for deposit!!', size_hint=(1, 0.5), width=170, height=70,
                               font_size=30,
                               color=(0, 0, 1, 1))
                    self.add_widget(l1)
                    Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
          else:

            l1=Label(text='Kindly fill all enteries!!',size_hint=(1,0.3),width=170,height=30,font_size=30,color=(0,0,1,1))
            SecondWindow.add_widget(self,l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)

class Customer:
    def __init__(self,name,id,fa_name,ph_no,email,dob,passw,acctype,dep_amt):
        Customer.name=name
        self.id=id
        self.father_name=fa_name
        self.ph_no=ph_no
        self.email=email
        self.dob=dob
        self.passw=passw
        self.acc_type=acctype.upper()
        self.dept_amt=dep_amt


    def info(self):
        self.q=Account(self.dept_amt,self.acc_type,self.id)
        self.q.balance=self.dept_amt

        l={ 'Name: ': self.name,'\nPassword: ':self.passw, '\nAccount type: ': self.acc_type ,'\nID: ': self.id, '\nFather name: ': self.father_name \
              , '\nPhone number: ': self.ph_no,  '\nEmail: ': self.email \
              , '\nDate of birth: ': self.dob, '\nBalance: ': self.q.balance,\
            '\nCreated On : ':str(d[2])+' '+str(d[1])+' '+str(d[4])+'  '+str(d[3])+'\n'}
        return l

    def add_account(self):

      a1=Account(self.dept_amt,self.acc_type,self.id)
      a1.Account(self)
      
    @staticmethod
    def remove():
        #this method opens detail file of any accoynt and remove that particular person
        m=[]
        with open(f'{(Account.acc_type).upper()}\\details','r+') as f:
            for lines in f:
                n = lines.strip().split(',')
                m.append(n)

            for i in m:

                if str(Account.id) == i[1]:
                    m.pop(m.index(i))
                    m.pop(0)

        with open(f'{(Account.acc_type).upper()}\\details', 'w') as f:
            f.write('Name,ID,Balance\n')
            for i in m:
                f.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n')
        with open('Customer_info','r+') as f:
            m=[]
            for lines in f:
                n=lines.strip().split(',')
                m.append(n)
            for i in m:
                if i[0]== Account.id:
                    m.pop(m.index(i))
                    m.pop(0)
        with open('Customer_info','w') as f:
            f.write('ID,Password,Account'+'\n')
            for i in m:
                f.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n')



    def remove_account(self,):
        if Account.acc_type=='loan account':
            Customer.remove()
            os.remove(f'LOAN ACCOUNT\\{Account.id}')
            if os.path.exists(f'LOAN ACCOUNT\\Loan-{Account.id}'):
                os.remove(f'LOAN ACCOUNT\\Loan-{Account.id}')

        else:
            Customer.remove()
            os.remove(f'{Account.acc_type}\\{Account.id}')

class ThirdWindow(Screen):
    pass
        
class FourthWindow(Screen):
    pass

class SixthWindow(Screen):
    pass
class SeventhWindow(Screen):
    deposit_amount=ObjectProperty(None)
    def hide_label(self,l1):
                l1.opacity=0
    def again_deposit(self,b1,l1):
        self.remove_widget(b1)
        self.remove_widget(l1)
        self.deposit_amount.text = ''

    def btn(self):
        if self.deposit_amount.text=='':
            l1=Label(text='Kindly enter amount!!',size_hint=(1,0.5),width=170,height=70,font_size=30,color=(0,0,1,1))
            self.add_widget(l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
        else:

            if Account.acc_type=='checking account':

              q=Checking_account()
            elif Account.acc_type=='loan account':

                q=Loan_account(Account.balance)
            else:
                q=Save_account()
            try:
                        a=int(self.deposit_amount.text)
                        q.deposit(a)
                        b1 = Button(text='Click me for deposit again', size_hint=(0.4, 0.1),
                                    pos_hint={'x': 0.3, 'y': 0.1}, background_color='black')
                        b1.bind(on_press=lambda instance: self.again_deposit(b1, l1))
                        self.add_widget(b1)
                        l1 = Label(text='Amount deposited successfully', size_hint=(1, 0.5), width=170, height=70,
                                   font_size=30
                                   , color=(0, 0, 1, 1))
                        self.deposit_amount.text = ''
                        self.add_widget(l1)

            except ValueError:

                    l1 = Label(text='Kindly enter correct value!!', size_hint=(1, 0.5), width=170, height=70, font_size=30,
                               color=(0, 0, 1, 1))
                    self.add_widget(l1)
                    Clock.schedule_once(lambda dt: self.hide_label(l1), 3)



    def change(self):
        if Account.acc_type=='saving account':
            self.manager.current='fourtime'
        elif Account.acc_type=='checking account':
            self.manager.current='sixtime'
        else:
            self.manager.current='thirdtime'

class EightWindow(Screen):
    withdraw=ObjectProperty(None)
    def hide_label(self,l1):
                l1.opacity=0
    def change(self):
        if Account.acc_type == 'saving account':
            self.manager.current = 'fourtime'
        elif Account.acc_type == 'checking account':
            self.manager.current = 'sixtime'
        else:
            self.manager.current = 'thirdtime'
    def again_withdraw(self,b1,l1):
        self.remove_widget(b1)
        self.remove_widget(l1)
        self.withdraw.text = ''
    def btn(self):
        if self.withdraw.text =='':
            l1=Label(text='Kindly enter amount!!!', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
            font_size=30)
            self.add_widget(l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)

        else:
          try:
            q = Checking_account()
            a=int(self.withdraw.text)
            wid=q.withdraw(a)
            if wid=='ok':

                 b1 = Button(text='Click me for Withdraw again', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
                         background_color='black')
                 b1.bind(on_press=lambda instance: self.again_withdraw(b1, l1))
                 self.add_widget(b1)
                 l1 = Label(text='Amount withdraw successfully', size_hint=(1, 0.5), width=170, height=70, font_size=30)
                 self.add_widget(l1)
                 self.withdraw.text=''
            else:
                self.add_widget(wid)
          except ValueError:
              l1 = Label(text='Kindly enter correct value!!', size_hint=(1, 0.5), width=170, height=70, font_size=30,
                         color=(0, 0, 1, 1))
              self.add_widget(l1)
              Clock.schedule_once(lambda dt: self.hide_label(l1), 3)



class NinethWindow(Screen):

    def change(self):
        self.l2.text=''

        if Account.acc_type == 'saving account':
            self.manager.current = 'fourtime'
        elif Account.acc_type == 'checking account':
            self.manager.current = 'sixtime'
        else:
            self.manager.current = 'thirdtime'
    def print_balance(self):
        q=Checking_account()
        c=q.balance_enquiry( )
        from kivy.metrics import dp

        self.l2 = Label(text=c, font_size=20, color='black', size_hint_y=None)
        self.l2.bind(texture_size=lambda instance, size: setattr(self.l2, 'height', size[1]))

        b1 = Button(text='BACK', background_color=(1, 1, 0, 1), size_hint=(None, None), pos_hint=(None, None),
                    size=(100, 70))
        b1.bind(on_press=lambda instance: self.change())

        scroll = ScrollView(bar_color='black', size=(Window.width, Window.height))
        layoutt = GridLayout(cols=1, size_hint_y=None)
        layoutt.padding = dp(35)
        layoutt.spacing = dp(10)
        layoutt.bind(minimum_height=layoutt.setter('height'))
        layoutt.add_widget(b1)
        layoutt.add_widget(self.l2)
        scroll.add_widget(layoutt)

        self.add_widget(scroll)



class TenthWindow(Screen):
          pass
class EleventhWindow(Screen):
    loan_amount = ObjectProperty(None)
    def hide_label(self,l1):
                l1.opacity=0

    def again_loan(self, b1, l1):
        self.remove_widget(b1)
        self.remove_widget(l1)
        self.loan_amount.text = ''
    def btn(self):
        if self.loan_amount.text == '':
            l1=Label(text='Kindly enter amount!!', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
                    background_color='black')
            self.add_widget(l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
        else:
          try:
            amount=int(self.loan_amount.text)
            c1=Loan_account(amount)

            Loan_account.apply_loan(c1)
            b1 = Button(text='Click me for Loan again', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
                    background_color='black')
            b1.bind(on_press=lambda instance: self.again_loan(b1, l1))
            self.add_widget(b1)
            l1 = Label(text='Loan successfully provided', size_hint=(1, 0.5), width=170, height=70, font_size=30
                   , color=(0, 0, 1, 1))
            self.add_widget(l1)
          except ValueError:
              l1 = Label(text='Kindly enter correct value!!', size_hint=(1, 0.5), width=170, height=70, font_size=30,
                         color=(0, 0, 1, 1))
              self.add_widget(l1)
              Clock.schedule_once(lambda dt: self.hide_label(l1), 3)


class TwelveWindow(Screen):
    def change(self):
        self.l1.text=''
        self.manager.current='thirdtime'
    def details(self):
        c=''
        with open(f'LOAN ACCOUNT\\Loan-{Account.id}')as f:
            for lines in f:
                c+=lines
            from kivy.metrics import dp

            self.l1 = Label(text=c, font_size=20, color='black', size_hint_y=None)
            self.l1.bind(texture_size=lambda instance, size: setattr(self.l1, 'height', size[1]))

            b1 = Button(text='BACK', background_color=(1, 1, 0, 1), size_hint=(None, None), pos_hint=(None, None),
                        size=(100, 70))
            b1.bind(on_press=lambda instance: self.change())

            scroll = ScrollView(bar_color='black', size=(Window.width, Window.height))
            layoutt = GridLayout(cols=1, size_hint_y=None)
            layoutt.padding = dp(35)
            layoutt.spacing = dp(10)
            layoutt.bind(minimum_height=layoutt.setter('height'))
            layoutt.add_widget(b1)
            layoutt.add_widget(self.l1)
            scroll.add_widget(layoutt)

            self.add_widget(scroll)
class ThirteenWindow(Screen):
  loan_amount = ObjectProperty(None)

  def hide_label(self, l1):
      l1.opacity = 0
  def again_loan(self, b1, l1):
        self.remove_widget(b1)
        self.remove_widget(l1)
        self.loan_amount.text = ''

  def btn(self):
    if self.loan_amount.text == '':
        l1 = Label(text='Kindly enter amount!!', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
                   background_color='black')
        self.add_widget(l1)
        Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
    else:
      try:
        amount = int(self.loan_amount.text)
        c1 = Loan_account(amount)
        c1.loan_receving()
        b1 = Button(text='Click me for Loan again', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1},
                    background_color='black')
        b1.bind(on_press=lambda instance: self.again_loan(b1, l1))
        self.add_widget(b1)
        l1 = Label(text='Amount successfully paid', size_hint=(1, 0.5), width=170, height=70, font_size=30
                   , color=(0, 0, 1, 1))
        self.add_widget(l1)
      except ValueError:
          l1 = Label(text='Kindly enter correct value!!', size_hint=(1, 0.5), width=170, height=70, font_size=30,
                     color=(0, 0, 1, 1))
          self.add_widget(l1)
          Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
class FourteenWindow(Screen):


    pass
class SixteenWindow(Screen):
    def change(self):
            self.manager.current = 'n14'
            self.l1.text=''
    def print_details(self):
        n=''
        with open("Customer_info",'r') as f:
            for lines in f:
                n+=lines
        from kivy.metrics import dp

        self.l1 = Label(text=n, font_size=20, color='black', size_hint_y=None)
        self.l1.bind(texture_size=lambda instance, size: setattr(self.l1, 'height', size[1]))

        b1 = Button(text='BACK', background_color=(1, 1, 0, 1), size_hint=(None, None), pos_hint=(None, None),
                    size=(100, 70))
        b1.bind(on_press=lambda instance: self.change())

        scroll = ScrollView(bar_color='black', size=(Window.width, Window.height))
        layoutt = GridLayout(cols=1, size_hint_y=None)
        layoutt.padding = dp(35)
        layoutt.spacing = dp(10)
        layoutt.bind(minimum_height=layoutt.setter('height'))
        layoutt.add_widget(b1)
        layoutt.add_widget(self.l1)
        scroll.add_widget(layoutt)

        self.add_widget(scroll)


class FifteenWindow(Screen):
    input=ObjectProperty()
    def channge(self):
        if Account.acc_type == 'saving account':
            self.manager.current = 'fourtime'
        elif Account.acc_type == 'checking account':
            self.manager.current = 'sixtime'
        else:
            self.manager.current = 'thirdtime'
    def remove(self):
        self.manager.current='onetime'
        Customer.remove_account(self)

    def value(self,a,b,x,y):
        l1 = TextInput(text='', size_hint=(0.35, 0.1), pos_hint={'x': x, 'y': y})
        self.add_widget(l1)
        b1 = Button(text='Done', size_hint=(0.2, 0.1), pos_hint={'x': 0.37, 'y': 0.25}, background_color='blue')
        b1.bind(on_press=lambda instance: self.submit(a, b, l1, b1, l1.text))
        self.add_widget(b1)
        print(self.name)


    @staticmethod
    def write(a,b,ns):
        m=[]
        with open(f'{(Account.acc_type).upper()}\\{Account.id}', 'r+') as f:
            for lines in f:
                n = lines.strip().split(' ')
                m.append(n)

            m[a][b] = ns
        with open(f'{(Account.acc_type).upper()}\\{Account.id}', 'w') as f:
            for i in m:
                for j in i:
                    f.write(str(j) + ' ')
                f.write('\n')
            f.write('\n')

    def change(self,instance):

      if  instance.name == 'namee':
           x=0.3
           y=0.75
           a=0
           b=1
           self.value(a,b,x,y)

      elif instance.name == 'idc':
          x = 0.3
          y = 0.9
          a=3
          b=1
          self.value(a, b, x, y)


      elif instance.name == 'email':
          x = 0.3
          y = 0.82
          a=6
          b=1
          self.value(a, b, x, y)
      elif instance.name == 'father_name':
          x = 0.3
          y = 0.62
          a=4
          b=2
          self.value(a, b, x, y)
      elif instance.name == 'number':
          x = 0.3
          y = 0.54
          a=5
          b=2
          self.value(a, b, x, y)
      elif instance.name == 'dob':
          x = 0.3
          y = 0.48
          a=7
          b=3
          self.value(a, b, x, y)
      else:
          x = 0.3
          y = 0.68
          a=1
          b=1
          self.value(a, b, x, y)



    def submit(self,a,b,l1,b1,n):
        FifteenWindow.write(a,b,n)
        if a == 3 and b==1:
            os.renames(f'{(Account.acc_type).upper()}\\{Account.id}',f'{(Account.acc_type).upper()}\\{n}')

            with open(f'Customer_info','r+') as f:
                m=[]
                for lines in f:
                    l=lines.strip().split(',')
                    m.append(l)
                for i in m:
                    if i[0]==Account.id:
                        i[0]=n
            with open('Customer_info','w')as f:
                for i in m:
                    f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')
            with open(f'{(Account.acc_type).upper()}\\details','r+') as f:
                a=[]
                for lines in f:
                    b=lines.strip().split(',')
                    a.append(b)
                for i in a:
                    if i[1]==Account.id:
                        i[1]=n
            with open(f'{(Account.acc_type).upper()}\\details','w') as f:
                for i in a:
                    f.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n')
            Account.id = n

        elif a == 1 and b==1:

            with open(f'Customer_info','r+') as f:
                m=[]
                for lines in f:
                    l=lines.strip().split(',')
                    m.append(l)
                for i in m:
                    if i[0]==Account.id:
                        i[1]=n
            with open('Customer_info','w')as f:
                for i in m:
                    f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')

        self.remove_widget(l1)
        self.remove_widget(b1)
class SeventeenWindow(Screen):
    nameee = ObjectProperty(None)
    acc = ObjectProperty(None)
    def hide_label(self,l1):
                l1.opacity=0

    def customer_details(self):
        SeventeenWindow.a = self.nameee.text
        SeventeenWindow.b = self.acc.text
        if self.a =='' or self.b == '':
            l1=Label(text="Kindly enter Enteries!!", size_hint=(1, 0.5), width=170, height=70, font_size=30
                   , color=(0, 0, 1, 1))
            self.add_widget(l1)
            Clock.schedule_once(lambda dt: self.hide_label(l1), 3)
        else:
            with open(f'Customer_info') as f:
                m=[]
                for lines in f:
                    n=lines.strip().split(',')
                    m.append(n)
                for i in m:
                    if self.a==i[0] and self.b ==i[2]:
                        self.manager.current='n18'
                        self.nameee.text=''
                        self.acc.text=''
                    else:
                        l1=Label(text='Invalid Details!!!',font_size=30,size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.2})
                        self.add_widget(l1)
                        Clock.schedule_once(lambda dt: self.hide_label(l1), 3)

class EighteenWindow(Screen):
    def details(self):
        l=SeventeenWindow()
        a=(l.b).upper()
        n = ''

        with open(f'{a}\\{l.a}', 'r') as f:
            for lines in f:
                n += lines
        from kivy.metrics import dp

        self.l2 = Label(text=n, font_size=20, color='black', size_hint_y=None)
        self.l2.bind(texture_size=lambda instance, size: setattr(self.l2, 'height', size[1]))

        b1 = Button(text='BACK', background_color=(1, 1, 0, 1), size_hint=(None, None), pos_hint=(None, None),
                    size=(100, 70))
        b1.bind(on_press=lambda instance: self.change())

        scroll = ScrollView(bar_color='black', size=(Window.width, Window.height))
        layoutt = GridLayout(cols=1, size_hint_y=None)
        layoutt.padding = dp(35)
        layoutt.spacing = dp(10)
        layoutt.bind(minimum_height=layoutt.setter('height'))
        layoutt.add_widget(b1)
        layoutt.add_widget(self.l2)
        scroll.add_widget(layoutt)

        self.add_widget(scroll)
    def change(self):
        self.manager.current='n14'
        self.l2.text=''

class WindowManager(ScreenManager):
   pass
class  my(App):
    def build(self):
        pass


if __name__ =='__main__':
    my().run()
