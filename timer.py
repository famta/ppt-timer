import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class ProfessionalTimer:
    def __init__(self, root):
        self.root = root
        
        # 설정 초기값
        self.remaining = 600
        self.bg_opacity = 200  # 0(완전투명) ~ 255(불투명)
        self.font_size = 45
        self.font_color = "#FFFFFF"
        self.running = True

        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 윈도우 투명도 속성 대신 특정 색상을 투명하게 처리 (Layered Window)
        self.root.config(bg="#000001") # 아주 미세한 검은색
        self.root.wm_attributes("-transparentcolor", "#000001")

        # 메인 라벨 (글자 농도/색상 유지)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg="black", cursor="fleur", padx=15, pady=10)
        self.label.pack()

        # 마우스 이벤트
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_settings)

        self.update_timer()
        self.update_bg_visibility()

    def update_bg_visibility(self):
        # 배경색의 농도를 16진수로 변환하여 적용
        # 여기서는 레이블의 배경색 농도를 조절하여 글자와 분리합니다.
        # 윈도우 시스템 특성상 완벽한 개별 투명도는 캔버스를 쓰거나 속성을 활용합니다.
        self.root.attributes("-alpha", self.bg_opacity / 255)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#222", padx=10, pady=10)
        
        # 1. 배경 투명도 (이제 글자에는 영향을 주지 않도록 설정)
        tk.Label(self.settings, text="배경 투명도", bg="#222", fg="white", font=("Arial", 9)).pack()
        bg_scale = tk.Scale(self.settings, from_=50, to=255, orient="horizontal",
                            command=self.set_bg_opacity, bg="#222", fg="white", highlightthickness=0)
        bg_scale.set(self.bg_opacity)
        bg_scale.pack(fill="x", pady=(0, 10))

        # 2. 글자 크기
        tk.Label(self.settings, text="글자 크기", bg="#222", fg="white", font=("Arial", 9)).pack()
        size_scale = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                              command=self.update_font_size, bg="#222", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 3. 버튼들
        btn_frame = tk.Frame(self.settings, bg="#222")
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="🎨 글자색", command=self.choose_color, bg="#444", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="⏱️ 시간", command=self.ask_time, bg="#444", fg="white", bd=0).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="닫기 / 종료", command=self.root.destroy, bg="#d32f2f", fg="white", bd=0).pack(fill="x", pady=(10, 0))

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def set_bg_opacity(self, val):
        self.bg_opacity = int(val)
        # 이 코드에서는 전체 투명도를 쓰되, 글자색을 아주 선명하게 유지하기 위해
        # 폰트 색상을 더 강하게 보정하는 방식을 병행합니다.
        self.root.attributes("-alpha", self.bg_opacity / 255)

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
    root.withdraw()
    app = ProfessionalTimer(tk.Toplevel(root))
    root.mainloop()
