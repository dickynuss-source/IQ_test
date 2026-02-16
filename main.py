import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.button import Button

# Warna Background (Ungu Gelap Misterius)
Window.clearcolor = (0.15, 0.1, 0.2, 1)

kv_string = '''
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

<RoundedButton@Button>:
    background_color: 0,0,0,0
    bg_color: 0.3, 0.2, 0.5, 1
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
    MenuScreen:
    QuizScreen:
    ResultScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20

        Label:
            text: "IQ TEST PRO"
            font_size: '45sp'
            bold: True
            color: 0.2, 0.9, 1, 1
            size_hint: 1, 0.4

        Label:
            text: "Uji Logika & Kecepatan Berpikir"
            font_size: '16sp'
            color: 0.7, 0.7, 0.7, 1
            size_hint: 1, 0.1

        RoundedButton:
            text: "LATIHAN (Santai)"
            bg_color: 0.2, 0.6, 0.4, 1
            on_release: 
                app.start_quiz(mode='latihan')
                root.manager.transition.direction = 'left'
                root.manager.current = 'quiz'

        RoundedButton:
            text: "MULAI TEST IQ (Waktu Terbatas)"
            bg_color: 0.8, 0.3, 0.2, 1
            on_release: 
                app.start_quiz(mode='test')
                root.manager.transition.direction = 'left'
                root.manager.current = 'quiz'

<QuizScreen>:
    name: 'quiz'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15

        # Header Info
        GridLayout:
            cols: 2
            size_hint: 1, 0.1
            Label:
                text: root.progress_text
                color: 1, 1, 0, 1
                halign: 'left'
            Label:
                text: root.timer_text
                font_size: '20sp'
                bold: True
                color: (1, 0.2, 0.2, 1) if root.is_warning else (1, 1, 1, 1)

        # Soal
        Label:
            text: root.question_text
            font_size: '28sp'
            bold: True
            size_hint: 1, 0.35
            text_size: self.width, None
            halign: 'center'
            valign: 'middle'

        # Pilihan Jawaban
        GridLayout:
            id: options_grid
            cols: 2
            spacing: 15
            size_hint: 1, 0.45

        RoundedButton:
            text: "Keluar"
            size_hint: 1, 0.1
            bg_color: 0.3, 0.3, 0.3, 1
            on_release: app.stop_quiz()

<ResultScreen>:
    name: 'result'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20

        Label:
            text: "HASIL TEST"
            font_size: '30sp'
            bold: True
            color: 1, 1, 1, 1
            size_hint: 1, 0.2

        Label:
            text: root.score_text
            font_size: '22sp'
            color: 0.5, 1, 0.5, 1
            size_hint: 1, 0.1

        Label:
            text: root.iq_score
            font_size: '60sp'
            bold: True
            color: 0.2, 0.9, 1, 1
            size_hint: 1, 0.3

        Label:
            text: root.feedback_text
            font_size: '16sp'
            color: 0.8, 0.8, 0.8, 1
            text_size: self.width, None
            halign: 'center'
            size_hint: 1, 0.2

        RoundedButton:
            text: "KEMBALI KE MENU"
            bg_color: 0.2, 0.5, 0.8, 1
            size_hint: 1, 0.2
            on_release: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
'''

class QuizScreen(Screen):
    question_text = StringProperty("Loading...")
    timer_text = StringProperty("00:00")
    progress_text = StringProperty("Soal 1")
    is_warning = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        Clock.schedule_once(self.setup_ui)

    def setup_ui(self, dt):
        grid = self.ids.options_grid
        for i in range(4):
            btn = Button(background_normal='', background_color=(0.3, 0.2, 0.5, 1))
            btn.bind(on_release=self.answer_clicked)
            self.buttons.append(btn)
            grid.add_widget(btn)

    def answer_clicked(self, instance):
        app = App.get_running_app()
        app.check_answer(instance.text)

class ResultScreen(Screen):
    score_text = StringProperty("")
    iq_score = StringProperty("")
    feedback_text = StringProperty("")

class MenuScreen(Screen):
    pass

class IQApp(App):
    mode = 'latihan'
    current_question = 0
    score = 0
    total_questions = 0
    time_left = 0
    timer_event = None
    
    # Database Statis (Logika & Verbal)
    static_questions = [
        {"q": "Lawan kata 'BESAR'?", "a": "Kecil", "opts": ["Luas", "Panjang", "Kecil", "Raksasa"]},
        {"q": "Lawan kata 'ABADI'?", "a": "Sementara", "opts": ["Kekal", "Sementara", "Lama", "Tetap"]},
        {"q": "Mobil : Bensin = Manusia : ...?", "a": "Makanan", "opts": ["Darah", "Makanan", "Kaki", "Rumah"]},
        {"q": "Apa warna bendera Indonesia?", "a": "Merah Putih", "opts": ["Merah Biru", "Merah Putih", "Putih Merah", "Merah Kuning"]},
        {"q": "Ibu kota Indonesia saat ini (2024)?", "a": "Jakarta", "opts": ["Bandung", "Surabaya", "Jakarta", "Medan"]},
        {"q": "Ayam berkokok, Anjing ...?", "a": "Menggonggong", "opts": ["Mengaum", "Mengeong", "Menggonggong", "Meringkik"]},
        {"q": "Es : Dingin = Api : ...?", "a": "Panas", "opts": ["Merah", "Panas", "Terang", "Asap"]},
        {"q": "Manakah yang bukan mamalia?", "a": "Ayam", "opts": ["Kucing", "Paus", "Ayam", "Kelelawar"]},
        {"q": "Lengkapi: Senin, Selasa, Rabu, ...?", "a": "Kamis", "opts": ["Jumat", "Minggu", "Kamis", "Sabtu"]},
        {"q": "Jika kemarin Hari Jumat, besok hari apa?", "a": "Minggu", "opts": ["Sabtu", "Minggu", "Senin", "Selasa"]}
    ]

    def build(self):
        return Builder.load_string(kv_string)

    # --- GENERATOR SOAL OTOMATIS (AGAR SOAL JADI RIBUAN/TAK TERBATAS) ---
    def generate_question(self):
        # Acak tipe soal: 40% Math, 40% Pattern, 20% Logic
        tipe = random.choice(['math', 'math', 'pattern', 'pattern', 'logic'])

        if tipe == 'math':
            op = random.choice(['+', '-', 'x', ':'])
            if op == '+':
                a, b = random.randint(10, 99), random.randint(10, 99)
                ans = a + b
                q_str = f"{a} + {b} = ?"
            elif op == '-':
                a, b = random.randint(20, 150), random.randint(10, 99)
                ans = a - b
                q_str = f"{a} - {b} = ?"
            elif op == 'x':
                a, b = random.randint(5, 15), random.randint(2, 12)
                ans = a * b
                q_str = f"{a} x {b} = ?"
            else: # Bagi
                b = random.randint(2, 12)
                ans = random.randint(2, 20)
                a = b * ans
                q_str = f"{a} : {b} = ?"
            
            # Buat pilihan ganda
            options = {ans}
            while len(options) < 4:
                fake = ans + random.randint(-10, 10)
                if fake != ans and fake >= 0:
                    options.add(fake)
            
            return q_str, str(ans), list(map(str, options))

        elif tipe == 'pattern':
            start = random.randint(1, 50)
            step = random.randint(2, 10)
            mode = random.choice(['+', '-', 'fib'])
            
            if mode == '+':
                seq = [start, start+step, start+(step*2), "?"]
                ans = start + (step*3)
            elif mode == '-':
                start = random.randint(50, 100)
                seq = [start, start-step, start-(step*2), "?"]
                ans = start - (step*3)
            else: # Fibonacci sederhana
                a, b = 1, 1
                seq = [1, 1, 2, 3, 5, "?"]
                ans = 8
            
            q_str = f"Pola: {seq[0]}, {seq[1]}, {seq[2]}, ...?"
            
            options = {ans}
            while len(options) < 4:
                fake = ans + random.randint(-5, 5)
                if fake != ans:
                    options.add(fake)
            
            return q_str, str(ans), list(map(str, options))

        else: # Logic dari database
            item = random.choice(self.static_questions)
            return item['q'], item['a'], item['opts']

    # --- LOGIKA GAME ---
    def start_quiz(self, mode='latihan'):
        self.mode = mode
        self.score = 0
        self.current_question = 0
        
        if mode == 'latihan':
            self.total_questions = 10
            self.time_left = 0 # No timer
        else:
            self.total_questions = 30 # IQ Test biasanya panjang
            self.time_left = 300 # 5 menit total
            self.start_timer()

        self.next_question()

    def start_timer(self):
        if self.timer_event: self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        m, s = divmod(self.time_left, 60)
        
        screen = self.root.get_screen('quiz')
        screen.timer_text = f"{m:02d}:{s:02d}"
        
        # Warna merah jika < 30 detik
        screen.is_warning = (self.time_left < 30)

        if self.time_left <= 0:
            self.finish_quiz()

    def next_question(self):
        self.current_question += 1
        if self.current_question > self.total_questions:
            self.finish_quiz()
            return

        q_text, ans, opts = self.generate_question()
        self.current_correct_answer = str(ans)
        
        # Acak posisi pilihan
        random.shuffle(opts)

        screen = self.root.get_screen('quiz')
        screen.progress_text = f"Soal {self.current_question}/{self.total_questions}"
        screen.question_text = q_text
        
        # Update tombol
        for i, btn in enumerate(screen.buttons):
            btn.text = str(opts[i])
            btn.background_color = (0.3, 0.2, 0.5, 1) # Reset warna
            btn.disabled = False

    def check_answer(self, user_ans):
        if str(user_ans) == self.current_correct_answer:
            self.score += 1
        
        # Lanjut soal berikutnya (bisa dikasih delay jika mau animasi)
        self.next_question()

    def finish_quiz(self):
        if self.timer_event: self.timer_event.cancel()
        
        screen = self.root.get_screen('result')
        
        # Hitung IQ Mockup (Rumus sederhana)
        # Asumsi: Jika benar semua (30 soal) = IQ 160+
        # Jika benar 50% (15 soal) = IQ 100 (Rata-rata)
        if self.total_questions > 0:
            ratio = self.score / self.total_questions
            iq_val = int(70 + (ratio * 90)) # Range IQ 70 - 160
        else:
            iq_val = 0

        screen.score_text = f"Benar {self.score} dari {self.total_questions}"
        
        if self.mode == 'latihan':
            screen.iq_score = "LATIHAN"
            screen.feedback_text = "Bagus! Terus berlatih untuk menajamkan logika."
        else:
            screen.iq_score = f"IQ: {iq_val}"
            if iq_val > 130:
                screen.feedback_text = "Luar Biasa! Logika Anda sangat tajam (Genius)."
            elif iq_val > 110:
                screen.feedback_text = "Hebat! Kecerdasan di atas rata-rata."
            elif iq_val > 90:
                screen.feedback_text = "Bagus. Kecerdasan rata-rata normal."
            else:
                screen.feedback_text = "Perlu lebih banyak latihan lagi."

        self.root.transition.direction = 'left'
        self.root.current = 'result'

    def stop_quiz(self):
        if self.timer_event: self.timer_event.cancel()
        self.root.transition.direction = 'right'
        self.root.current = 'menu'

if __name__ == '__main__':
    IQApp().run()
