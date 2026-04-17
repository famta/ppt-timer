import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class YoutubeStyleTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.font_size = 60
        self.font_color = "#FFFFFF" 
        self.fg_alpha = 1.0    # 글자 투명도 (0.1 ~ 1.0)
        self.running = True
        self.time_str = "00:10:00"

        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정 (배경 제거 및 투명도 활성화)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 배경색을 특정 색으로 지정하고 그 색만 투명하게 뚫음
        self.transparent_key = '#abcdef' 
        self.root.config(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)
        
        # 3. 레이아웃 (Stack 구조: 아이콘이 숫자 위에 겹침)
        self.container = tk.Frame(self.root, bg=self.transparent_key)
        self.container.pack(expand=True, fill='both')

        # 타이머 숫자 라벨
        self.label = tk.Label(self.container, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.transparent_key, cursor="fleur")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # 일시정지 아이콘 라벨 (유튜브 스타일 - 숫자 위에 겹침)
        self.pause_icon = tk.Label(self.container, text="||", font=("Helvetica", int(self.font_size*1.2), "bold"), 
                                   fg="white", bg=self.transparent_key)
        # 처음에는 숨김
        self.pause_icon.place_forget()

        # 이벤트 바인딩
        for widget in [self.label, self.container, self.pause_icon]:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)
            widget.bind("<Double-Button-1>", self.toggle_timer)
            widget.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.apply_alpha()

    def apply_alpha(self):
        """진짜 글자 투명도 적용 (윈도우 전체 투명도 제어)"""
        # 배경은 어차피 transparent_key로 뚫려있으므로, alpha를 조절하면 글자만 투명해집니다.
        self.root.attributes("-alpha", self.fg_alpha)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=15, pady=15, highlightbackground="#444", highlightthickness=1)
        
        # 헤더
        title_f = tk.Frame(self.settings, bg="#222")
        title_f.pack(fill="x", pady=(0, 10))
        tk.Label(title_f, text="TIMER SETTINGS", bg="#222", fg="#aaa", font=("Arial", 8, "bold")).pack(side="left")
        tk.Button(title_f, text="✕", command=self.settings.destroy, bg="#222", fg="white", bd=0).pack(side="right")

        # 1. 글자 투명도 (T2) - 이제 제대로 작동합니다
        tk.Label(self.settings, text="글자 투명도 (T2)", bg="#222", fg="white", font=("Arial", 9)).pack(anchor="w")
        fg_sc = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                         command=self.set_fg_alpha, bg="#222", fg="white", highlightthickness=0)
        fg_sc.set(self.fg_alpha)
        fg_sc.pack(fill="x", pady=(0, 10))

        # 2. 글자 크기
        tk.Label(self.settings, text="글자 크기", bg="#222", fg="white", font=("Arial", 9)).pack(anchor="w")
        sz_sc = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                         command=self.set_font_size, bg="#222", fg="white", highlightthickness=0)
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=(0, 15))

        # 버튼들
        tk.Button(self.settings, text="🎨 색상 변경", command=self.choose_color, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ 시간 설정", command=self.ask_time, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="❌ 종료", command=self.exit_app, bg="#d32f2f", fg="white", bd=0, pady=7).pack(fill="x", pady=10)

        self.settings.focus_set()
        self.settings.bind("<FocusOut>", lambda e: self.settings.after(100, self.settings.destroy))

    def set_fg_alpha(self, val):
        self.fg_alpha = float(val)
        self.apply_alpha()

    def set_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))
        self.pause_icon.config(font=("Helvetica", int(self.font_size*1.2), "bold"))
        # 창 크기를 글자 크기에 맞춰 넉넉하게 조정
        self.root.geometry(f"{int(self.font_size*5)}x{int(self.font_size*2)}")

    def choose_color(self):
        color = colorchooser.askcolor(title="Select Color", color=self.font_color)[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time(self):
        input_time = simpledialog.askstring("Timer", "HH:MM:SS", initialvalue="00:10:00")
        if input_time:
            try:
                h, m, s = map(int, input_time.split(':'))
                self.remaining = h * 3600 + m * 60 + s
                return True
            except: return False
        return False

    def exit_app(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()

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
            self.label.config(text=self.time_str)
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running:
            self.pause_icon.place_forget() # 아이콘 숨김
            self.update_timer()
        else:
            self.pause_icon.place(relx=0.5, rely=0.5, anchor="center") # 숫자 위에 겹치기
            # 일시정지 아이콘도 글자 투명도와 비슷하게 약간 반투명하게 설정 가능
            self.pause_icon.config(fg="white") 

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeStyleTimer(root)
    root.mainloop()
