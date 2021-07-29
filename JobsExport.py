from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
import sqlite3
import smtplib
import csv
from kivymd.uix.snackbar import Snackbar
from email.message import EmailMessage
from kivy.uix.popup import Popup
import time
import glob
import os
import json



class Jobs_Export(Popup):
    #exp1=your email
    #exp2=your password
    #exp3=send to
    #exp4=subject
    #exp5=content

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def send_to_email(self, exp1, exp2, exp3, exp4, exp5):
        
        '''Send jobs as a csv file to email'''
        if exp1=='' or exp2=='' or exp3=='':
            Snackbar(text=self.data['expenses_fillTheFields']).open()
            return
        else:
            a=time.localtime()
            dates=str(a[2])+'-'+str(a[1])+'-'+str(a[0])+'_'+str(a[3])+'-'+str(a[4])+'-'+str(a[5])

            conn = sqlite3.connect('jobs_db.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM jobs_table")
            file_save = 'jobs_' + dates + '.csv'
            f = open(file_save, 'w', newline='')
            for i in cur.fetchall():
                csv.writer(f).writerow(i)
            f.close()
            if self.ids.check_db.state=='down':
                files = [file_save,'jobs_db.db','data.txt']
            elif self.ids.check_db.state=='normal':
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

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as conn:
                conn.login(exp1, exp2)
                conn.send_message(msg)

            Snackbar(text=self.data['expensesExport_sendSucces']+str(exp3)+'.').open()
        filelist = glob.glob('*.csv')
        for fl in filelist:
            os.remove(fl)
        self.dismiss()
