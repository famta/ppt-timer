import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class UltimateTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기값 설정
        self.remaining = 600
        self.bg_alpha = 0.8    # 배경(창 전체) 투명도 (0.1 ~ 1.0)
        self.fg_alpha = 1.0    # 글자 투명도 (0.1 ~ 1.0)
        self.font_size = 50
        self.font_rgb = (255, 255, 255) # 기본 흰색
        self.running = True

        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="black") # 기본 배경색 고정

        # 3. 캔버스 사용 (글자 투명도 시뮬레이션을 위해 필수)
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.toggle_timer)
        self.canvas.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.refresh_display()

    def refresh_display(self):
        """배경과 글자 투명도를 각각 계산하여 렌더링"""
        # [A] 배경 투명도 적용 (윈도우 전체 투명도)
        self.root.attributes("-alpha", self.bg_alpha)
        
        # [B] 글자 투명도 적용 (배경색인 검정색과 RGB를 합성)
        r = int(self.font_rgb[0] * self.fg_alpha)
        g = int(self.font_rgb[1] * self.fg_alpha)
        b = int(self.font_rgb[2] * self.fg_alpha)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.canvas.delete("all")
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        # 중앙 정렬 (초기 실행 시 winfo값이 1이므로 대비책 마련)
        cx = w/2 if w > 1 else 100
        cy = h/2 if h > 1 else 40
        
        self.canvas.create_text(cx, cy, text=self.time_str, 
                                font=("Helvetica", self.font_size, "bold"), 
                                fill=hex_color)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#333", padx=15, pady=15)
        
        # 슬라이더 1: 배경 투명도 (T1)
        tk.Label(self.settings, text="배경 투명도 (뒤쪽 비침)", bg="#333", fg="white", font=("Arial", 9)).pack(anchor="w")
        bg_sc = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                         command=self.set_bg_alpha, bg="#333", fg="white", highlightthickness=0)
        bg_sc.set(self.bg_alpha)
        bg_sc.pack(fill="x", pady=(0, 10))

        # 슬라이더 2: 글자 투명도 (T2)
        tk.Label(self.settings, text="글자 투명도 (글자만 투명하게)", bg="#333", fg="white", font=("Arial", 9)).pack(anchor="w")
        fg_sc = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                         command=self.set_fg_alpha, bg="#333", fg="white", highlightthickness=0)
        fg_sc.set(self.fg_alpha)
        fg_sc.pack(fill="x", pady=(0, 10))

        # 슬라이더 3: 글자 크기
        tk.Label(self.settings, text="글자 크기", bg="#333", fg="white", font=("Arial", 9)).pack(anchor="w")
        sz_sc = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                         command=self.set_font_size, bg="#333", fg="white", highlightthickness=0)
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=(0, 10))

        # 버튼들
        btn_f = tk.Frame(self.settings, bg="#333")
        btn_f.pack(fill="x", pady=5)
        tk.Button(btn_f, text="🎨 색상", command=self.choose_color, bg="#555", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_f, text="⏱️ 시간", command=self.ask_time, bg="#555", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="설정 닫기", command=self.settings.destroy, bg="#777", fg="white", bd=0).pack(fill="x", pady=2)
        tk.Button(self.settings, text="프로그램 종료", command=self.exit_program, bg="red", fg="white", bd=0).pack(fill="x", pady=5)

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def set_bg_alpha(self, val):
        self.bg_alpha = float(val)
        self.refresh_display()

    def set_fg_alpha(self, val):
        self.fg_alpha = float(val)
        self.refresh_display()

    def set_font_size(self, val):
        self.font_size = int(val)
        self.root.geometry(f"{int(self.font_size*4.5)}x{int(self.font_size*1.8)}")
        self.refresh_display()

    def exit_program(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def choose_color(self):
        color = colorchooser.askcolor(title="글자 색상 선택")[0] # RGB 튜플
        if color:
            self.font_rgb = color
            self.refresh_display()

    def ask_time(self):
        input_time = simpledialog.askstring("시간 설정", "HH:MM:SS", initialvalue="00:10:00")
        if input_time:
            try:
                h, m, s = map(int, input_time.split(':'))
                self.remaining = h * 3600 + m * 60 + s
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
            self.refresh_display()
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTimer(root)
    root.mainloop()
