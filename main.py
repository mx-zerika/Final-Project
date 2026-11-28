from kivy.uix.scrollview import ScrollView
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
from systems.subject_system import (
    load_subject_progress,
    save_subject_progress,
    complete_subject_lesson,
    get_subject_statistics
)
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
            text="[ STUDENT RECORD ]",
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

        self.profile_scroll = scroll

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
            text="-- ACADEMIC ACHIEVEMENT --",
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
            text="-- LESSON RECORD --",
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
             "The New Student",
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

        total_lessons = len(self.app.mission)
        completed_count = min(
            max(self.app.mission_index, 0),
            total_lessons
        )

        for index, mission in enumerate(self.app.mission):

            mission_box = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(65),
                spacing=dp(8),
                padding=[dp(8), dp(5)]
            )

            with mission_box.canvas.before:
                Color(*PANEL)
                mission_bg = RoundedRectangle(
                    pos=mission_box.pos,
                    size=mission_box.size,
                    radius=[dp(8)]
                )
            mission_box.bind(
               pos=lambda instance, value, bg=mission_bg:
               setattr(bg, "pos", value),

               size=lambda instance, value, bg=mission_bg:
               setattr(bg, "size", value)
           )
        
            mission_label = Label(
                text=f"LESSON {index + 1:02d}\n{mission['title']}",
                color=PARCHMENT,
                font_size="10sp",
                halign="left",
                valign="middle",
                size_hint_x=0.48
            )

            mission_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            if index < completed_count:
                status = "COMPLETED!"
                status_color = GOLD
                button_text = "REVIEW"
                button_disabled = False

            elif index == completed_count:
                status = "CURRENT LESSON"
                status_color = GOLD
                button_text = "START"
                button_disabled = False 

            else:
                status = "LOCKED"
                status_color = MUTED
                button_text = "LOCKED"
                button_disabled = True

            status_label = Label(
                text=status,
                color=status_color,
                font_size="9sp",
                bold=True,
                size_hint_x=0.24,
                halign="center"
            )

            action_button = ProtocolButton(
                text=button_text,
                size_hint_x=0.28,
                disabled=button_disabled
            )

            if index < completed_count:
                action_button.bind(
                    on_press=lambda btn, i=index:
                    self.app.start_mission(
                        btn,
                        replay_index=i
                    )
                )

            elif index == completed_count:
                action_button.bind(
                    on_press=self.app.start_mission
                )

            mission_box.add_widget(mission_label)
            mission_box.add_widget(status_label)
            mission_box.add_widget(action_button)

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

        self.rank_scroll = scroll

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
            padding=dp(12),
            spacing=dp(6)
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
            bold=True,
            size_hint_y=None,
            height=dp(35),
        )

        root.add_widget(self.level_label)

        self.rank_label = Label(
            text="RANK: FRESHMAN",
            color=PARCHMENT,
            font_size="14sp",
            bold=True,
            size_hint_y=None,
            height=dp(26)
        )

        root.add_widget(self.rank_label)

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
            text="ACADEMIC CURRICULUM",
            color=PARCHMENT,
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(36)
        ))

        self.mission_label = Label(
            text="LESSON 01 | KNOWLEDGE CHECK",
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
            text="Start Lesson",
        )

        self.mission_button.bind(on_press=self.start_mission)
        root.add_widget(self.mission_button)

        profile_button = ProtocolButton(
            text="Student Profile"
        )

        profile_button.bind(
            on_press=self.open_profile
        )

        root.add_widget(profile_button)

        rank_button = ProtocolButton(
            text="Academic Ranks"
        )

        rank_button.bind(
            on_press=self.open_rank_archive
        )

        root.add_widget(rank_button)

        root.add_widget(Widget())

        self.status_label = Label(
            text="System Ready. Awaiting Student Input..",
            color=MUTED,
            font_size="12sp",
            size_hint_y=None,
            height=dp(36),
            halign="center",
            valign="middle",
        )
        root.add_widget(self.status_label)

        # Restore Dashboard
        self.refresh_dashboard_display()

        if self.mission_index < len(self.mission):
            next_number = self.mission_index + 1
            self.mission_label.text = (
                f"LESSON {next_number:02d} | KNOWLEDGE CHECK"
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

    def refresh_dashboard_display(self):
        total_lessons = len(self.mission)
        completed_lessons = min(self.mission_index, total_lessons)

        #Academic infor
        self.level_label.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )

        self.rank_label.text = (
            f"RANK: {self.get_academic_rank()}"
        )

        #EXP infor
        self.exp_label.text = (
            f"EXPERIENCE {self.exp} / 100"
        )

        self.exp_bar.value = self.exp

        #Lesson progress cuy
        self.mission_progress_label.text = (
            f"LESSONS COMPLETED: "
            f"{completed_lessons} / {total_lessons}"
        )

        self.mission_progress_bar.max = total_lessons
        self.mission_progress_bar.value = completed_lessons 

    def refresh_profile_display(self):
        profile = self.profile_screen
        profile.profile_level.text = (
            f"ACADEMIC LEVEL {self.level:02d}"
        )
        profile.profile_rank.text = (
            f"RANK: {self.get_academic_rank()}"
        )
        profile.profile_exp.text = (
            f"EXPERIENCE {self.exp} / 100"
        )

        profile.profile_exp_bar.value = self.exp

        profile.profile_mission.text = (
            f"LESSONS COMPLETED: "
            f"{self.mission_index} / {len(self.mission)}"
        )

        profile.update_achievements()
        profile.update_mission_archive()

    def open_profile(self, instance):
       self.refresh_profile_display()
       self.profile_screen.profile_scroll.scroll_y = 1
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
        font_size="17sp",
        size_hint_y=True,
        height=dp(110),
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

            question_label = content.children[-1]
            question_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

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
                    self.status_label.text = "CORRECT ANSWER. KNOWLEDGE ACQUIRED"

               else:
                   self.mission_label.text = "All Lessons Completed!"
                   self.mission_button.text = "Lessons Completed!"
                   self.mission_button.disabled = True
                   self.status_label.text = "Academic Status: Completed"
                   
        else:
            if is_replay:
                self.status_label.text = (
                    "INCORRECT REVIEW ANSWER."
                )
            else:
                self.status_label.text = "INCORRECT ANSWER. TRY AGAIN?"

        #Update Dashboard - renew again 
        self.refresh_dashboard_display()
        self.refresh_profile_display()
    
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
            text="ACADEMIC RECORD UPDATED",
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
            text="Your academic standing has advanced. Keep it up.",
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
            "KNOWLEDGE SEEKER": "Complete every available lesson.",
            "THE NEW STUDENT": "Reach Level 2."
        }

        message = "\n\n". join(
            f"{name}\n{description[name]}"
            for name in new_achivements
        )

        popup = Popup(
            title="ACADEMIC ACHIEVEMENT",
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

    def show_notification(self, title, message):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12)
        )

        content.add_widget(Label(
            text=message,
            color=PARCHMENT,
            font_size="14sp",
            halign="center",
            valign="middle"
        ))

        close_button = ProtocolButton(
            text="ACKNOWLEDGE"
        )

        content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.42),
            background_color=BG,
            separator_color=GOLD
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

  def sync_subject_progress(self):
        for lesson in self.mission[:self.mission_index]:

            subject = lesson.get("subject")
            lesson_id = lesson.get("id")

            if subject and lesosn_id:
                complete_subject_lesson(
                    self.subject_progress,
                    subject,
                    lesson_id
                )

            save_subject_progress(self.subject_progress)
            self.sync_subject_progress()


if __name__ == "__main__":
    StudentProtocol().run()
