# main.py (FINAL: SAVE & LOAD SYSTEM FIXED)
import random
import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader

# Warna Background (Biru Gelap Modern)
Window.clearcolor = (0.1, 0.15, 0.22, 1)

kv_string = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

# Template Tombol Keren
<RoundedButton@Button>:
    background_color: 0,0,0,0  
    bg_color: 0.2, 0.6, 1, 1
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]
    font_size: '18sp'
    bold: True
    color: 1, 1, 1, 1

ScreenManager:
    transition: SlideTransition()
    GradeScreen:
    MenuScreen:
    GameScreen:

<GradeScreen>:
    name: 'grade'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20

        Label:
            text: "MATH MASTER"
            font_size: '42sp'
            bold: True
            color: 1, 0.8, 0, 1
            size_hint: 1, 0.3

        # Tombol Load Game
        RoundedButton:
            id: btn_resume
            text: "LANJUTKAN GAME TERAKHIR"
            bg_color: 0.3, 0.3, 0.3, 1
            size_hint: 1, 0.15
            disabled: True
            on_release: 
                app.play_sound('click')
                app.load_last_game()

        Label:
            text: "ATAU PILIH KELAS BARU:"
            font_size: '16sp'
            color: 0.7, 0.7, 0.7, 1
            size_hint: 1, 0.1

        RoundedButton:
            text: "KELAS 3 SD"
            bg_color: 0.2, 0.7, 0.3, 1
            on_release:
                app.play_sound('click')
                app.set_grade(3)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 5 SD"
            bg_color: 0.9, 0.5, 0.1, 1
            on_release:
                app.play_sound('click')
                app.set_grade(5)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

        RoundedButton:
            text: "KELAS 8 SMP"
            bg_color: 0.8, 0.2, 0.2, 1
            on_release:
                app.play_sound('click')
                app.set_grade(8)
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20

        Label:
            text: app.grade_title
            font_size: '22sp'
            bold: True
            color: 0.5, 0.8, 1, 1
            size_hint: 1, 0.15

        GridLayout:
            cols: 2
            spacing: 20
            size_hint: 1, 0.6

            RoundedButton:
                text: "Tambah (+)"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('tambah')

            RoundedButton:
                text: "Kurang (-)"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('kurang')

            RoundedButton:
                text: "Kali (x)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('kali')

            RoundedButton:
                text: "Bagi (:)"
                bg_color: 0.7, 0.3, 0.6, 1
                on_release:
                    app.play_sound('click')
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'game'
                    root.manager.get_screen('game').start_new_game('bagi')

        RoundedButton:
            text: "<< KEMBALI"
            bg_color: 0.4, 0.4, 0.4, 1
            size_hint: 1, 0.15
            on_release: 
                app.play_sound('click')
                root.manager.transition.direction = 'right'
                root.manager.current = 'grade'

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        # --- HEADER INFO ---
        GridLayout:
            cols: 3
            size_hint: 1, 0.15
            
            # Info Kiri
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: root.level_text
                    font_size: '18sp'
                    color: 1, 1, 0, 1
                Label:
                    text: root.lives_text
                    font_size: '16sp'
                    color: 1, 0.3, 0.3, 1
                    bold: True

            # Info Tengah (Timer)
            Label:
                text: root.timer_text
                font_size: '35sp'
                bold: True
                color: (1, 0.2, 0.2, 1) if int(root.timer_text) <= 5 else (1, 1, 1, 1)

            # Info Kanan
            Label:
                text: root.score_text
                font_size: '18sp'
                color: 0, 1, 0.5, 1

        Label:
            text: root.status_text
            size_hint: 1, 0.05
            font_size: '14sp'
            color: 0.6, 0.6, 0.6, 1

        # --- SOAL ---
        Label:
            text: root.question_text
            font_size: '55sp'
            bold: True
            size_hint: 1, 0.35
            color: 1, 1, 1, 1

        # --- JAWABAN ---
        GridLayout:
            id: answer_grid
            cols: 2
            spacing: 15
            padding: [10, 0, 10, 10]
            size_hint: 1, 0.4

        # --- TOMBOL BAWAH ---
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1, 0.12

            RoundedButton:
                text: "SIMPAN & KELUAR"
                bg_color: 0.2, 0.6, 0.8, 1
                on_release: 
                    app.play_sound('click')
                    root.save_and_quit()

            RoundedButton:
                text: "BATAL / KELUAR"
                bg_color: 0.8, 0.2, 0.2, 1
                on_release: 
                    app.play_sound('click')
                    root.just_quit()
'''

# ---------- Helper Logging ----------
def write_local_log(msg):
    try:
        app = App.get_running_app()
        if app:
            data_dir = getattr(app, 'user_data_dir', None) or app.user_data_dir
        else:
            data_dir = os.path.expanduser('~')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        log_path = os.path.join(data_dir, 'app_debug.log')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass

# ---------- Custom Widgets ----------
class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.6, 1, 1])

# ---------- Screens ----------
class GradeScreen(Screen):
    def on_enter(self):
        # Setiap masuk layar ini, cek apakah ada Save Data
        self.check_save_data()

    def check_save_data(self):
        try:
            app = App.get_running_app()
            btn = self.ids.btn_resume
            
            if getattr(app, 'store', None) and app.store.exists('math_save'):
                data = app.store.get('math_save')
                # Tampilkan info save di tombol
                lvl = data.get('level', 1)
                scr = data.get('score', 0)
                mode = data.get('mode', 'tambah').upper()
                
                btn.text = f"LANJUT: {mode} (Level {lvl}) - Skor {scr}"
                btn.disabled = False
                btn.bg_color = (0.2, 0.7, 0.2, 1) # Hijau
            else:
                btn.text = "TIDAK ADA SAVE DATA"
                btn.disabled = True
                btn.bg_color = (0.3, 0.3, 0.3, 1) # Abu-abu
        except Exception as e:
            write_local_log(f"Error checking save: {e}")

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    level_text = StringProperty("Level: 1")
    lives_text = StringProperty("Nyawa: 3")
    timer_text = StringProperty("20")
    score_text = StringProperty("Skor: 0")
    status_text = StringProperty("Soal 1/10")
    question_text = StringProperty("Siap?")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        
        # State Variables
        self.level = 1
        self.total_score = 0
        self.question_num = 1
        self.lives = 3
        self.game_mode = 'tambah'
        
        self.time_left = 20
        self.correct_answer = 0
        self.timer_event = None
        self.game_active = False 
        Clock.schedule_once(self.setup_buttons)

    def setup_buttons(self, dt):
        if 'answer_grid' not in self.ids:
            Clock.schedule_once(self.setup_buttons, 0.1)
            return
        grid = self.ids.answer_grid
        grid.clear_widgets()
        self.buttons = []
        for _ in range(4):
            btn = RoundedButton(text="", font_size='30sp')
            btn.bind(on_release=self.check_answer_anim)
            self.buttons.append(btn)
            grid.add_widget(btn)

    # --- GAMEPLAY LOGIC ---

    def start_new_game(self, mode):
        """Memulai game baru dari awal"""
        self.game_mode = mode
        self.level = 1
        self.total_score = 0
        self.question_num = 1
        self.lives = 3
        self.start_round()

    def resume_game(self, data):
        """Melanjutkan game dari data save"""
        self.game_mode = data.get('mode', 'tambah')
        self.level = data.get('level', 1)
        self.total_score = data.get('score', 0)
        self.lives = data.get('lives', 3)
        self.question_num = data.get('question_num', 1)
        self.start_round()

    def start_round(self):
        # Update UI Awal
        self.update_ui_labels()
        self.next_question()

    def next_question(self):
        self.game_active = True
        if self.timer_event: self.timer_event.cancel()
        
        # Kesulitan Waktu
        base = 20
        reduction = min(12, (self.level - 1))
        self.time_left = base - reduction
        
        self.timer_text = str(self.time_left)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        
        self.update_ui_labels()
        self.generate_question()

    def update_ui_labels(self):
        self.level_text = f"Level: {self.level}"
        self.score_text = f"Skor: {self.total_score}"
        self.status_text = f"Soal {self.question_num}/10"
        self.lives_text = f"Nyawa: {self.lives}"

    def generate_question(self):
        app = App.get_running_app()
        grade = getattr(app, 'selected_grade', 3)
        diff = self.level
        
        # Logic Soal
        if self.game_mode == 'tambah':
            max_v = 15 + (10 * diff) + (grade*2)
            n1, n2 = random.randint(1, max_v), random.randint(1, max_v)
            ans, sym = n1 + n2, '+'
        elif self.game_mode == 'kurang':
            max_v = 20 + (10 * diff)
            a, b = random.randint(1, max_v), random.randint(1, max_v)
            n1, n2 = max(a,b), min(a,b)
            ans, sym = n1 - n2, '-'
        elif self.game_mode == 'kali':
            max_v = 4 + diff + (grade//2)
            n1, n2 = random.randint(2, max_v), random.randint(2, max_v)
            ans, sym = n1 * n2, 'x'
        elif self.game_mode == 'bagi':
            max_q = 3 + diff
            n2 = random.randint(2, 10 + grade)
            q = random.randint(2, max_q)
            n1, ans, sym = n2 * q, q, ':'
        else:
            n1, n2, ans, sym = 1, 1, 2, '+'

        self.correct_answer = ans
        self.question_text = f"{n1} {sym} {n2} = ?"

        # Jawaban Pengecoh
        answers = [ans]
        while len(answers) < 4:
            fake = ans + random.randint(-5, 5)
            if fake != ans and fake not in answers:
                if fake < 0 and grade < 5: fake = abs(fake)
                answers.append(fake)
        random.shuffle(answers)

        for i, btn in enumerate(self.buttons):
            btn.text = str(answers[i])
            btn.disabled = False
            btn.bg_color = (0.2, 0.6, 1, 1) # Reset Biru
            # Animasi Fade In
            anim = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.3)
            anim.start(btn)

    def update_timer(self, dt):
        if not self.game_active: return
        self.time_left -= 1
        self.timer_text = str(self.time_left)
        if self.time_left <= 0:
            self.check_answer_anim(None, timeout=True)

    def check_answer_anim(self, instance, timeout=False):
        if not self.game_active: return
        self.game_active = False 
        if self.timer_event: self.timer_event.cancel()

        # Animasi Pencet
        if instance:
            anim = Animation(size_hint=(0.45, 0.9), duration=0.05) + Animation(size_hint=(0.5, 1), duration=0.05)
            anim.start(instance)

        Clock.schedule_once(lambda dt: self._process_result(instance, timeout), 0.15)

    def _process_result(self, instance, timeout):
        app = App.get_running_app()
        correct = False
        
        # Cari tombol benar
        correct_btn = None
        for btn in self.buttons:
            if btn.text == str(self.correct_answer):
                correct_btn = btn

        if not timeout and instance:
            if int(instance.text) == self.correct_answer:
                correct = True
                self.total_score += 10
                app.play_sound('correct')
                self.animate_btn(instance, (0.2, 0.8, 0.2, 1)) # Hijau
            else:
                app.play_sound('wrong')
                self.animate_btn(instance, (0.8, 0.2, 0.2, 1)) # Merah
        else:
            app.play_sound('wrong') # Timeout

        if not correct:
            self.lives -= 1
            if correct_btn:
                self.animate_btn(correct_btn, (0.2, 0.8, 0.2, 1)) # Tunjukkan yg benar
            
            if self.lives <= 0:
                self.update_ui_labels()
                Clock.schedule_once(self.show_game_over, 1.0)
                return

        self.update_ui_labels()
        for btn in self.buttons: btn.disabled = True
        Clock.schedule_once(self.finish_step, 1.0)

    def animate_btn(self, btn, color):
        Animation(bg_color=color, duration=0.2).start(btn)

    def finish_step(self, dt):
        if self.lives <= 0: return

        if self.question_num >= 10:
            # Level Up - Auto Save
            self.question_num = 1
            self.level += 1
            self.save_data_internal() # Auto Save
            
            app = App.get_running_app()
            app.play_sound('win')
            self.show_level_complete()
        else:
            self.question_num += 1
            self.next_question()

    # --- SAVE & LOAD LOGIC ---

    def save_data_internal(self):
        """Fungsi internal untuk menyimpan ke JsonStore"""
        try:
            app = App.get_running_app()
            if getattr(app, 'store', None):
                app.store.put('math_save',
                              grade=app.selected_grade,
                              level=self.level,
                              score=self.total_score,
                              lives=self.lives,
                              question_num=self.question_num,
                              mode=self.game_mode)
                write_local_log("Game Saved Successfully")
        except Exception as e:
            write_local_log(f"Save Error: {e}")

    def save_and_quit(self):
        """Dipanggil tombol Simpan & Keluar"""
        if self.timer_event: self.timer_event.cancel()
        self.save_data_internal()
        # Tampilkan popup sebentar lalu keluar
        popup = Popup(title='Disimpan!', 
                      content=Label(text='Progres Anda aman.\nKembali ke menu utama...', font_size='18sp'),
                      size_hint=(0.6, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: self.exit_to_menu(popup), 1.5)

    def just_quit(self):
        """Keluar tanpa menyimpan (progress level ini hilang)"""
        if self.timer_event: self.timer_event.cancel()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

    def exit_to_menu(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

    # --- POPUPS ---

    def show_level_complete(self):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl = Label(text=f"LEVEL {self.level-1} SELESAI!", font_size='22sp', bold=True, color=(0,1,0,1))
        content.add_widget(lbl)
        
        btn = RoundedButton(text="LANJUT LEVEL BERIKUTNYA", bg_color=(0, 0.6, 0, 1))
        btn.bind(on_release=lambda x: self.next_level_action(popup))
        content.add_widget(btn)
        
        popup = Popup(title="HEBAT!", content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
        popup.open()

    def next_level_action(self, popup):
        popup.dismiss()
        self.lives = 3 # Reset nyawa setiap level baru (opsional, biar seru reset aja)
        self.start_round()

    def show_game_over(self, dt):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(text="GAME OVER", font_size='28sp', bold=True, color=(1,0,0,1)))
        content.add_widget(Label(text="Nyawa habis!", font_size='18sp'))
        
        # Tombol Ulang
        btn_retry = RoundedButton(text="ULANGI LEVEL", bg_color=(0.2, 0.6, 1, 1))
        btn_retry.bind(on_release=lambda x: self.retry_action(popup))
        content.add_widget(btn_retry)

        # Tombol Keluar
        btn_exit = RoundedButton(text="KELUAR MENU", bg_color=(0.5, 0.2, 0.2, 1))
        btn_exit.bind(on_release=lambda x: self.exit_game_over(popup))
        content.add_widget(btn_exit)

        popup = Popup(title="", content=content, size_hint=(0.8, 0.6), auto_dismiss=False)
        popup.open()

    def retry_action(self, popup):
        popup.dismiss()
        self.lives = 3
        self.question_num = 1
        self.start_round()

    def exit_game_over(self, popup):
        popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'grade'

# ---------- App ----------
class MathApp(App):
    selected_grade = NumericProperty(3)
    grade_title = StringProperty("Kelas 3 SD")
    store = None
    sounds = {}

    def build(self):
        try:
            data_dir = self.user_data_dir
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            # JsonStore untuk menyimpan data
            self.store = JsonStore(os.path.join(data_dir, 'math_save.json'))
        except Exception:
            self.store = None
        
        self.load_sounds()
        return Builder.load_string(kv_string)

    def load_sounds(self):
        files = {'click': 'click.wav', 'correct': 'correct.wav', 'wrong': 'wrong.wav', 'win': 'win.wav'}
        for k, v in files.items():
            try:
                snd = SoundLoader.load(v)
                if snd: self.sounds[k] = snd
            except: pass

    def play_sound(self, name):
        if name in self.sounds and self.sounds[name]:
            try: 
                if self.sounds[name].state == 'play': self.sounds[name].stop()
                self.sounds[name].play()
            except: pass

    def set_grade(self, grade):
        self.selected_grade = grade
        titles = {3: "Kelas 3 SD", 5: "Kelas 5 SD", 8: "Kelas 8 SMP"}
        self.grade_title = titles.get(grade, "")

    def load_last_game(self):
        """Fungsi dipanggil tombol Load di Menu Awal"""
        if self.store and self.store.exists('math_save'):
            data = self.store.get('math_save')
            
            # Set Grade dulu
            self.set_grade(data.get('grade', 3))
            
            # Pindah screen
            self.root.transition.direction = 'left'
            self.root.current = 'game'
            
            # Load data ke GameScreen
            game_screen = self.root.get_screen('game')
            game_screen.resume_game(data)

if __name__ == '__main__':
    try:
        MathApp().run()
    except Exception:
        pass
