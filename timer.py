import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class PerfectBlueTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 제어 변수
        self.after_id = None
        self.initial_seconds = 600 
        self.remaining = 600
        self.font_size = 60
        self.font_color = "#0000FF" 
        self.fg_alpha = 1.0  # 초기 투명도 100%
        self.running = True
        self.time_str = "00:10:00"

        self.root.withdraw()
        self.ask_time()
        self.root.deiconify()

        # 2. 윈도우 설정
        self.root.title("Blue Timer")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        self.transparent_key = '#abcdef' 
        self.root.config(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)
        
        # 작업 표시줄 아이콘 표시 (윈도우 전용)
        self.root.after(10, lambda: self.set_appwindow(self.root))

        # 3. 레이아웃
        self.main_frame = tk.Frame(self.root, bg=self.transparent_key)
        self.main_frame.pack(expand=True, fill='both')

        self.label = tk.Label(self.main_frame, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.transparent_key)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.pause_icon = tk.Label(self.main_frame, text="||", font=("Helvetica", int(self.font_size*1.5), "bold"), 
                                   fg="white", bg=self.transparent_key)
        self.pause_icon.place_forget()

        # 이벤트 바인딩
        for w in [self.label, self.main_frame, self.pause_icon]:
            w.bind("<ButtonPress-1>", self.start_move)
            w.bind("<B1-Motion>", self.do_move)
            w.bind("<Double-Button-1>", self.toggle_timer)
            w.bind("<Button-3>", self.show_settings)

        self.start_timer_loop()
        self.apply_alpha() # 초기 투명도 적용
        self.resize_window()

    def set_appwindow(self, root):
        import ctypes
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        style = (style & ~0x00000080) | 0x00040000
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
        root.withdraw()
        root.after(10, root.deiconify)

    def apply_alpha(self):
        """실제 글자 투명도 조절 (윈도우 알파값 제어)"""
        self.root.attributes("-alpha", self.fg_alpha)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            return 

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#1a1a1a", padx=15, pady=15, highlightbackground="#444", highlightthickness=2)
        
        header = tk.Frame(self.settings, bg="#1a1a1a")
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="TIMER SETTINGS", bg="#1a1a1a", fg="white", font=("Arial", 9, "bold")).pack(side="left")
        tk.Button(header, text="✕", command=self.settings.destroy, bg="#1a1a1a", fg="white", bd=0, padx=5).pack(side="right")

        # [복구] 투명도 슬라이더 - command를 확실히 연결
        tk.Label(self.settings, text="글자 투명도 (T2)", bg="#1a1a1a", fg="#aaa", font=("Arial", 8)).pack(anchor="w")
        sc_alpha = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                            command=self.set_fg_alpha, bg="#1a1a1a", fg="white", highlightthickness=0)
        sc_alpha.set(self.fg_alpha)
        sc_alpha.pack(fill="x", pady=(0, 10))

        # 크기 슬라이더
        tk.Label(self.settings, text="글자 크기", bg="#1a1a1a", fg="#aaa", font=("Arial", 8)).pack(anchor="w")
        sc_size = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                           command=self.set_font_size, bg="#1a1a1a", fg="white", highlightthickness=0)
        sc_size.set(self.font_size)
        sc_size.pack(fill="x", pady=(0, 15))

        # 버튼들
        tk.Button(self.settings, text="🔄 시간 초기화 (Reset)", command=self.reset_timer, bg="#0056b3", fg="white", bd=0, pady=8).pack(fill="x", pady=(5, 2))
        tk.Button(self.settings, text="🎨 색상 변경", command=self.choose_color, bg="#333", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ 시간 재설정", command=self.ask_time, bg="#333", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="🛑 프로그램 종료", command=self.exit_app, bg="#8b0000", fg="white", bd=0, pady=7).pack(fill="x", pady=(10, 0))

    def set_fg_alpha(self, val):
        """슬라이더에서 값을 받아 즉시 반영"""
        self.fg_alpha = float(val)
        self.apply_alpha()

    def set_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))
        self.pause_icon.config(font=("Helvetica", int(self.font_size*1.5), "bold"))
        self.resize_window()

    def reset_timer(self):
        self.remaining = self.initial_seconds
        self.update_display()
        if self.running:
            self.start_timer_loop()
        if hasattr(self, 'settings'):
            self.settings.destroy()

    def resize_window(self):
        text = self.label.cget("text")
        char_count = len(text)
        new_width = int(self.font_size * char_count * 0.8)
        new_height = int(self.font_size * 2.0)
        self.root.geometry(f"{new_width}x{new_height}")

    def choose_color(self):
        color = colorchooser.askcolor(title="글자색", color=self.font_color)[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time(self):
        ans = simpledialog.askstring("Timer", "HH:MM:SS", initialvalue=self.time_str)
        if ans:
            try:
                parts = list(map(int, ans.split(':')))
                if len(parts) == 3:
                    self.remaining = parts[0] * 3600 + parts[1] * 60 + parts[2]
                elif len(parts) == 2:
                    self.remaining = parts[0] * 60 + parts[1]
                self.initial_seconds = self.remaining
                self.update_display()
                if self.running: self.start_timer_loop()
            except: pass

    def exit_app(self):
        if self.after_id: self.root.after_cancel(self.after_id)
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def start_move(self, event): self.x, self.y = event.x, event.y
    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def update_display(self):
        h, rem = divmod(max(0, self.remaining), 3600)
        m, s = divmod(rem, 60)
        self.time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
        self.label.config(text=self.time_str)
        self.resize_window()

    def start_timer_loop(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.update_timer()

    def update_timer(self):
        if self.running and self.remaining >= 0:
            self.update_display()
            self.remaining -= 1
            self.after_id = self.root.after(1000, self.update_timer)
        else:
            self.after_id = None

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running:
            self.pause_icon.place_forget()
            self.start_timer_loop()
        else:
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.pause_icon.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerfectBlueTimer(root)
    root.mainloop()
