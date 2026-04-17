import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class UltimateTextTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.font_size = 60
        self.font_color_rgb = (255, 255, 255) # RGB 튜플 (흰색)
        self.fg_alpha = 1.0    # [복구] 글자 투명도 (0.1 ~ 1.0)
        self.running = True
        self.time_str = "00:10:00"

        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정 (배경 완전 투명화)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 특정 색상을 투명하게 뚫음
        self.transparent_key = '#abcdef' 
        self.root.config(bg=self.transparent_key)
        self.root.wm_attributes("-transparentcolor", self.transparent_key)

        # 3. 캔버스 (글자 투명도 조절 및 아이콘 표시를 위해 사용)
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.transparent_key)
        self.canvas.pack(expand=True, fill='both')

        # 마우스 이벤트
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.toggle_timer)
        self.canvas.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.render_text()

    def render_text(self):
        """글자 투명도(T2)와 일시정지 아이콘을 포함하여 화면 갱신"""
        # 글자 투명도 계산 (색상 합성 방식)
        r = int(self.font_color_rgb[0] * self.fg_alpha)
        g = int(self.font_color_rgb[1] * self.fg_alpha)
        b = int(self.font_color_rgb[2] * self.fg_alpha)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        
        # 일시정지 시 앞에 || 표시 추가
        display_text = self.time_str
        if not self.running:
            display_text = f"|| {self.time_str}"
        
        self.canvas.delete("all")
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        cx, cy = (w/2 if w > 1 else 150), (h/2 if h > 1 else 50)
        
        self.canvas.create_text(cx, cy, text=display_text, 
                                font=("Helvetica", self.font_size, "bold"), 
                                fill=hex_color)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=15, pady=15, highlightbackground="#444", highlightthickness=1)
        
        # 헤더 및 닫기 버튼
        title_frame = tk.Frame(self.settings, bg="#222")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="SETTINGS", bg="#222", fg="#aaa", font=("Arial", 8, "bold")).pack(side="left")
        tk.Button(title_frame, text="✕", command=self.settings.destroy, bg="#222", fg="white", bd=0).pack(side="right")

        # 1. 글자 투명도 슬라이더 (복구 완료)
        tk.Label(self.settings, text="글자 투명도 (T2)", bg="#222", fg="white", font=("Arial", 9)).pack(anchor="w")
        fg_sc = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                         command=self.set_fg_alpha, bg="#222", fg="white", highlightthickness=0)
        fg_sc.set(self.fg_alpha)
        fg_sc.pack(fill="x", pady=(0, 10))

        # 2. 글자 크기 슬라이더
        tk.Label(self.settings, text="글자 크기", bg="#222", fg="white", font=("Arial", 9)).pack(anchor="w")
        sz_sc = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                         command=self.set_font_size, bg="#222", fg="white", highlightthickness=0)
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=(0, 15))

        # 기능 버튼들
        tk.Button(self.settings, text="🎨 글자 색상 변경", command=self.choose_color, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ 시간 재설정", command=self.ask_time, bg="#444", fg="white", bd=0, pady=5).pack(fill="x", pady=2)
        tk.Button(self.settings, text="❌ 프로그램 종료", command=self.exit_app, bg="#d32f2f", fg="white", bd=0, pady=7).pack(fill="x", pady=10)

        self.settings.focus_set()
        self.settings.bind("<FocusOut>", lambda e: self.settings.after(100, self.settings.destroy))

    def set_fg_alpha(self, val):
        self.fg_alpha = float(val)
        self.render_text()

    def set_font_size(self, val):
        self.font_size = int(val)
        self.root.geometry(f"{int(self.font_size*6)}x{int(self.font_size*1.8)}")
        self.render_text()

    def exit_app(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def choose_color(self):
        color = colorchooser.askcolor(title="Select Color")[0]
        if color:
            self.font_color_rgb = color
            self.render_text()

    def ask_time(self):
        input_time = simpledialog.askstring("Timer", "HH:MM:SS", initialvalue="00:10:00")
        if input_time:
            try:
                h, m, s = map(int, input_time.split(':'))
                self.remaining = h * 3600 + m * 60 + s
                self.render_text()
                return True
            except: return False
        return False

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
            self.render_text()
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        self.render_text() # 상태 변화 즉시 반영 (아이콘 표시)
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTextTimer(root)
    root.mainloop()
