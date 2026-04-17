import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class ProfessionalTimer:
    def __init__(self, root):
        self.root = root
        
        # 설정 초기값
        self.remaining = 600
        self.bg_alpha = 0.8
        self.font_size = 45
        self.font_color = "#FFFFFF"
        self.running = True

        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.bg_alpha)
        self.root.config(bg="black")

        # 숫자 라벨 (전체 창)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg="black", cursor="fleur", padx=15, pady=10)
        self.label.pack()

        # 마우스 이벤트
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        
        # 우클릭 시 설정창(Toplevel) 띄우기
        self.label.bind("<Button-3>", self.show_settings)

        self.update_timer()

    def show_settings(self, event):
        # 이미 설정창이 열려있으면 닫기
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.title("Settings")
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=10, pady=10)
        
        # 테두리 없는 미니 설정창
        self.settings.overrideredirect(True)

        # 1. 투명도 슬라이더
        tk.Label(self.settings, text="배경 투명도", bg="#222", fg="white", font=("Arial", 9)).pack()
        alpha_scale = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05,
                               orient="horizontal", command=self.update_alpha,
                               bg="#222", fg="white", highlightthickness=0)
        alpha_scale.set(self.bg_alpha)
        alpha_scale.pack(fill="x", pady=(0, 10))

        # 2. 글자 크기 슬라이더
        tk.Label(self.settings, text="글자 크기", bg="#222", fg="white", font=("Arial", 9)).pack()
        size_scale = tk.Scale(self.settings, from_=20, to=200, resolution=1,
                              orient="horizontal", command=self.update_font_size,
                              bg="#222", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 3. 기타 버튼들
        btn_frame = tk.Frame(self.settings, bg="#222")
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="🎨 색상", command=self.choose_color, bg="#444", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="⏱️ 시간", command=self.ask_time, bg="#444", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="닫기 / 종료", command=self.root.destroy, bg="red", fg="white", bd=0).pack(fill="x", pady=(10, 0))

        # 설정창 바깥 클릭 시 닫기
        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def update_alpha(self, val):
        self.bg_alpha = float(val)
        self.root.attributes("-alpha", self.bg_alpha)

    def update_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))

    def choose_color(self):
        color = colorchooser.askcolor(title="글자 색상 선택", color=self.font_color)[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time(self):
        input_time = simpledialog.askstring("시간 설정", "HH:MM:SS", initialvalue="00:10:00")
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
            self.label.config(text=f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Timer")
    app = ProfessionalTimer(root)
    root.mainloop()
