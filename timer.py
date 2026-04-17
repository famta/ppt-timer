import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class TextOnlyTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.font_size = 60
        self.font_color = "#FFFFFF" 
        self.running = True
        self.time_str = "00:10:00"

        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정 (배경 완전 투명화)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 배경을 특정 색으로 칠하고 그 색만 투명하게 뚫음
        self.transparent_key = '#abcdef' 
        self.root.config(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)

        # 3. 타이머 라벨
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.transparent_key, cursor="fleur")
        self.label.pack(expand=True, fill='both')

        # 마우스 이벤트
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_settings)

        self.update_timer()

    def show_settings(self, event):
        """우클릭 시 설정창 노출"""
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        # 마우스 커서 위치에 설정창 배치
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=15, pady=15, highlightbackground="#444", highlightthickness=1)
        
        # --- 설정 UI 구성 ---
        title_frame = tk.Frame(self.settings, bg="#222")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="SETTINGS", bg="#222", fg="#aaa", font=("Arial", 8, "bold")).pack(side="left")
        
        # [X] 닫기 버튼 (명확하게 추가)
        close_btn = tk.Button(title_frame, text="✕", command=self.settings.destroy, 
                              bg="#222", fg="white", bd=0, cursor="hand2", activebackground="#444", activeforeground="red")
        close_btn.pack(side="right")

        # 글자 크기 슬라이더
        tk.Label(self.settings, text="Font Size", bg="#222", fg="white", font=("Arial", 9)).pack(anchor="w")
        sz_sc = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                         command=self.set_font_size, bg="#222", fg="white", highlightthickness=0, troughcolor="#444")
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=(0, 15))

        # 기능 버튼들
        tk.Button(self.settings, text="🎨 Change Color", command=self.choose_color, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ Set Time", command=self.ask_time, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        
        # 구분선
        tk.Frame(self.settings, height=1, bg="#444").pack(fill="x", pady=10)
        
        # 프로그램 완전 종료 버튼
        tk.Button(self.settings, text="EXIT PROGRAM", command=self.exit_app, bg="#d32f2f", fg="white", bd=0, pady=7, font=("Arial", 9, "bold")).pack(fill="x")

        # [중요] 포커스를 설정창으로 강제 이동시켜 바깥 클릭 시 잘 닫히게 함
        self.settings.focus_set()
        self.settings.bind("<FocusOut>", lambda e: self.settings.after(100, self.settings.destroy))

    def set_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))

    def choose_color(self):
        color = colorchooser.askcolor(title="Select Color")[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time(self):
        input_time = simpledialog.askstring("Timer", "Enter Time (HH:MM:SS)", initialvalue="00:10:00")
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
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextOnlyTimer(root)
    root.mainloop()
