import tkinter as tk
from tkinter import simpledialog, colorchooser

class TransparentTimer:
    def __init__(self, root):
        self.root = root
        
        # 설정 초기값
        self.remaining = 600
        self.bg_alpha = 0.8  # 배경 투명도 (0.0 ~ 1.0)
        self.fg_alpha = 1.0  # 글자 투명도 (0.0 ~ 1.0)
        self.font_size = 45
        self.font_color = (255, 255, 255) # RGB 튜플 (흰색)
        self.running = True

        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 캔버스 생성 (글자와 배경을 자유롭게 그리기 위함)
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.toggle_timer)
        self.canvas.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.refresh_ui()

    def refresh_ui(self):
        """배경과 글자 투명도를 각각 적용하여 화면 갱신"""
        # 1. 창 전체 투명도 (배경 제어)
        self.root.attributes("-alpha", self.bg_alpha)
        
        # 2. 글자 투명도 조절
        # Tkinter 캔버스 자체는 글자 투명도를 지원하지 않으므로 
        # 글자 색상을 배경색(Black)과 섞어서 반투명 효과를 시뮬레이션합니다.
        r = int(self.font_color[0] * self.fg_alpha)
        g = int(self.font_color[1] * self.fg_alpha)
        b = int(self.font_color[2] * self.fg_alpha)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width()/2 if self.canvas.winfo_width() > 1 else 50,
            self.canvas.winfo_height()/2 if self.canvas.winfo_height() > 1 else 30,
            text=self.time_str,
            font=("Helvetica", self.font_size, "bold"),
            fill=hex_color,
            tags="timer_text"
        )

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#333", padx=12, pady=12)
        
        # 배경 투명도 (T1)
        tk.Label(self.settings, text="배경 투명도 (창 전체)", bg="#333", fg="white", font=("Arial", 9)).pack()
        bg_scale = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                            command=self.update_bg_alpha, bg="#333", fg="white", highlightthickness=0)
        bg_scale.set(self.bg_alpha)
        bg_scale.pack(fill="x", pady=(0, 10))

        # 글자 투명도 (T2)
        tk.Label(self.settings, text="글자 투명도 (색상 투과)", bg="#333", fg="white", font=("Arial", 9)).pack()
        fg_scale = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                            command=self.update_fg_alpha, bg="#333", fg="white", highlightthickness=0)
        fg_scale.set(self.fg_alpha)
        fg_scale.pack(fill="x", pady=(0, 10))

        # 글자 크기
        tk.Label(self.settings, text="글자 크기", bg="#333", fg="white", font=("Arial", 9)).pack()
        size_scale = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                              command=self.update_font_size, bg="#333", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 버튼들
        tk.Button(self.settings, text="🎨 색상 변경", command=self.choose_color, bg="#555", fg="white", bd=0).pack(fill="x", pady=2)
        tk.Button(self.settings, text="설정 닫기", command=self.settings.destroy, bg="#777", fg="white", bd=0).pack(fill="x", pady=2)
        tk.Button(self.settings, text="프로그램 종료", command=self.root.destroy, bg="#d32f2f", fg="white", bd=0).pack(fill="x", pady=5)

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def update_bg_alpha(self, val):
        self.bg_alpha = float(val)
        self.refresh_ui()

    def update_fg_alpha(self, val):
        self.fg_alpha = float(val)
        self.refresh_ui()

    def update_font_size(self, val):
        self.font_size = int(val)
        # 캔버스 크기를 폰트 크기에 맞춰 조정
        self.root.geometry(f"{int(self.font_size*4.5)}x{int(self.font_size*1.8)}")
        self.refresh_ui()

    def choose_color(self):
        color = colorchooser.askcolor(title="글자 색상")[0] # RGB 튜플 가져오기
        if color:
            self.font_color = color
            self.refresh_ui()

    def ask_time(self):
        input_time = simpledialog.askstring("설정", "HH:MM:SS", initialvalue="00:10:00")
        if input_time:
            try:
                h, m, s = map(int, input_time.split(':'))
                self.remaining = h * 3600 + m * 60 + s
            except: pass

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def update_timer(self):
        if self.running and self.remaining >= 0:
            h, rem = divmod(self.remaining, 3600)
            m, s = divmod(rem, 60)
            self.time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            self.refresh_ui()
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TransparentTimer(tk.Toplevel(root))
    root.mainloop()
