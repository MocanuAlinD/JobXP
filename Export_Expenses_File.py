from kivy.uix.popup import Popup
import sqlite3
import smtplib
import csv
from email.message import EmailMessage
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty
from datetime import date,datetime
import datetime
import time
import os
import glob
import json


class Export_Expenses(Popup):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def export_to_file(self,exp1,exp2,exp3,exp4,exp5):
        #exp1=your email
        #exp2=your password
        #exp3=send to
        #exp4=subject
        #exp5=content
        if exp1=='' or exp2=='' or exp3=='' or exp4=='' or exp5=='':
            Snackbar(text=self.data['expenses_fillTheFields']).open()
            return
        else:
            a=time.localtime()
            dates=str(a[2])+'-'+str(a[1])+'-'+str(a[0])+'_'+str(a[3])+'-'+str(a[4])+'-'+str(a[5])

            conn = sqlite3.connect('jobs_db.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM exp_table")
            file_save = 'expenses_' + dates + '.csv'
            f = open(file_save, 'w', newline='')
            for i in cur.fetchall():
                csv.writer(f).writerow(i)
            f.close()

            if self.ids.check_db_exp.state=='down':
                files = [file_save,'jobs_db.db','data.txt']
            elif self.ids.check_db_exp.state=='normal':
                files = [file_save, 'data.txt']

            msg = EmailMessage()
            msg['Subject'] = exp4
            msg['From'] = exp1
            msg['To'] = exp3
            msg.set_content(exp5)

            for file in files:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                msg.add_attachment(file_data, maintype='application',
                                   subtype='octet-stream', filename=file_name)
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as conn:
                    conn.login(exp1, exp2)
                    conn.send_message(msg)
                Snackbar(text=self.data['expensesExport_sendSucces']+str(exp3)+'.').open()
            except:
                Snackbar(text=self.data['expensesExport_noInternet']).open()
        filelist = glob.glob('*.csv')
        for fl in filelist:
            os.remove(fl)
        self.dismiss()