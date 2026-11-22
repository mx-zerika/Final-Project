from kivy.uix.scrollview import ScrollView
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from config import BG, PANEL, GOLD, PARCHMENT, MUTED
from systems.save_system import load_progress, save_progress
from systems.exp_system import award_exp
from systems.rank_system import (
    get_academic_rank,
    get_unlocked_rank_count,
    get_rank_status,
    RANKS
)

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

class AchievementCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*PANEL)
            self.bg_rect = RoundedRectangle(
                radius=[dp(8)]
            )

            self.bind(
                pos=self.update_bg,
                size=self.update_bg
            )
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class ProfileScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        # MAIN PROFILE LAYOUT
        main_layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10)
        )

        # PROFILE HEADER
        main_layout.add_widget(Label(
            text="[ STUDENT PROFILE ]",
            color=GOLD,
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))

        main_layout.add_widget(Label(
            text="ACADEMIC CENTER",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(25)
        ))

        #Scrollable Content 

        scroll = ScrollView(
        do_scroll_x=False,
        bar_width=dp(4)
        )

        content = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(12),
            spacing=dp(18)
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Student Emblem

        content.add_widget(Label(
            text= "STUDENT RECORD",
            color=GOLD,
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=dp(100)
        ))

        # Level
        self.profile_level = Label(
            text="ACADEMIC LEVEL 01",
            color=GOLD,
            font_size="20sp",
            size_hint_y=None,
            height=dp(45)
        )
        content.add_widget(self.profile_level)

        self.profile_rank = Label(
            text="RANK: FRESHMAN",
            color=GOLD,
            font_size="15sp",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )

        content.add_widget(self.profile_rank)

        # EXPERIENCE
        self.profile_exp = Label(
            text="EXPERIENCE 0 / 100",
            color=PARCHMENT,
            font_size="15sp",
            size_hint_y=None,
            height=dp(35)
        )
        content.add_widget(self.profile_exp)

        self.profile_exp_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(12)
        )
        content.add_widget(self.profile_exp_bar)

        # MISSION STATISTICS

        self.profile_mission = Label(
            text="LESSONS COMPLETED: 0 / 5",
            color=PARCHMENT,
            font_size="15sp",
            size_hint_y=None,
            height=dp(45)
        )
        content.add_widget(self.profile_mission)
        
        content.add_widget(Label(
            text="-- ACHIEVEMENT ARCHIVE --",
            color=GOLD,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))

        self.achievement_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10)
        )

        self.achievement_list.bind(
            minimum_height=self.achievement_list.setter("height")
        )

        content.add_widget(self.achievement_list)

        # MIssion archive place

        self.mission_archive = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10)
        )

        self.mission_archive.bind(
            minimum_height=self.mission_archive.setter("height")
        )

        content.add_widget(Label(
            text="LESSON ARCHIVE",
            color=GOLD,
            font_size="18sp",
            size_hint_y=None,
            height=dp(35)
        ))

        content.add_widget(self.mission_archive)

        content.add_widget(Widget(
                size_hint_y=None,
                height=dp(30)
                ))
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        #Fixed Navigation Button
        
        back_button = ProtocolButton(
            text="BACK TO CENTER"
        )
        
        back_button.bind(
            on_press=self.go_to_dashboard
        )
        
        main_layout.add_widget(back_button)
        
        self.add_widget(main_layout)

    def update_achievements(self):

        self.achievement_list.clear_widgets()

        achievements = [
            ( self.app.mission_index >= 1,
            "First Steps",
            "COMMON",
            "Complete your first learning lesson."),

            ( self.app.mission_index >= len(self.app.mission),
             "Knowledge Seeker",
                "RARE",
                "Complete every available lesson."),

            ( self.app.level >= 2,
             "The New Student of The Year",
                "EPIC",
                "Reach Academic Level 2"),

        ]

        for unlocked, achievement, rarity, description in achievements:

             if unlocked:
                 status = "[UNLOCKED]"
                 color = GOLD

             else:
                status = "[LOCKED]"
                color = MUTED

             achievement_card = AchievementCard(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(85)
             )

             achievement_card.add_widget(Label(
                 text=f"{status} {achievement}",
                 color=color,
                 font_size="14sp",
                 bold=True,
                 halign="left"
             ))

             achievement_card.add_widget(Label(
                 text=description,
                 color=PARCHMENT,
                 font_size="12sp",
                 halign="left",
                 valign="middle"
             ))

             achievement_card.add_widget(Label(
                 text=f" {rarity}",
                 color=MUTED,
                 font_size="10sp",
                 halign="left"
             ))

             self.achievement_list.add_widget(achievement_card)

    def update_mission_archive(self):
        self.mission_archive.clear_widgets()

        for index in range(self.app.mission_index):

            mission = self.app.mission[index]

            mission_box = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(65),
                spacing=dp(10),
                padding=[dp(8), dp(5)]
            )

            with mission_box.canvas.before:
                Color(*PANEL)
                mission_bg = RoundedRectangle(
                    pos=mission_box.pos,
                    size=mission_box.size,
                    radius=[dp(8)]
                )
            def update_mission_bg(instance, *args, bg=mission_bg):
                bg.pos = instance.pos
                bg.size = instance.size

            mission_box.bind(
                pos=update_mission_bg,
                size=update_mission_bg
            )

            mission_label = Label(
                text=f"LESSON {index + 1:02d}\n{mission['title']}",
                color=PARCHMENT,
                font_size="11sp",
                halign="left",
                valign="middle",
                size_hint_x=0.52
            )

            mission_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            status_label = Label(
                text="COMPLETED",
                color=GOLD,
                font_size="10sp",
                bold=True,
                size_hint_x=0.23,
                halign="center",
                valign="middle",
            )

            retry_button = ProtocolButton(
                text="REVIEW",
                size_hint_x=0.25
            )

            retry_button.bind(
                on_press=lambda btn, i=index:
                self.app.start_mission(btn, replay_index=i)
            )

            mission_box.add_widget(mission_label)
            mission_box.add_widget(status_label)
            mission_box.add_widget(retry_button)

            self.mission_archive.add_widget(mission_box)
                

    def go_to_dashboard(self, instance):
     self.manager.current = "dashboard"

class RankArchiveScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        #MAIN LAYOUT BOSS
        main_layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10)
        )

        #Header nya
        main_layout.add_widget(Label(
             text="[ ACADEMIC RANK ]",
             color=GOLD,
             font_size="12sp",
             bold=True,
             size_hint_y=None,
             height=dp(50)
         ))

        main_layout.add_widget(Label(
            text="YOUR ACADEMIC JOURNEY",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(25)
        ))

        self.rank_count_label = Label(
            text="RANKS UNLOCKED: 0 / 5",
            color=GOLD,
            font_size="13sp",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )

        main_layout.add_widget(self.rank_count_label)

        #Scrollable rank content yeyyy

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )

        self.rank_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(12),
            spacing=dp(15)
        )

        self.rank_list.bind(
            minimum_height=self.rank_list.setter("height")
        )

        scroll.add_widget(self.rank_list)
        main_layout.add_widget(scroll)

        #Going back button
        back_button = ProtocolButton(
            text="BACK"
        )

        back_button.bind(
            on_press=self.go_to_dashboard
        )

        main_layout.add_widget(back_button)
        self.add_widget(main_layout)

    def update_ranks(self):

        self.rank_list.clear_widgets()

        unlocked_count = get_unlocked_rank_count(self.app.level)

        self.rank_count_label.text = (
            f"RANKS UNLOCKED: {unlocked_count} / {len(RANKS)}"
        )

        for rank_name, min_level, max_level in RANKS:
            status = get_rank_status(
                self.app.level,
                min_level,
                max_level
            )
            
            if status == "CURRENT":
                status_text = "CURRENT RANK"
                color = GOLD

            elif status == "UNLOCKED":
                status_text = "UNLOCKED"
                color = PARCHMENT

            else:
                status_text = "LOCKED"
                color = MUTED

            rank_card = AchievementCard(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(8),
                size_hint_y=None,
                height=dp(100)
            )

            rank_card.add_widget(Label(
                text=rank_name,
                color=color,
                font_size="16sp",
                bold=True
            ))

            rank_card.add_widget(Label(
                text=f"LEVEL {min_level:02d} - {max_level:02d}",
                color=MUTED,
                font_size="12sp"
            ))

            rank_card.add_widget(Label(
                text=status_text,
                color=color,
                font_size="11sp",
                bold=True
            ))

            self.rank_list.add_widget(rank_card)
        

    def go_to_dashboard(self, instance):
        self.manager.current = "dashboard"

class StudentProtocol(App):
    def load_progress(self):
        load_progress(self)

    def save_progress(self):
        save_progress(self)

    def build(self):
        Window.clearcolor = BG
        Window.size = (430, 760)
        self.screen_manager = ScreenManager ()

        self.exp = 0
        self.level  = 1
        self.mission_index = 0
        self.load_progress()
        self.is_replay = False

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
            },


            {
                "title": "PYTHON FUNDAMENTALS II",
                "question": "Which keyword is used to define a function in Python?",
                "answers": [
                    "def",
                    "class",
                    "import"
                ],
                "correct": "def"
            },


            {
                "title": "PYTHON DATA TYPES",
                "question": "Which data type is used to store True or False values in Python?",
                "answers": [
                    "String",
                    "Boolean",
                    "Integer"
                ],
                "correct": "Boolean"
            }
        ]


        root = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8)
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
            text="AVAILABLE LESSONS",
            color=PARCHMENT,
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(36)
        ))

        self.mission_label = Label(
            text="LESSON 1 | KNOWLEDGE CHECK",
            color=GOLD,
            font_size="14sp",
            size_hint_y=None,
            height=dp(30)
        )
        root.add_widget(self.mission_label)

        self.mission_progress_label = Label(
            text="LESSONS COMPLETED: 0/5",
            color=PARCHMENT,
            font_size="13sp",
            size_hint_y=None,
            height=dp(28)        
            )

        root.add_widget(self.mission_progress_label)

        self.mission_progress_bar = ProgressBar(
            max=len(self.mission),
            value=0,
            size_hint_y=None,
            height=dp(10)
        )

        root.add_widget(self.mission_progress_bar)

        self.mission_button =ProtocolButton(
            text="Begin Academic Assesment",
        )

        self.mission_button.bind(on_press=self.start_mission)
        root.add_widget(self.mission_button)

        profile_button = ProtocolButton(
            text="STUDENT PROFILE"
        )

        profile_button.bind(
            on_press=self.open_profile
        )

        root.add_widget(profile_button)

        rank_button = ProtocolButton(
            text="ACADEMIC RANKS"
        )

        rank_button.bind(
            on_press=self.open_rank_archive
        )

        root.add_widget(rank_button)

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

        self.mission_progress_label.text = (
            f"LESSONS COMPLETED: {self.mission_index} / {len(self.mission)}"
        )

        self.mission_progress_bar.value = self.mission_index

        if self.mission_index < len(self.mission):
            next_number = self.mission_index + 1
            self.mission_label.text = (
                f"LESSONS {next_number:02d} | KNOWLEDGE CHECK"
            )
        else:
            self.mission_label.text = "ALL LESSONS COMPLETED!"
            self.mission_button.text = "LESSONS COMPLETED!"
            self.mission_button.disabled = True
            self.status_label.text = "ACADEMIC STATUS: COMPLETED!"

        # Dashboard Screen

        dashboard_screen = Screen(name="dashboard")
        dashboard_screen.add_widget(root)

        self.screen_manager.add_widget(dashboard_screen)

        #Profile Screen
        self.profile_screen = ProfileScreen(
            self, name="profile"
        )

        self.screen_manager.add_widget(self.profile_screen)

        #Rank Archive Screen
        self.rank_archive_screen = RankArchiveScreen(
            self, name="rank_archive"
        )

        self.screen_manager.add_widget(self.rank_archive_screen)

        return self.screen_manager

    def open_profile(self, instance):
        self.profile_screen.profile_level.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )
        self.profile_screen.profile_exp.text = (
            f"EXPERIENCE {self.exp} / 100"
        )

        self.profile_screen.profile_exp_bar.value = self.exp

        self.profile_screen.profile_mission.text = (
            f"LESSON COMPLETED: {self.mission_index} / {len(self.mission)}"
        )

        self.profile_screen.update_achievements()
        self.profile_screen.update_mission_archive()
        self.profile_screen.profile_rank.text = (
            f"RANK: {self.get_academic_rank()}"
        )
        self.screen_manager.current = "profile"

    def open_rank_archive(self, instance):

        self.rank_archive_screen.update_ranks()
        self.screen_manager.current = "rank_archive"

    def start_mission(self, instance, replay_index=None):

        # Determine if this is a replay
        is_replay = replay_index is not None

        if is_replay:
            mission = self.mission[replay_index]

        else:
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
        title=mission["title"] + (" | REPLAY" if is_replay else ""),
        content=content,
        size_hint=(0.88,  0.60),
        separator_color=GOLD,
        background_color=PANEL,
    )

        for answer in mission["answers"]:

            button =  ProtocolButton(text=answer)
            
            button.bind(
                on_press=lambda btn, a=answer, m=mission, p=popup, r=is_replay:
                self.check_answer(
                    a,
                    m["correct"],
                    p,
                    r 
                    )
        )
            # IMPORTANT: KEEP THIS INSIDE THE FOR LOOP!
            content.add_widget(button)

        popup.open()

    # CHECK ANSWER

    def check_answer(self, answer, correct_answer, popup, is_replay=False):
        popup.dismiss()
        previously_unlocked = self.get_unlocked_achivements()

        if answer == correct_answer:

            if is_replay:
                self.status_label.text = "LESSON REVIEW COMPLETED. NO EXP GAINED"
            else:
               old_rank = self.get_academic_rank()

               old_level, new_level = award_exp(self, 20)

            # New thing i added. Advanced lesson hehehe
            self.mission_index += 1
            self.save_progress()

        new_rank = self.get_academic_rank()

        if new_level > old_level:
            if new_rank != old_rank:
                self.show_rank_up_popup(new_rank)
            else:
                self.show_level_up_popup()

            if self.mission_index < len(self.mission):
                next_number = self.mission_index + 1

                self.mission_label.text = (
                    f"LESSON {next_number:02d} | KNOWLEDGE CHECK"
                )

                self.mission_button.text = "START LESSON"
                self.mission_button.disabled = False

            else:
                self.mission_label.text = "ALL LESSONS COMPLETED" 
                self.mission_button.text = "LESSONS COMPLETED"
                self.mission_button.disabled = True
                self.status_label.text = "ACADEMIC STATUS: COMPLETED!"

        else:
            self.status_label.text = "INCORRECT! NO EXP"

        #Update Dashboard - renew again 
        self.level_label.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )
        self.exp_label.text = (
            f"EXPERIENCE {self.exp} / 100"
        )
        self.exp_bar.value = self.exp

        self.mission_progress_label.text = (
            f"LESSONS COMPLETED: {self.mission_index} / {len(self.mission)}"
        )
        self.mission_progress_bar.value = self.mission_index

        self.profile_screen.update_achievements()

        newly_unlocked = (
            self.get_unlocked_achivements()
            - previously_unlocked
        )

        if newly_unlocked:
            self.show_achivements_popup(
                sorted(newly_unlocked)
            )

    def show_level_up_popup(self):


        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(20)
        )

        title = Label(
            text="ACADEMIC PROMOTION",
            color=GOLD,
            font_size="20sp",
            bold=True
        )

        level_text = Label(
            text=f"YOU HAVE REACHED LEVEL {self.level:02d}!",
            color=PARCHMENT,
            font_size="16sp"
        )

        message = Label(
            text="Your Knowledge continues to grow.",
            color=MUTED,
            font_size="13sp"
        )

        close_button = ProtocolButton(
            text="CONTINUE"
        )

        content.add_widget(title)
        content.add_widget(level_text)
        content.add_widget(message)
        content.add_widget(close_button)

        popup = Popup(
            title="",
            content=content,
            size_hint=(None, None),
            size=(dp(340), dp(280)),
            background_color=BG,
            separator_height=0
        )

        close_button.bind(on_press=popup.dismiss)

        popup.open()

    def show_rank_up_popup(self, new_rank):
        content = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )

        content.add_widget(Label(
            text="ACADEMIC PROMOTION!",
            color=GOLD,
            font_size="13sp",
            bold=True
        ))

        content.add_widget(Label(
            text="NEW RANK ACHIEVED!",
            color=PARCHMENT,
            font_size="20sp",
            bold=True
        ))

        content.add_widget(Label(
            text=new_rank,
            color=GOLD,
            font_size="18sp",
            bold=True
        ))

        content.add_widget(Label(
            text="Your academic journey continues..",
            color=MUTED,
            font_size="12sp"
        ))

        close_button = ProtocolButton(
            text="CONTINUE"
        )

        content.add_widget(close_button)

        popup = Popup(
            title="ACADEMIC PROMOTION",
            content=content,
            size_hint=(0.85, 0.55),
            auto_dismiss=False
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()
            
    def get_unlocked_achivements(self):
        unlocked = set()

        if self.mission_index >= 1:
            unlocked.add("FIRST STEPS")

        if self.mission_index >= len(self.mission):
            unlocked.add("KNOWLEDGE SEEKER")

        if self.level >= 2:
            unlocked.add("THE NEW STUDENT")

        return unlocked

    def show_achivements_popup(self, new_achivements):

        description = {
            "FIRST STEPS": "Complete your first learning lesson.",
            "KNOWLEDGE SEEKER": "Complete every avaible lesson.",
            "THE SCHOLAR": "Reach Level 2."
        }

        message = "\n\n". join(
            f"{name}\n{description[name]}"
            for name in new_achivements
        )

        popup = Popup(
            title="ACHIVEMENT UNLOCKED!",
            content=Label(
                text=message,
                color=PARCHMENT,
                halign="center",
                valign="middle"
            ),
            size_hint=(None, None),
            size=(dp(340), dp(250)),
            background_color=PANEL,
            separator_color=GOLD
        )

        popup.open()

    def get_academic_rank(self):
        return get_academic_rank(self.level)


if __name__ == "__main__":
    StudentProtocol().run()
