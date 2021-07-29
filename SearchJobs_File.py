from kivy.properties import ObjectProperty,StringProperty,ListProperty
from kivy.uix.popup import Popup
import sqlite3
import json




class Search_jobs(Popup):
    '''Search jobs'''
    txt_search=ObjectProperty()
    rv_search=ObjectProperty()

    def __init__(self):
        super().__init__()
        with open('languages.txt') as outfile:
            self.data=json.load(outfile)

    def find(self,*args):
        '''Find something in jobs'''
        self.conn = sqlite3.connect('jobs_db.db')
        self.cur=self.conn.cursor()
        searched=str(args[0]).lower()
        if searched=='':
            self.rv_search.data=[]
            return
        else:
            result=self.cur.execute("SELECT rowid,* FROM jobs_table")
            result=self.cur.fetchall()
            self.conn.commit()
            if searched:
                self.rv_search.data=[]
                for i in range(len(result)):
                    for j in result[i]:
                        j=str(j).lower()
                        if searched in j:
                            a=result[i][0] # index
                            b=result[i][1].split('-') #data completa
                            b=b[2]+'-'+b[1]+'-'+b[0]
                            cc=result[i][2] # city
                            d=result[i][3] # suma
                            e=result[i][4] # adresa
                            f=result[i][5] # persoana
                            g=result[i][6] # avans

                            unu="[color=#fb8500][b]{}[/b][/color] - {} - {} - {}".format(a,b,cc,f)
                            doi="[b]{}[/b] {} --- [b]{}[/b] {}".format(self.data['jobspage_taken'],d,self.data['jobspage_upfront'],g)
                            trei="[b]{}[/b] {}".format(self.data['jobspage_address'],e)
                            self.rv_search.data.append({'text':unu,'secondary_text':doi,'tertiary_text':trei})
            else:
                return