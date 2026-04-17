import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class BlueTextTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.font_size = 60
        self.font_color = "#0000FF"  # [변경] 기본 색상을 Blue(#0000FF)로 설정
        self.fg_alpha = 1.0
        self.running = True
        self.time_str = "00:10:00"

        # 시작 전 시간 설정
        self.ask_time_initial()

        # 2. 윈도우 설정
        self.root.title("Timer")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 배경 제거 로직
        self.transparent_key = '#abcdef' 
        self.root.config(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)
        
        # 작업 표시줄 아이콘 활성화
        self.root.after(10, lambda: self.set_appwindow(self.root))

        # 3. 레이아웃
        self.container = tk.Frame(self.root, bg=self.transparent_key)
        self.container.pack(expand=True, fill='both')

        # 타이머 숫자 (기본 파란색)
        self.label = tk.Label(self.container, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.transparent_key, cursor="fleur")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # 일시정지 아이콘 (숫자 정중앙에 겹침)
        self.pause_icon = tk.Label(self.container, text="||", font=("Helvetica", int(self.font_size*1.2), "bold"), 
                                   fg="white", bg=self.transparent_key)
        self.pause_icon.place_forget()

        # 마우스 이벤트 바인딩
        for w in [self.label, self.container, self.pause_icon]:
            w.bind("<ButtonPress-1>", self.start_move)
            w.bind("<B1-Motion>", self.do_move)
            w.bind("<Double-Button-1>", self.toggle_timer)
            w.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.apply_alpha()
        self.set_font_size(self.font_size)

    def set_appwindow(self, root):
        import ctypes
        gwl_exstyle = -20
        ws_ex_appwindow = 0x00040000
        ws_ex_toolwindow = 0x00000080
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, gwl_exstyle)
        style = style & ~ws_ex_toolwindow
        style = style | ws_ex_appwindow
        ctypes.windll.user32.SetWindowLongW(hwnd, gwl_exstyle, style)
        root.withdraw()
        root.after(10, root.deiconify)

    def apply_alpha(self):
        """글자 투명도 조절"""
        self.root.attributes("-alpha", self.fg_alpha)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            return 

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=15, pady=15, highlightbackground="#545454", highlightthickness=2)
        
        title_f = tk.Frame(self.settings, bg="#222")
        title_f.pack(fill="x", pady=(0, 10))
        tk.Label(title_f, text="TIMER SETTINGS", bg="#222", fg="white", font=("Arial", 9, "bold")).pack(side="left")
        tk.Button(title_f, text="✕", command=self.settings.destroy, bg="red", fg="white", bd=0, padx=5).pack(side="right")

        tk.Label(self.settings, text="글자 투명도 (T2)", bg="#222", fg="white").pack(anchor="w")
        fg_sc = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                         command=self.set_fg_alpha, bg="#222", fg="white", highlightthickness=0)
        fg_sc.set(self.fg_alpha)
        fg_sc.pack(fill="x", pady=(0, 10))

        tk.Label(self.settings, text="글자 크기", bg="#222", fg="white").pack(anchor="w")
        sz_sc = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                         command=self.set_font_size, bg="#222", fg="white", highlightthickness=0)
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=(0, 15))

        tk.Button(self.settings, text="🎨 색상 변경", command=self.choose_color, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ 시간 설정", command=self.ask_time, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="🛑 프로그램 종료", command=self.exit_app, bg="#8b0000", fg="white", bd=0, pady=7).pack(fill="x", pady=10)

    def set_fg_alpha(self, val):
        self.fg_alpha = float(val)
        self.apply_alpha()

    def set_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))
        self.pause_icon.config(font=("Helvetica", int(self.font_size*1.2), "bold"))
        self.root.geometry(f"{int(self.font_size*5)}x{int(self.font_size*2)}")

    def choose_color(self):
        color = colorchooser.askcolor(title="색상 선택", color=self.font_color)[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time_initial(self):
        self.root.withdraw()
        self.ask_time()
        self.root.deiconify()

    def ask_time(self):
        input_time = simpledialog.askstring("Timer", "HH:MM:SS", initialvalue=self.time_str)
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
            self.pause_icon.place_forget()
            self.update_timer()
        else:
            self.pause_icon.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueTextTimer(root)
    root.mainloop()
