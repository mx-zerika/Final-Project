import json
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

# Dark Academia Palette

BG = (0.098,  0.090,0.075, 1)
PANEL= (0.161, 0.145, 0.122, 1)
GOLD = (0.725, 0.604, 0.404, 1)
PARCHMENT = (0.906, 0.847,  0.722, 1)
MUTED  =  (0.66, 0.62, 0.54, 1)


class ProtocolButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = PANEL
        self.color = PARCHMENT
        self.font_size = "15sp"
        self.size_hint_y  = None
        self.height = dp(48)


class StudentProtocol(App):
     def load_progress(self):
        if os.path.exists("progress.json"):
            try:
                with open("progress.json", "r") as file:
                    data = json.load(file)

                self.exp = data.get("exp", 0)
                self.level = data.get("level", 1)
                self.mission_index = data.get("mission_index", 0)

            except (json.JSONDecodeError, TypeError, ValueError):
                print("Save file is invalid. Starting fresh.")
    def save_progress(self):
        data = {
            "exp": self.exp,
            "level": self.level,
            "mission_index": self.mission_index 
        }

        with open("progress.json", "w") as file:
            json.dump(data, file, indent=4)

        print("PROGRESS SAVED!")

    def build(self):
        Window.clearcolor = BG
        Window.size = (430, 760)

        self.exp = 0
        self.level  = 1
        self.mission_index = 0

         #MISSION DATABASE

        self.mission = [
            {
                "title": "PROGRAMMING FUNDAMENTALS",
                "question": "Which language is used to build this prototype?",
                "answers": ["Python", "HTML", "SQL"],
                "correct": "Python"
            },

            {
                "title": "WEB DEVELOPMENT",
                "question": "Which language is used to style web pages?",
                "answers": ["CSS", "HTML", "SQL"],
                "correct": "CSS"
            },

            {
                "title": "DATABASE FUNDAMENTALS",
                "question": "Which language is commonly used to query databases?",
                "answers": ["CSS", "Kotlin", "SQL"],
                "correct": "SQL"
            }
        ]

        
        root = BoxLayout(
            orientation="vertical",
            padding=dp(22),
            spacing=dp(14)
        )

        root.add_widget(Label(
            text="[ THE STUDENT  PROTOCOL ]",
            color=GOLD,
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=dp(52),
        ))

        root.add_widget(Label(
            text="ACADEMIC CENTER",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(25),
        ))

        root.add_widget(Widget(
            size_hint_y=None, 
            height=dp(5)
        ))

        root.add_widget(Label(
            text="STUDENT PROFILE",
            color=PARCHMENT,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(32),
        ))

        self.level_label  =  Label(
            text="ACADEMIC LEVEL 01",
            color=GOLD,
            font_size="19sp",
            size_hint_y=None,
            height=dp(35),
        )
        root.add_widget(self.level_label)

        self.exp_label  = Label(
            text="EXPERIENCE 0 / 100",
            color=PARCHMENT,
            size_hint_y=None,
            height=dp(28),
        )
        root.add_widget(self.exp_label)

        self.exp_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(12),
        )
        root.add_widget(self.exp_bar)

        root.add_widget(Widget(
            size_hint_y=None, 
            height=dp(8)
        ))

        root.add_widget(Label(
            text="AVAIBLE MISSIONS",
            color=PARCHMENT,
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(36)
        ))

        root.add_widget(Label(
            text="MISSION 01 | KNOWLEDGE CHECK",
            color=GOLD,
            font_size="14sp",
            size_hint_y=None,
            height=dp(30)
        ))
        root.add_widget(self.mission_label)
        
        self.mission_button =ProtocolButton(
            text="Begin Academic Assesment",
        )
        
        self.mission_button.bind(on_press=self.start_mission)
        root.add_widget(self.mission_button)

        root.add_widget(Widget())

        self.status_label = Label(
            text="STATUS: PENDING",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(30),
        )
        root.add_widget(self.status_label)

        # Restore Dashboard

        self.level_label.text = f"ACADEMIC LEVEL {self.level:02d}"
        self.exp_label.text = f"EXPERIENCE {self.exp} / 100"
        self.exp_bar.value = self.exp

        if self.mission_index < len(self.mission):
            next_number = self.mission_index + 1
            self.mission_label.text = (
                f"MISSION {next_number:02d} | KNOWLEDGE CHECK"
            )
        else:
            self.mission_label.text = "ALL MISSION COMPLETED!"
            self.mission_button.text = "MISSION COMPLETED!"
            self.mission_button.disabled = True
            self.status_label.text = "ACADEMIC STATUS: COMPLETED!"


        return root


    def start_mission(self, instance):
       
        if self.mission_index >= len(self.mission):
            return

        
        mission = self.mission[self.mission_index]

        content  = BoxLayout(
        orientation="vertical",
        padding=dp(16),
        spacing=dp(12),
    )

        content.add_widget(Label(
        text=mission["question"],
        color=PARCHMENT,
        font_size="16sp",
        size_hint_y=None,
        height=dp(85),
        halign="center",
        valign="middle",
    ))

        popup = Popup(
        title=mission["title"],
        content=content,
        size_hint=(0.88,  0.60),
        separator_color=GOLD,
        background_color=PANEL,
    )

       for answer in mission["answers"]:

            button =  ProtocolButton(text=answer)
            
            button.bind(
                on_press=lambda btn, a=answer, m=mission, p=popup:
                self.check_answer(
                    a,
                    m["correct"],
                    p 
                    )
        )
            # IMPORTANT: KEEP THIS INSIDE THE FOR LOOP!
            content.add_widget(button)

        popup.open()


    def check_answer(self, answer, correct_answer, popup):
        popup.dismiss()

        if answer == correct_answer:

            # REWARD  
            self.exp += 20
            self.status_label.text = "CORRECT! +20 EXP"

            # LEVEL SYSTEM

            while self.exp >= 100:
                self.exp -=100
                self.level += 1

            self.level_label.text = (
                f"ACADEMIC LEVEL {self.level:02d}"
            )
            self.exp_label.text = (
                f"EXPERIENCE {self.exp} / 100"
            )
            self.exp_bar.value = self.exp

            self.mission_index += 1
            print("MISSION INDEX:", self.mission_index)
            print("TOTAL MISSIONS:", len(self.mission))

            if self.mission_index < len(self.mission):
                next_number = self.mission_index + 1

                self.mission_label.text = (
                    f"MISSION {next_number:02d} | KNOWLEDGE CHECK"
                )

            else:
                self.mission_label.text = "ALL MISSIONS COMPLETED" 
                self.mission_button.text = "MISSION COMPLETED"
                self.mission_button.disabled = True
                self.status_label.text = "ACADEMIC STATUS: COMPLETED!"

        else:
     
            self.status_label.text = "INCORRECT! NO EXP"

        self.level_label.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )

        self.exp_label.text = (
            f"EXPERIENCE {self.exp} / 100"
        )
        self.exp_bar.value = self.exp     

if __name__ == "__main__":
    StudentProtocol().run()
