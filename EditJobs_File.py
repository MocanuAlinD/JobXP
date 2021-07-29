from kivy.properties import ObjectProperty
import sqlite3
import datetime
from kivymd.uix.snackbar import Snackbar
from kivy.uix.popup import Popup
import json



class EditJobs(Popup):
    nr_to_edit=ObjectProperty()
    edit_index=ObjectProperty()
    edit_date_day=ObjectProperty()
    edit_date_month=ObjectProperty()
    edit_date_year=ObjectProperty()
    edit_address=ObjectProperty()
    edit_city=ObjectProperty()
    edit_amount=ObjectProperty()
    edit_person=ObjectProperty()
    edit_upfront=ObjectProperty()
    last_saved=ObjectProperty('---')
    first=ObjectProperty()
    last=ObjectProperty()
    luc=ObjectProperty()
    remove_button=ObjectProperty()
    leng=ObjectProperty()
    temp_amount_edit=0

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def edit_jobs(self,*args):
        conn = sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        a=args[0] # index
        b=args[1] # year
        c=args[2] # month
        d=args[3] # day
        e=args[4] # city
        f=args[5] # amount
        g=args[6] # address
        h=args[7] # person
        i=args[8] # upfront
        if i=='':
            i=0
        try:
            datetime.date(int(b),int(c),int(d))
        except ValueError:
            self.edit_date_year.text=''
            self.edit_date_month.text=''
            self.edit_date_day.text=''
            return
        full_date=datetime.date(int(b),int(c),int(d))
        if a=='' or b=='' or c=='' or d=='' or e=='' or f=='' or g=='' or h=='':
            Snackbar(text=self.data['addjobs_couldNotSave']).open()
            return
        else:
            cur.execute('''
            UPDATE jobs_table SET
            rowid=:rowid,
            dt= :dt,
            city = :city,
            amount = :amount,
            address = :address,
            person = :person,
            upfront = :upfront
            WHERE rowid=:rowid''',
                    {
                        'rowid': a,
                        'dt': full_date,
                        'city': e,
                        'amount': f,
                        'address': g,
                        'person': h,
                        'upfront': i
                    })
            conn.commit()
            Snackbar(text='{} {}'.format(self.data['expenses_changesSaved'],a)).open()
            self.remaining_cash_after_edit()
            
            if str(self.nr_to_edit.text)==str(self.last):
                self.nr_to_edit.text=self.nr_to_edit.text
            else:
                self.nr_to_edit.text=str(int(self.nr_to_edit.text)+1)
            self.last_saved=a


    def add_to_fields(self):
        self.conn = sqlite3.connect('jobs_db.db')
        self.cur=self.conn.cursor()
        self.cur.execute("SELECT rowid,* FROM jobs_table")
        self.luc=self.cur.fetchall()
        if self.luc==[]:
            return
        self.first=self.luc[0][0]
        self.last=self.luc[-1][0]
        self.leng=len(self.luc)
        arg=self.nr_to_edit.text
        if arg=='':
            self.dis()
            return
        self.cur.execute("SELECT rowid,* FROM jobs_table WHERE rowid IN ({})".format(int(arg)))
        self.luc1=self.cur.fetchall()
        if arg:
            if arg in [str(self.luc1[i][0]) for i in range(len(self.luc1))]:
                self.arrows()
                dt_date=self.luc1[0][1].split('-')
                dt_year=int(dt_date[0])
                dt_month=int(dt_date[1])
                dt_day=int(dt_date[2])
                self.ids.remove_button.disabled=False
                self.ids.save_button_jobs.disabled=False
                self.edit_index.text=str(self.luc1[0][0])
                self.edit_date_year.text=str(dt_year)
                self.edit_date_month.text=str(dt_month)
                self.edit_date_day.text=str(dt_day)
                self.edit_city.text=self.luc1[0][2]
                self.edit_amount.text=str(self.luc1[0][3])
                self.edit_address.text=self.luc1[0][4]
                self.edit_person.text=self.luc1[0][5]
                self.temp_amount_edit=self.edit_amount.text
                if self.edit_upfront.text=='':
                    self.edit_upfront.text=str(0)
                else:
                    self.edit_upfront.text=str(self.luc1[0][6])
            else:
                self.dis()


    def dis(self):
        self.edit_index.text=''
        self.edit_date_day.text=''
        self.edit_date_month.text=''
        self.edit_date_year.text=''
        self.edit_city.text=''
        self.edit_amount.text=''
        self.edit_address.text=''
        self.edit_person.text=''
        self.edit_upfront.text=''
        self.ids.remove_button.disabled=True
        self.ids.save_button_jobs.disabled=True
        self.arrows()

    def arrows(self):
        if len(self.luc)==1:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if self.nr_to_edit.text=='':
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if int(self.nr_to_edit.text)==self.first:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=False
            return
        if int(self.nr_to_edit.text)==self.last:
            self.ids.button_arrow_right.disabled=True
            self.ids.button_arrow_left.disabled=False
            return
        if int(self.nr_to_edit.text)<self.first:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if int(self.nr_to_edit.text)>self.last:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if self.first<int(self.nr_to_edit.text)<self.last:
            self.ids.button_arrow_left.disabled=False
            self.ids.button_arrow_right.disabled=False
            return
        self.add_to_fields()


    def remove_jobs(self):
        self.remaining_cash_after_remove()
        conn =  sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        arg=self.nr_to_edit.text
        cur.execute('DELETE FROM jobs_table WHERE rowid = ' + arg)
        conn.commit()
        cur.execute("SELECT rowid,* FROM jobs_table")
        self.luc=cur.fetchall()
        if self.luc==[]:
            self.dis()
            return
        if int(arg)==self.first:
            self.nr_to_edit.text=str(int(arg)+1)
            return
        if int(arg)==self.last:
            self.nr_to_edit.text=str(int(arg)-1)
            return
        if int(self.nr_to_edit.text)==self.last:
            self.ids.button_arrow_right.disabled=True
            self.ids.button_arrow_left.disabled=False
            return
        if int(self.nr_to_edit.text)<self.first:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if int(self.nr_to_edit.text)>self.last:
            self.ids.button_arrow_left.disabled=True
            self.ids.button_arrow_right.disabled=True
            return
        if self.first<int(self.nr_to_edit.text)<self.last:
            self.ids.button_arrow_left.disabled=False
            self.ids.button_arrow_right.disabled=False
            self.nr_to_edit.text=str(int(arg)+1)
            return

    def remaining_cash_after_remove(self,*args):
        if self.edit_amount.text=='':
            return
        arg1=self.edit_amount.text
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']

        rest=float(remaining_home)-float(arg1)

        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)

    def remaining_cash_after_edit(self):
        if self.edit_amount.text=='' or float(self.edit_amount.text)==float(self.temp_amount_edit):
            return
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']

        if float(self.edit_amount.text)>float(self.temp_amount_edit):
            rest=float(remaining_home) + ( float(self.edit_amount.text) - float(self.temp_amount_edit))
        elif float(self.edit_amount.text)<float(self.temp_amount_edit):
            rest=float(remaining_home) - (float(self.temp_amount_edit) - float(self.edit_amount.text))


        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)

        self.temp_amount_edit=0