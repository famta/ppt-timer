import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class ProfessionalTimer:
    def __init__(self, root):
        self.root = root
        
        # 설정 초기값
        self.remaining = 600
        self.bg_color_hex = "#000000" # 기본 배경색 (검정)
        self.font_size = 45
        self.font_color = "#FFFFFF"   # 기본 글자색 (흰색)
        self.running = True

        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # [핵심] 윈도우의 특정 색상을 투명하게 처리
        # 이 색상이 배경색으로 지정되면 그 부분만 투명해집니다.
        self.trans_key = "#000001" 
        self.root.config(bg=self.trans_key)
        self.root.wm_attributes("-transparentcolor", self.trans_key)

        # 타이머 라벨 (배경색 조절로 투명도 흉내)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg="black", cursor="fleur", padx=15, pady=10)
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
        
        # 1. 배경 투명도 (전체 창의 투명도를 조절)
        tk.Label(self.settings, text="배경 투명도 (글자 영향 없음)", bg="#333", fg="white", font=("Arial", 9)).pack()
        bg_scale = tk.Scale(self.settings, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                            command=self.set_bg_opacity, bg="#333", fg="white", highlightthickness=0)
        # 현재 창의 투명도 값을 가져와 설정
        bg_scale.set(self.root.attributes("-alpha"))
        bg_scale.pack(fill="x", pady=(0, 10))

        # 2. 글자 크기
        tk.Label(self.settings, text="글자 크기 조절", bg="#333", fg="white", font=("Arial", 9)).pack()
        size_scale = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                              command=self.update_font_size, bg="#333", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 3. 기능 버튼
        btn_frame = tk.Frame(self.settings, bg="#333")
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="🎨 색상", command=self.choose_color, bg="#555", fg="white", bd=0, padx=5).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="⏱️ 시간", command=self.ask_time, bg="#555", fg="white", bd=0, padx=5).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="설정 닫기", command=self.settings.destroy, bg="#777", fg="white", bd=0).pack(fill="x", pady=(10, 0))
        tk.Button(self.settings, text="프로그램 종료", command=self.root.destroy, bg="#d32f2f", fg="white", bd=0).pack(fill="x", pady=(5, 0))

        # 설정창 바깥 클릭 시 자동 닫기
        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def set_bg_opacity(self, val):
        # 배경 투명도를 조절해도 글자색(fg)은 Label 속성에 의해 선명하게 유지됩니다.
        self.root.attributes("-alpha", float(val))

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
        elif self.remaining < 0:
            self.label.config(text="00:00", fg="red")

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Toplevel을 사용하여 투명도 제어를 더 정교하게 만듦
    app = ProfessionalTimer(tk.Toplevel(root))
    root.mainloop()
