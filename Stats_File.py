from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
import sqlite3
import datetime
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDTimePicker,MDDatePicker
from datetime import date
import json


class Stats(Screen):
    money_rv=ObjectProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def get_date_first(self, date):
        self.ids.first_day.text=str(date.day)
        self.ids.first_month.text=str(date.month)
        self.ids.first_year.text=str(date.year)
    
    def show_date_picker_first(self):
        self.ids.first_day.text=''
        self.ids.first_month.text=''
        self.ids.first_year.text=''

        td=date.today()
        year=td.year
        date_dialog=MDDatePicker(callback=self.get_date_first,year=year,month=1,day=1)
        date_dialog.open()

    def get_date_last(self, date):
        self.ids.last_day.text=str(date.day)
        self.ids.last_month.text=str(date.month)
        self.ids.last_year.text=str(date.year)

    def show_date_picker_last(self):
        self.ids.last_day.text=''
        self.ids.last_month.text=''
        self.ids.last_year.text=''
        date_dialog=MDDatePicker(callback=self.get_date_last)
        date_dialog.open()

    def total(self):
        var1=str(self.ids.first_day.text)
        var2=str(self.ids.first_month.text)
        var3=str(self.ids.first_year.text)

        var4=str(self.ids.last_day.text)
        var5=str(self.ids.last_month.text)
        var6=str(self.ids.last_year.text)

        if var1=='' or var2=='' or var3=='' or var4=='' or var5=='' or var6=='':
            return

        try:
            datetime.date(int(var3),int(var2),int(var1))
        except ValueError:
            self.ids.first_day.text=''
            self.ids.first_month.text=''
            self.ids.first_year.text=''
            Snackbar(text=self.data['statspage_invalidStartDate']).open()
            return
            
        try:
            datetime.date(int(var6),int(var5),int(var4))
        except ValueError:
            self.ids.last_day.text=''
            self.ids.last_month.text=''
            self.ids.last_year.text=''
            Snackbar(text=self.data['statspage_invalidEndDate']).open()
            return

        a=datetime.date(int(var3),int(var2),int(var1))
        b=datetime.date(int(var6),int(var5),int(var4))

        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("SELECT * FROM jobs_table WHERE dt>=? and dt<=?",(a,b))
        tot=cur.fetchall()

        moc=0
        for i in tot:
            abc=i[2]
            moc=moc+abc

        self.ids.id_label_date.text=str(moc)
        self.ids.first_day.text=''
        self.ids.first_month.text=''
        self.ids.first_year.text=''
        self.ids.last_day.text=''
        self.ids.last_month.text=''
        self.ids.last_year.text=''

    # cele 3 butoane de arata pe an/luna/zi
    def separate(self, sp):
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        alin=cur.execute("SELECT rowid,* FROM jobs_table ORDER BY dt DESC")

        lucrari=[]

        toate={}

        if sp=='year':
            for i in alin.fetchall():
                a=i[1][:4]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1][:4]]+=i[3]

            self.money_rv.data=[]
            for i in toate.items():
                txt=str(i[0][:4])+' '+': '+'[b][color=#fb8500]{}[/color][/b]'.format(i[1])
                self.money_rv.data.append({'text': txt})

        elif sp=='month':
            for i in alin.fetchall():
                a=i[1][:7]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1][:7]]+=i[3]

            self.money_rv.data=[]
            for i in toate.items():
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
                txt=j+' '+str(i[0][:4])+' '+': '+'[b][color=#fb8500]{}[/color][/b]'.format(i[1])
                self.money_rv.data.append({'text': txt})
        elif sp=='day':
            for i in alin.fetchall():
                a=i[1]
                toate[a]=0
                lucrari.append(i)

            for i in lucrari:
                toate[i[1]]+=i[3]

            self.money_rv.data=[]
            for i in toate.items():
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
                txt=str(int(i[0][-2:]))+' '+j+' '+i[0][:4]+': [b][color=#fb8500]{}[/color][/b]'.format(i[1])
                self.money_rv.data.append({'text': txt})


        