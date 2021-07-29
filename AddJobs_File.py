from kivy.uix.popup import Popup
import sqlite3
import datetime
from kivymd.uix.snackbar import Snackbar
import json
from kivy.properties import ObjectProperty, StringProperty
import time

class AddJobs(Popup):
    id_remaining_cash_jobs=ObjectProperty()
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)
    
    def write_to_lucrari(self, *args):
        '''Add new job to jobs list'''
        # date validation and 3 windows for date on the same row
        try:
            datetime.date(int(args[2]),int(args[1]),int(args[0]))
        except ValueError:
            Snackbar(text=self.data['addjobs_invalid_date']).open()
            return
        conn=sqlite3.connect("jobs_db.db")
        cur=conn.cursor()
        abc=int(args[0])
        abc1=int(args[1])
        abc2=int(args[2])
        a=datetime.date(abc2,abc1,abc)
        b=args[3]
        cc=args[4]
        d=args[5]
        e=args[6]
        f=args[7]
        if f=='':
            f=0
        if abc=='' or abc1=='' or abc2=='' or a == '' or b == '' or cc == '' or d == '' or e == '' or f == '':
            Snackbar(text=self.data['addjobs_couldNotSave'] ).open()
            return
        else:
            cur.execute("INSERT INTO jobs_table VALUES (:dt, :city, :amount, :address, :person, :upfront)",
                        {
                            'dt': a,
                            'city': b,
                            'amount': cc,
                            'address': d,
                            'person': e,
                            'upfront': f
                        })
            conn.commit()
            conn.close()
            Snackbar(text=self.data['addjobs_jobSaved']).open()
            self.remainingCash_jobs(cc)

    def remainingCash_jobs(self,arg1):
        with open('data.txt') as outfile:
            data=json.load(outfile)
            remaining_home=data['home_cash']
        rest=float(remaining_home)+float(arg1)

        data['home_cash']="{:.2f}".format(float(rest))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)
