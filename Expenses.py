from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty,StringProperty,ListProperty
import sqlite3
from datetime import date
from email.message import EmailMessage
from kivymd.uix.picker import MDDatePicker
import datetime
from kivymd.uix.snackbar import Snackbar
import json
import threading


class Expenses(Screen):

    exp_rv=ObjectProperty()
    all_rv=ObjectProperty() # rv de la TOATE
    search_exp_remove_rv=ObjectProperty()
    search_exp_rv=ObjectProperty()
    markup=True
    val=StringProperty('Stuff')
    first_exp=ObjectProperty()
    last_exp=ObjectProperty()
    category=StringProperty('')
    temp_exp_edit=0

    def __init__(self,**kwargs):
        super(Expenses, self).__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def add_data(self,val1,val2):
        self.show_remaining_cash()
        self.add_to_toate()
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("SELECT rowid,* FROM exp_table ORDER BY "+val1+' '+val2)
        self.exp_rv.data=[]
        for i in cur.fetchall():
            split_date=i[1].split('-')
            final_date=split_date[2]+'-'+split_date[1]+'-'+split_date[0]
            dates="[b]{}[/b] - {}".format(i[0],final_date) # index number - date
            rest="[b][color=#fb8500]{}[/color][/b] - {}".format(i[2],i[3])
            cat="{}".format(i[4])
            self.exp_rv.data.append({'text': dates, 'secondary_text': rest, 'tertiary_text':cat})
        conn.commit()
        conn.close()
        present_date=date.today()
        self.ids.id_exp_day.text=str(present_date.day)
        self.ids.id_exp_month.text=str(present_date.month)
        self.ids.id_exp_year.text=str(present_date.year)

    def add_to_toate(self):
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        alin=cur.execute("SELECT rowid,* FROM exp_table ORDER BY dt DESC")

        lucrari=[]

        toate={}
        for i in alin.fetchall():
            a=i[1][:7]
            toate[a]=0
            lucrari.append(i)

        for i in lucrari:
            toate[i[1][:7]]+=i[2]

        self.all_rv.data=[]
        for i in toate.items():
            a="{:.2f}".format(float(i[1]))
            j=i[0][-2:]
            if j=='01':
                j=self.data['january']
            if j=='02':
                j=self.data['february']
            if j=='03':
                j=self.data['march']
            if j=='04':
                j=self.data['april']
            if j=='05':
                j=self.data['may']
            if j=='06':
                j=self.data['june']
            if j=='07':
                j=self.data['july']
            if j=='08':
                j=self.data['august']
            if j=='09':
                j=self.data['september']
            if j=='10':
                j=self.data['october']
            if j=='11':
                j=self.data['november']
            if j=='12':
                j=self.data['december']
            txt=j+' '+str(i[0][:4])+' '+': '+'[b][color=#fb8500]{}[/color][/b]'.format(a)
            self.all_rv.data.append({'text': txt})
        conn.commit()
        conn.close()

    def check_active(self,val,checkbox,value):
        self.val=val
        if value:
            return self.val

    # from button Add in expenses
    def get_date(self,day,month,year,cash,product):
        try:
            datetime.date(int(year),int(month),int(day))
        except ValueError:
            Snackbar(text=self.data['addjobs_invalid_date']).open()
            return
        if cash=='' or product=='':
            Snackbar(text=self.data['expenses_fillTheFields']).open()
            return
        dt=datetime.date(int(year),int(month),int(day))
        cash=float(cash)
        product=str(product).capitalize()
        category=self.val

        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("INSERT INTO exp_table VALUES (:dt, :amount, :product, :category)",
            {
            'dt': dt,
            'amount': cash,
            'product': product,
            'category': category
            })
        conn.commit()

        cur.execute("SELECT rowid,* FROM exp_table")
        first_last=cur.fetchall()
        self.first_exp=first_last[0][0]
        self.last_exp=first_last[-1][0]
        conn.commit()

        self.ids.id_cash.text=''
        self.ids.id_product.text=''
        self.add_data('dt','desc')
        conn.close()
        self.remainingCash(cash)

    
    # CALENDAR FROM-TO
    def show_all(self):
        self.ids.total_spent.text=''
        self.ids.total_earned.text=''
        var1=str(self.ids.exp_from_day.text)
        var2=str(self.ids.exp_from_month.text)
        var3=str(self.ids.exp_from_year.text)
        var4=str(self.ids.exp_to_day.text)
        var5=str(self.ids.exp_to_month.text)
        var6=str(self.ids.exp_to_year.text)

        try:
            datetime.date(int(var3),int(var2),int(var1))
        except ValueError:
            self.ids.total_spent.text=self.data['expenses_invalidFromDate']
            self.ids.exp_from_day.text=''
            self.ids.exp_from_month.text=''
            self.ids.exp_from_year.text=''
            return
            
        try:
            datetime.date(int(var6),int(var5),int(var4))
        except ValueError:
            self.ids.total_earned.text=self.data['expenses_invalidToDate']
            self.ids.exp_to_day.text=''
            self.ids.exp_to_month.text=''
            self.ids.exp_to_year.text=''
            return

        if var1=='' or var2=='' or var3=='' or var4=='' or var5=='' or var6=='':
            return

        a=datetime.date(int(var3),int(var2),int(var1))
        print('A:',a)
        b=datetime.date(int(var6),int(var5),int(var4))
        print('B:',b)
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("SELECT amount,product FROM exp_table WHERE dt>=? and dt<=?",(a,b))
        tot=cur.fetchall()
        total=0
        for i in tot:
            total+=i[0]
        total="{:.2f}".format(total)
        print('Total: ',total)
        self.ids.total_spent.text=str(total)
        cur.execute("SELECT amount FROM jobs_table WHERE dt>=? and dt<=?",(a,b))
        tot1=cur.fetchall()
        
        total1=0
        for i in tot1:
            total1+=i[0]
        total1="{:.2f}".format(total1)
        self.ids.total_earned.text=str(total1)

    

    def exp_search(self,*args):
        conn = sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute('SELECT rowid,* FROM exp_table')
        searched=str(args[0]).lower()
        result=cur.fetchall()
        if searched=='':
            self.search_exp_rv.data=[]
            return
        else:
            if searched: 
                self.search_exp_rv.data=[]
                for i in range(len(result)):
                    for j in result[i]:
                        j=str(j).lower()
                        if searched in j:
                            good_date=result[i][1].split('-')
                            rev_date=good_date[2]+'-'+good_date[1]+'-'+good_date[0]
                            txt="[b]{}[/b] {} [b][color=#fb8500]{}[/color][/b] {}".format(result[i][0],rev_date,result[i][2],result[i][3])
                            self.search_exp_rv.data.append({'text': txt})

    def remove_exp(self,rem):
        if rem=='' or int(rem)<self.first_exp or int(rem)>self.last_exp:
            Snackbar(text=self.data['expenses_nothingToRemove']).open()
            self.ids.exp_search_field_remove.text=''
            return
        self.remaining_cash_remove_exp(rem)
        rem=int(rem)
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute('DELETE FROM exp_table WHERE rowid=' + str(rem))
        conn.commit()
        Snackbar(text="{} {}".format(self.data['expenses_removedIDNo'],str(rem))).open()
        # Snackbar(text="Removed id no: {}".format(str(rem))).open()
        self.ids.exp_search_field_remove.text=''
        self.ids.exp_search_field.text=''
        self.add_data('dt','desc')

        cur.execute("SELECT rowid,* FROM exp_table")
        first_last=cur.fetchall()
        self.first_exp=first_last[0][0]
        self.last_exp=first_last[-1][0]
        conn.close()

    

    def save_edited_jobs(self,*args):
        conn = sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        a=str(args[0]) # day
        b=str(args[1]) # month
        c=str(args[2]) # year
        d=str(args[3]) # amount
        e=args[4] # product

        try:
            datetime.date(int(c),int(b),int(a))
        except ValueError:
            self.ids.edit_day_exp.text=''
            self.ids.edit_month_exp.text=''
            self.ids.edit_year_exp.text=''
            Snackbar(text=self.data['addjobs_invalid_date']).open()
            return

        if a=='' or b=='' or c=='' or d=='' or e=='':
            self.ids.save_button_edit_exp.disabled=True
            Snackbar(text=self.data['addjobs_couldNotSave']).open()
            return
        else:
            cat=self.val # category
            full_date=str(datetime.date(int(c),int(b),int(a))) # full_date
            cur.execute('''UPDATE exp_table SET
            dt = ?,
            amount = ?,
            product = ?,
            category = ?
            WHERE rowid=?''',(full_date,d,e,cat,str(self.index),))
            conn.commit()
            conn.close()
            
            Snackbar(text='{} {}'.format(self.data['expenses_changesSaved'],self.index)).open()
            # Snackbar(text='Changes saved for job no {}'.format(self.index)).open()
            self.ids.edit_label_exp.text="{} {}".format(self.data['lastSaved'],str(self.index))
            self.remaining_cash_after_edit_exp()
            if str(self.ids.exp_nr_to_edit.text)==str(self.last_exp):
                self.ids.exp_nr_to_edit.text=self.ids.exp_nr_to_edit.text
            else:
                self.ids.exp_nr_to_edit.text=str(int(self.ids.exp_nr_to_edit.text)+1)
            self.add_data('dt','desc')

    def add_to_fields_exp(self):
        self.ids.save_button_edit_exp.disabled=True
        self.conn = sqlite3.connect('jobs_db.db')
        self.cur=self.conn.cursor()
        self.cur.execute("SELECT rowid,* FROM exp_table")
        exp_list_1=self.cur.fetchall()
        if exp_list_1==[]:
            return

        self.first_exp=exp_list_1[0][0]
        self.last_exp=exp_list_1[-1][0]
        arg=self.ids.exp_nr_to_edit.text
        if arg=='' or arg=='-':
            self.clear_fields()
            return
        self.cur.execute("SELECT rowid,* FROM exp_table WHERE rowid IN ({})".format(int(arg)))
        exp_list_2=self.cur.fetchall()
        if exp_list_2==[]:
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=True
            self.clear_fields()
            return
        if arg:
            self.index=exp_list_2[0][0]
            dt=exp_list_2[0][1].split('-')
            year=int(dt[0])
            month=int(dt[1])
            day=int(dt[2])
            amount=float(exp_list_2[0][2])
            product=exp_list_2[0][3]
            self.category=exp_list_2[0][4]
            if arg in [str(exp_list_2[i][0]) for i in range(len(exp_list_2))]:
                self.arrows_exp()
                self.ids.save_button_edit_exp.disabled=False
                self.ids.edit_index_exp.text=str(self.index)
                self.ids.edit_day_exp.text=str(day)
                self.ids.edit_month_exp.text=str(month)
                self.ids.edit_year_exp.text=str(year)
                self.ids.edit_amount_exp.text=str(amount)
                self.ids.edit_product_exp.text=product
                self.ids.edit_category_exp.text=self.category
                self.temp_exp_edit=float(self.ids.edit_amount_exp.text)
            else:
                self.clear_fields()

    def arrows_exp(self):
        conn = sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("SELECT * FROM exp_table")
        exp_list_1=cur.fetchall()
        if exp_list_1==[]:
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=True
            return
        if self.ids.exp_nr_to_edit.text=='':
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=True
            return
        if int(self.ids.exp_nr_to_edit.text)==self.first_exp:
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=False
            return
        if int(self.ids.exp_nr_to_edit.text)==self.last_exp:
            self.ids.button_arrow_right_exp.disabled=True
            self.ids.button_arrow_left_exp.disabled=False
            return
        if int(self.ids.exp_nr_to_edit.text)<self.first_exp:
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=True
            return
        if int(self.ids.exp_nr_to_edit.text)>self.last_exp:
            self.ids.button_arrow_left_exp.disabled=True
            self.ids.button_arrow_right_exp.disabled=True
            return
        if self.first_exp<int(self.ids.exp_nr_to_edit.text)<self.last_exp:
            self.ids.button_arrow_left_exp.disabled=False
            self.ids.button_arrow_right_exp.disabled=False
            return

    def clear_fields(self):
        self.ids.edit_index_exp.text=''
        self.ids.edit_day_exp.text=''
        self.ids.edit_month_exp.text=''
        self.ids.edit_year_exp.text=''
        self.ids.edit_amount_exp.text=''
        self.ids.edit_product_exp.text=''
        self.ids.edit_category_exp.text=''
        self.ids.save_button_edit_exp.disabled=True
        self.arrows_exp()



    
    def get_date_first(self, date):
        self.ids.exp_from_day.text=str(date.day)
        self.ids.exp_from_month.text=str(date.month)
        self.ids.exp_from_year.text=str(date.year)
    
    def show_date_picker_first(self):
        self.ids.exp_from_day.text=''
        self.ids.exp_from_month.text=''
        self.ids.exp_from_year.text=''

        td=date.today()
        year=td.year
        date_dialog=MDDatePicker(callback=self.get_date_first,year=year,month=1,day=1)
        date_dialog.open()

    def get_date_last(self, date):
        self.ids.exp_to_day.text=str(date.day)
        self.ids.exp_to_month.text=str(date.month)
        self.ids.exp_to_year.text=str(date.year)

    def show_date_picker_last(self):
        self.ids.exp_to_day.text=''
        self.ids.exp_to_month.text=''
        self.ids.exp_to_year.text=''
        date_dialog=MDDatePicker(callback=self.get_date_last)
        date_dialog.open()

    # only show remaining cash in below label
    def show_remaining_cash(self):
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']
        self.ids.id_remaining_cash.text=self.data['remaining_cash']+"{:.2f}".format(float(remaining_home))+' lei'

    # modify remaining cash after something is added to list of expenses (from def get_date())
    def remainingCash(self,arg1):
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']

        rest=float(remaining_home)-float(arg1)
        self.ids.id_remaining_cash.text=self.data['remaining_cash']+"{:.2f}".format(float(rest))+' lei'

        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)

    def remaining_cash_remove_exp(self,recash):
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute('SELECT amount FROM exp_table WHERE rowid=' + str(recash))
        cash=cur.fetchall()[0][0]

        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']
        rest=float(remaining_home)+float(cash)

        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)
        conn.commit()
        conn.close()

    def remaining_cash_after_edit_exp(self):
        if self.ids.edit_amount_exp.text=='' or float(self.ids.edit_amount_exp.text)==float(self.temp_exp_edit):
            return
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']

        if float(self.ids.edit_amount_exp.text)>float(self.temp_exp_edit):
            rest=float(remaining_home) - (float(self.ids.edit_amount_exp.text)-float(self.temp_exp_edit))
        elif float(self.ids.edit_amount_exp.text)<float(self.temp_exp_edit):
            rest=float(remaining_home) + (float(self.temp_exp_edit) - float(self.ids.edit_amount_exp.text))

        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)

        self.temp_exp_edit=0

    def separate(self,sp):
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        alin=cur.execute("SELECT rowid,* FROM exp_table ORDER BY dt DESC")

        lucrari=[]

        toate={}

        if sp=='year':
            for i in alin.fetchall():
                a=i[1][:4]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1][:4]]+=float(i[2])

            self.all_rv.data=[]
            for i in toate.items():
                a="{:.2f}".format(float(i[1]))
                txt=str(i[0])+' '+': '+'[b][color=#fb8500]{}[/color][/b]'.format(a)
                self.all_rv.data.append({'text': txt})

        elif sp=='month':
            for i in alin.fetchall():
                a=i[1][:7]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1][:7]]+=float(i[2])

            self.all_rv.data=[]
            for i in toate.items():
                a="{:.2f}".format(float(i[1]))
                j=i[0][-2:]
                if j=='01':
                    j=self.data['january']
                if j=='02':
                    j=self.data['february']
                if j=='03':
                    j=self.data['march']
                if j=='04':
                    j=self.data['april']
                if j=='05':
                    j=self.data['may']
                if j=='06':
                    j=self.data['june']
                if j=='07':
                    j=self.data['july']
                if j=='08':
                    j=self.data['august']
                if j=='09':
                    j=self.data['september']
                if j=='10':
                    j=self.data['october']
                if j=='11':
                    j=self.data['november']
                if j=='12':
                    j=self.data['december']
                txt=j+' '+str(i[0][:4])+' '+': '+'[b][color=#fb8500]{}[/color][/b]'.format(a)
                self.all_rv.data.append({'text': txt})
        elif sp=='day':
            for i in alin.fetchall():
                a=i[1]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1]]+=float(i[2])

            self.all_rv.data=[]
            for i in toate.items():
                a="{:.2f}".format(float(i[1]))
                j=i[0][5:7]
                if j=='01':
                    j=self.data['january']
                if j=='02':
                    j=self.data['february']
                if j=='03':
                    j=self.data['march']
                if j=='04':
                    j=self.data['april']
                if j=='05':
                    j=self.data['may']
                if j=='06':
                    j=self.data['june']
                if j=='07':
                    j=self.data['july']
                if j=='08':
                    j=self.data['august']
                if j=='09':
                    j=self.data['september']
                if j=='10':
                    j=self.data['october']
                if j=='11':
                    j=self.data['november']
                if j=='12':
                    j=self.data['december']
                txt=str(int(i[0][-2:]))+' '+j+' '+i[0][:4]+': [b][color=#fb8500]{}[/color][/b]'.format(a)
                self.all_rv.data.append({'text': txt})

        conn.commit()
        conn.close()
