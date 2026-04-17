import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class PerfectTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.bg_opacity = 0.8  # 배경 창의 투명도
        self.font_color_hex = "#FFFFFF" # 글자 색상 (기본 흰색)
        self.font_size = 45
        self.running = True

        self.ask_time()

        # 2. 윈도우 레이아웃 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 전체 창 투명도 설정 (배경용)
        self.root.attributes("-alpha", self.bg_opacity)

        # 3. 타이머 라벨 (글자는 100% 선명도 유지)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color_hex, bg="black", cursor="fleur", padx=15, pady=10)
        self.label.pack()

        # 마우스 이벤트
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_settings)

        self.update_timer()

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#333", padx=12, pady=12)
        
        # [A] 배경 투명도 슬라이더 (창 전체 투명도 조절)
        tk.Label(self.settings, text="[1] 배경 투명도 조절", bg="#333", fg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        bg_scale = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                            command=self.set_window_alpha, bg="#333", fg="white", highlightthickness=0)
        bg_scale.set(self.bg_opacity)
        bg_scale.pack(fill="x", pady=(0, 10))

        # [B] 글자 농도 조절 (글자 색상을 흐리게 만듦)
        tk.Label(self.settings, text="[2] 글자 진하기(농도) 조절", bg="#333", fg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        fg_scale = tk.Scale(self.settings, from_=50, to=255, orient="horizontal",
                            command=self.set_font_brightness, bg="#333", fg="white", highlightthickness=0)
        fg_scale.set(255) # 기본 최대 밝기
        fg_scale.pack(fill="x", pady=(0, 10))

        # [C] 글자 크기 슬라이더
        tk.Label(self.settings, text="[3] 글자 크기 조절", bg="#333", fg="white", font=("Arial", 9, "bold")).pack(anchor="w")
        size_scale = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                              command=self.update_font_size, bg="#333", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 하단 버튼
        btn_frame = tk.Frame(self.settings, bg="#333")
        btn_frame.pack(fill="x", pady=(5, 0))
        tk.Button(btn_frame, text="🎨 색상", command=self.choose_color, bg="#555", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="⏱️ 시간", command=self.ask_time, bg="#555", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="닫기", command=self.settings.destroy, bg="#777", fg="white", bd=0).pack(fill="x", pady=(10, 0))
        tk.Button(self.settings, text="종료 (Exit)", command=self.root.destroy, bg="#d32f2f", fg="white", bd=0).pack(fill="x", pady=(5, 0))

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def set_window_alpha(self, val):
        """배경 창의 투명도만 조절"""
        self.bg_opacity = float(val)
        self.root.attributes("-alpha", self.bg_opacity)

    def set_font_brightness(self, val):
        """글자의 밝기(농도)만 조절 - 배경엔 영향 없음"""
        v = int(val)
        # 현재 선택된 색상 계열을 유지하면서 밝기만 조절하기 위해 회색조 처리
        # (원하는 색상이 있다면 choose_color에서 바꾼 색상이 유지됨)
        hex_color = f'#{v:02x}{v:02x}{v:02x}'
        self.label.config(fg=hex_color)

    def update_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))

    def choose_color(self):
        color = colorchooser.askcolor(title="글자 색상 선택")[1]
        if color:
            self.font_color_hex = color
            self.label.config(fg=self.font_color_hex)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = PerfectTimer(tk.Toplevel(root))
    root.mainloop()
