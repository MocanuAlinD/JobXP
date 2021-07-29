from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
import sqlite3
import smtplib
import csv
from kivymd.uix.snackbar import Snackbar
from email.message import EmailMessage
import json


class JobsPage(Screen):
    rv=ObjectProperty()
    tlb=ObjectProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def show_remaining_cash_jobs(self):
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']
        self.ids.id_remaining_cash_jobs.text='Cash: '+"{:.2f}".format(float(remaining_home))+' lei'

    def reverse_order(self,val):
        conn =  sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute("SELECT rowid,* FROM jobs_table ORDER BY dt {}".format(val))
        self.rv.data=[]
        for i in cur.fetchall():
            a=i[0]
            b=i[1]
            b1=b.split('-')
            b=b1[2]+'-'+b1[1]+'-'+b1[0]
            cc=i[2]
            if cc=='':
                cc='Unknown'

            d=i[3]
            e=i[4]
            f=i[5]
            g=i[6]

            unu="[b]{}[/b] - {} - {} - {}".format(a,b,cc,f)
            doi="[b]{}[/b] [b][color=#fb8500]{}[/color][/b] --- [b]{}[/b] {}".format(self.data['jobspage_taken'],d,self.data['jobspage_upfront'],g)
            trei="[b]{}[/b] {}".format(self.data['jobspage_address'],e)
            self.rv.data.append({'text':unu,'secondary_text':doi,'tertiary_text':trei})
        conn.commit()
        conn.close()
        self.show_remaining_cash_jobs()

    def change_screens(self, screen):
        self.manager.current=screen

    
