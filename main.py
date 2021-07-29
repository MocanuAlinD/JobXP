from Expenses import Expenses
from Export_Expenses_File import Export_Expenses
from Stats_File import Stats
from SearchJobs_File import Search_jobs
from AddJobs_File import AddJobs
from EditJobs_File import EditJobs
from JobsPage_File import JobsPage
from JobsExport import Jobs_Export

from kivymd.uix.button import MDRectangleFlatButton,MDFillRoundFlatButton,MDTextButton,MDIconButton
from kivymd.uix.button import MDRaisedButton,MDFloatingActionButtonSpeedDial
from kivymd.uix.navigationdrawer import MDNavigationDrawer,NavigationLayout
from kivy.properties import ObjectProperty,StringProperty,ListProperty
from kivymd.uix.list import ThreeLineListItem,ThreeLineAvatarListItem
from kivymd.uix.list import OneLineAvatarListItem,OneLineListItem
from kivymd.uix.button import MDFlatButton,MDRoundFlatButton
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.picker import MDTimePicker,MDDatePicker
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window as w
from kivymd.uix.card import MDSeparator
from kivymd.uix.dialog import MDDialog
from email.message import EmailMessage
from kivymd.uix.tab import MDTabsBase
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from datetime import date
from kivy import utils
import datetime
import platform
import sqlite3
import smtplib
import random
import json
import sys
import os
import csv

kv='''
#:import random random
#:import utils kivy.utils
#:import Factory kivy.factory.Factory
#:import metrics kivy.metrics
#: import SlideTransition kivy.uix.screenmanager.SlideTransition
#: import CardTransition kivy.uix.screenmanager.CardTransition
#: import SwapTransition kivy.uix.screenmanager.SwapTransition
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
#: import WipeTransition kivy.uix.screenmanager.WipeTransition
#: import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#: import RiseInTransition kivy.uix.screenmanager.RiseInTransition
#: import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    id: sm
    transition: NoTransition()
    # transition: SlideTransition()
    # transition: CardTransition()
    # transition: SwapTransition(duration=0.4)
    # transition: FadeTransition(duration=0.3)
    # transition: WipeTransition()
    # transition: FallOutTransition()
    # transition: RiseInTransition()
    MainPage:
        id: idmainpage
    JobsPage:
        id: idjobspage
    Stats:
        id: idstatspage
    Expenses:
        id: idexpenses
    SettingsPage:
        id: idsettings


<Item>
    IconLeftWidget:
        icon: root.source

<ExitButton@MDIconButton>:
    icon: 'exit-to-app'
    size_hint: 0.2,0.05
    pos_hint: {'right': 0.98, 'top': 0.98}
    theme_text_color: "Custom"
    text_color: utils.get_color_from_hex('#e76f51')
    on_release: app.stop()

<PalBut@MDIconButton>:
    size_hint: 1,1

<Check@MDCheckbox>:
    group: 'group'
    unselected_color: 0,1,0,1

<Alin@ThreeLineListItem>:
    color: 1,0,0,0
    markup: True
    theme_text_color: 'Custom'
    secondary_theme_text_color: 'Custom'
    tertiary_theme_text_color: 'Custom'
    text_color: 1,1,1,0.8
    secondary_text_color: 1,1,1,0.8
    tertiary_text_color: 1,1,1,0.8
    font_style: 'Body2'
    secondary_font_style: 'Body2'
    tertiary_font_style: 'Body2'

<Alin_money@ThreeLineListItem>:
    halign: 'left'
    markup: True
    theme_text_color: 'Custom'
    secondary_theme_text_color: 'Custom'
    tertiary_theme_text_color: 'Custom'
    text_color: 1,1,1,0.8
    secondary_text_color: 1,1,1,0.8
    tertiary_text_color: 1,1,1,0.8
    font_style: 'Body2'
    secondary_font_style: 'Body2'
    tertiary_font_style: 'Body2'

# in stats.kv
<Alin_money_jobs@OneLineListItem>:
    halign: 'left'
    markup: True
    theme_text_color: 'Custom'
    text_color: 1,1,1,0.8
    font_style: 'Body2'

# in expenses.kv
<All_expenses@OneLineListItem>:
    halign: 'left'
    markup: True
    theme_text_color: 'Custom'
    text_color: 1,1,1,0.8
    font_style: 'Body2'
    
# expenses.kv search tab
<Alin_exp@OneLineListItem>:
    halign: 'left'
    markup: True
    theme_text_color: 'Custom'
    text_color: 1,1,1,0.8
    font_style: 'Body2'


# <Alin_exp_remove@OneLineListItem>:
#     halign: 'left'
#     markup: True
#     theme_text_color: 'Custom'
#     text_color: 1,1,1,0.8
#     font_style: 'Body2'
#     on_release: app.root.ids.idexpenses.remove_exp(self.text.split(' ')[0])

'''

class ImageButton(ButtonBehavior,Image):
    pass


class SettingsPage(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('languages.txt') as outfile:
            self.data1=json.load(outfile)

    def clear_DB(self, abc):
        conn=sqlite3.connect('jobs_db.db')
        cur=conn.cursor()
        cur.execute('DELETE FROM ' + abc)
        conn.commit()
        conn.close()

    def change_cash(self,cash_modified):
        if not cash_modified:
            return

        with open('data.txt') as outfile:
            data=json.load(outfile)
            # remaining_home=data['home_cash']

        # data={}
        data['home_cash']="{:.2f}".format(float(cash_modified))
        with open('data.txt', 'w') as outfile:
            json.dump(data,outfile)
        self.ids.new_cash.text=''
        Snackbar(text='{} {} lei'.format(self.data1['mainpage_newCash'],cash_modified)).open()


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class Item(ThreeLineAvatarListItem):
    source = StringProperty()
    

class MainPage(Screen):
    pass

class Main(MDApp):
    language={}

    def build(self):
        with open('languages.txt') as outfile:
            data=json.load(outfile)
        for i in data.items():
            self.language[i[0]]=i[1]

        self.current_date=datetime.datetime.now()
        self.add_day=str(self.current_date.day)
        self.add_month=str(self.current_date.month)
        self.add_year=str(self.current_date.year)
        self.create_db()
        self.toolbar_color=utils.get_color_from_hex("#004E64") # albastru inchis
        self.bg_color=utils.get_color_from_hex("#006494")      # albastru intre
        self.fg_color=utils.get_color_from_hex("#247ba0")      # albastru intre
        self.login_bg=utils.get_color_from_hex("#1b98e0")      # albastru deschis
        
        self.green_bg=utils.get_color_from_hex("#1D353F")
        self.green_fg=utils.get_color_from_hex("#2a9d8f")
        self.green=utils.get_color_from_hex("#7AE582")
        self.check_active_color=utils.get_color_from_hex('#457F96')
        self.white=utils.get_color_from_hex('#e8f1f2')

        w.softinput_mode='below_target'
        if platform.system() == 'Windows':
            w.size = (360, 740)
            w.top = 40
            w.left=500
        elif platform.system() == 'android' or platform.system() == 'linux':
            pass
        Builder.load_file('kv_folder/mainpage.kv')
        Builder.load_file('kv_folder/jobspage.kv')
        Builder.load_file('kv_folder/stats.kv')
        Builder.load_file('kv_folder/addjobs.kv')
        Builder.load_file('kv_folder/editjobs.kv')
        Builder.load_file('kv_folder/expenses.kv')
        Builder.load_file('kv_folder/settingspage.kv')
        Builder.load_file('kv_folder/jobs_export.kv')
        screen = Builder.load_string(kv)
        return screen

    def create_db(self):
        conn =  sqlite3.connect('jobs_db.db')
        c=conn.cursor()
        c.execute(''' CREATE TABLE IF NOT EXISTS jobs_table (
        dt text,
        city text,
        amount integer,
        address text,
        person text,
        upfront integer)
        ''')
        conn.commit()

        c.execute(''' CREATE TABLE IF NOT EXISTS exp_table (
        dt text,
        amount integer,
        product text,
        category text)
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def restart():
        os.execvp(sys.executable, ['python'] + sys.argv)

    def change_language_ro(self):
        with open('langro.txt') as outfile:
            data=json.load(outfile)

        for i in data.items():
            self.language[i[0]]=i[1]

        with open('languages.txt', 'w') as outfile:
            json.dump(self.language,outfile)
        
    def change_language_en(self):
        with open('langen.txt') as outfile:
            data=json.load(outfile)
            
        for i in data.items():
            self.language[i[0]]=i[1]

        with open('languages.txt', 'w') as outfile:
            json.dump(self.language,outfile)



if __name__=='__main__':
    Main().run()
