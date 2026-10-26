from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget

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
    def build(self):
        Window.clearcolor = BG
        Window.size = (430, 760)

        self.exp = 0
        self.level  = 1

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

        root.add_widget(Widget(size_hint_y=None, height=dp(5)))

        root.add_widget(Label(
            text="STUDENT PROFILE",
            color=PARCHMENT,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(32),
            halign="left",
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

        root.add_widget(Widget(size_hint_y=None, height=dp(8)))

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

        mission =ProtocolButton(
            text="Begin Academic Assesment",
        )
         mission.bind(on_press=self.start_mission)
        root.add_widget(mission)

        root.add_widget(Widget())

        self.status_label = Label(
            text="STATUS: PENDING",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(30),
        )
        root.add_widget(self.status_label)

        return root


    def start_mission(self, instance):
        from kivy.uix.popup import Popup

        content  = BoxLayout(
        orientation="vertical",
        padding=dp(16),
        spacing=dp(12),
    )

        content.add_widget(Label(
        text="Which language is used  to build this prototype?",
        color=PARCHMENT,
        font_size="16sp",
    ))

        popup = Popup(
        text="ACADEMIC ASSESMENT",
        content=content,
        size_hint=(0.88,  0.60),
        separator_color=GOLD,
        background_color=PANEL,
    )

        for answer in ["Python",  "HTML", "SQL",]:
            button =  ProtocolButton(text=answer)
            button.bind(
                on_press=lambda btn, a=answer:
                self.check_answer(a, popup)
        )
        content.add_widget(button)

        popup.open()

    def check_answer(self, answer, popup):
        popup.dismiss()

        if answer == "Python":
         self.exp += 50
         self.status_label.text = "CORRECT! +25 EXP"

        if self.exp >= 100:
            self.exp -=100
            self.level +=  1

        self.level_label.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )
        self.exp_label.text = (
            f"EXPERIENCE {self.exp} / 100"
        )
        self.exp_bar.value = self.exp
        
        

if __name__ == "__main__":
    StudentProtocol().run()
