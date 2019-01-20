from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


class MenuScreen(Screen):
    pass


class ScoreScreen(Screen):
    pass


class StartPopup(Popup):
    localtime = datetime.datetime.now()


class EndPopup(Popup):
    pass


class sm(ScreenManager):
    menu_screen = ObjectProperty(None)
    score_screen = ObjectProperty(None)

    localtime = datetime.datetime.now()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('frisbee.json', scope)
    client = gspread.authorize(creds)

    team_sheet = client.open('Teams')
    ts1 = team_sheet.get_worksheet(0)
    ts2 = team_sheet.get_worksheet(1)
    worksheet_list = team_sheet.worksheets()
    wsl = str(worksheet_list).split()

    for word in wsl:
        if "Worksheet" in word:
            wsl.remove(word)
    for word in wsl:
        if "id" in word:
            wsl.remove(word)
    for word in wsl:
        if "<Worksheet" in word:
            wsl.remove(word)

    stat_sheet = client.open('Statistics')
    ss_sheet = stat_sheet.worksheet('Dummy')
    new_sheet = ""

    def spinner_clicked(self, wsl):
        pass

    t1p = ObjectProperty(True)
    t2p = ObjectProperty(False)

    def start_button(object):
        start_button = StartPopup()
        start_button.open()

    def end_button(object):
        end_button = EndPopup()
        end_button.open()


Builder.load_string("""
<sm>:
    MenuScreen:
        name: "menu_screen"
        BoxLayout:
            orientation: "vertical"
            padding: 10
            spacing: 20
            color: 0, 0, 0, 1

#label: first team, second team for clarity

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .05
                Label: 
                    text: "First Team"
                    size_hint_x: .5
                Label:
                    text: "Second Team"
                    size_hint_x: .5

#spinners for choosing the 2 opposing team
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .20
                Spinner:
                    text: root.wsl[0]
                    values: root.wsl
                    id: spinner1_id
                    on_text: root.spinner_clicked(spinner1_id.text)
                    on_text: root.ts1 = root.team_sheet.worksheet(spinner1_id.text[1:-1])
                Spinner:
                    text: root.wsl[1]
                    values: root.wsl
                    id: spinner2_id
                    on_text: root.spinner_clicked(spinner2_id.text)
                    on_text: root.ts2 = root.team_sheet.worksheet(spinner2_id.text[1:-1])
# pull

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .20
                CheckBox:
                    group: "pull"
                    active: True
                    value: root.t1p
                    size_hint_y: .25
                    on_press: pull_label_id.text = "Pulling team:" + spinner1_id.text
                Label:
                    id: pull_label_id
                    text: "Pulling team:" + spinner1_id.text
                    size_hint_y: .25
                CheckBox:
                    group: "pull"
                    value: root.t2p
                    size_hint_y: .25
                    on_press: pull_label_id.text = "Pulling team:" + spinner2_id.text

# start and end button
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .25
                Button:
                    text: "Ready"
                    on_press: root.worksheet = root.stat_sheet.add_worksheet(title=str(root.localtime.year) + "_"\
                     + str(root.localtime.month) + "_" + str(root.localtime.day) + "_" + str(root.localtime.hour)\
                     + "_" +str(root.localtime.minute) + str(root.localtime.second) +"_" + spinner1_id.text + "_vs_"\
                      + spinner2_id.text, rows ="100",\
                      cols= "20")
                    on_press: root.new_sheet = str(root.localtime.year) + "_" + str(root.localtime.month) + "_" \
                    + str(root.localtime.day) + "_" + str(root.localtime.hour) + "_" +str(root.localtime.minute) +\
                     str(root.localtime.second) +"_" + spinner1_id.text + "_vs_" + spinner2_id.text
                    on_press: goal_1_id.values = root.ts1.col_values(1)
                    on_press: assist_1_id.values = root.ts1.col_values(1)
                    on_press: goal_2_id.values = root.ts2.col_values(1)
                    on_press: assist_2_id.values = root.ts2.col_values(1)
                    on_release: app.root.start_button()
                    on_release: root.current = "score_screen"


                Button:
                    text: "Exit"
                    on_press: app.stop()

    ScoreScreen:
        name: "score_screen"
        BoxLayout:
            orientation: "vertical"
            padding: 10
            spacing: 20
            color: 0, 0, 0, 1
# team vs team label

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .25
                Label:
                    text: spinner1_id.text
                    size_hint_x: .25
                Label:
                    text: "Versus"
                    size_hint_x: .25
                Label:
                    text: spinner2_id.text
                    size_hint_x: .25

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .5
                Label:
                    id: team_1_score
                    text: "0"
                Label:
                    text: ":"
                Label:
                    id: team_2_score
                    text: "0"

#player spinners

            BoxLayout:
                orientation: "horizontal"

                BoxLayout:
                    orientation: "horizontal"
                    BoxLayout:
                        orientation: "vertical"
                        Label:
                            text: "Goal"
                        Spinner:
                            text: "team 1 player"
                            values: ["1"]
                            id: goal_1_id
                            on_text: root.spinner_clicked(goal_1_id.text)


                    BoxLayout:
                        orientation: "vertical"
                        Label:
                            text: "Assist"
                        Spinner:
                            text: "team 1 player"
                            values: ["1"]
                            id: assist_1_id
                            on_text: root.spinner_clicked(assist_1_id.text)


                BoxLayout:
                    orientation: "horizontal"
                    BoxLayout:
                        orientation: "vertical"
                        Label:
                            text: "Goal"
                        Spinner:
                            text: "team 2 player"
                            values: ["1"]
                            id: goal_2_id
                            on_text: root.spinner_clicked(goal_2_id.text)

                    BoxLayout:
                        orientation: "vertical"
                        Label:
                            text: "Assist"
                        Spinner:
                            text: "team 2 player"
                            values: ["1"]
                            id: assist_2_id
                            on_text: root.spinner_clicked(assist_2_id.text)

# score plus buttons            

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: .5
                Button:
                    text: "+1 point"
                    on_press: root.ss_sheet.append_row([str(root.localtime.hour)+ ':' + str(root.localtime.minute),\
                     spinner1_id.text, goal_1_id.text, assist_1_id.text])    
                    on_press: team_1_score.text = str(int(team_1_score.text)+1)
                    on_release: app.root.ss_sheet.update_acell('F1', team_1_score.text)
                    on_release: goal_1_id.text = "team 1 player"
                    on_release: assist_1_id.text = "team 1 player"

#on_press: plusz 1 pont, facebook post, label update  
                Button:
                    text: "+1 point"
                    on_press: root.ss_sheet.append_row([str(root.localtime.hour)+ ':' + str(root.localtime.minute),\
                    spinner2_id.text, goal_2_id.text, assist_2_id.text])
                    on_press: team_2_score.text = str(int(team_2_score.text)+1)
                    on_release: app.root.ss_sheet.update_acell('G1', team_2_score.text)
                    on_release: goal_2_id.text = "team 2 player"
                    on_release: assist_2_id.text = "team 2 player"


#on_press: plusz 1 pont, facebook post, label update 

            BoxLayout:
                orientation: "horizontal"
                BoxLayout:
                    orientation: "horizontal"
                    Button:
                        text: "Corr A -1"                                  
                        on_press: team_1_score.text = str(int(team_1_score.text)-1) 
                        on_release: app.root.ss_sheet.update_acell('F1', team_1_score.text)
                        on_release: app.root.ss_sheet.append_row(['KORREKCIÓ', '-1 pont', spinner1_id.text])
                    Button:
                        text: "Corr B -1"                                  
                        on_press: team_2_score.text = str(int(team_2_score.text)-1) 
                        on_release: app.root.ss_sheet.update_acell('G1', team_2_score.text)
                        on_release: app.root.ss_sheet.append_row(['KORREKCIÓ', '-1 pont', spinner2_id.text])
                    #last action delete
                Button:
                    text: "End"
                    on_press: app.root.ss_sheet.update_acell('L1', pull_label_id.text)
                    on_press: app.root.ss_sheet.update_acell('K1', \
                    str(root.localtime.hour)+ ':' + str(root.localtime.minute))                               
                    on_release: app.root.end_button()
                    on_release: root.current = "menu_screen"
                    #pop up: Next Match | Exit                   

<StartPopup>:
    name: "popup"
    size_hint: .5, .5
    auto_dismiss: False
    title: "Start the ScoreScreen"
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "Start"
            on_press: app.root.ss_sheet = app.root.stat_sheet.worksheet(app.root.new_sheet)
            on_release: app.root.ss_sheet.append_row(['Game Time', 'Team Get', 'Goal', 'Assist', 'Score:', '0',\
             '0', 'Game Start', str(root.localtime.hour)+ ':' + str(root.localtime.minute), 'Game End', 'not finished'])
            on_release: root.dismiss()    

<EndPopup>:
    name: "popup2"
    size_hint: .5, .5
    auto_dismiss: False
    title: "Next Match?"
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "Next Match"
            on_press: root.dismiss()
        Button:
            text: "Stop Application"
            on_press: app.stop()            


""")


class Frisbee_SK(App):

    def build(self):
        return sm()


if __name__ == '__main__':
    Frisbee_SK().run()
