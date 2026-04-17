import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class UltimateTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기값 설정
        self.remaining = 600
        self.font_size = 50
        self.font_color = "#FFFFFF" 
        self.bg_opacity = 180       
        self.running = True

        # 시간 설정 (취소 시 프로그램 종료 방지 로직 포함)
        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정 (Toplevel 대신 root 직접 제어)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # 윈도우 특정 색상 투명화 (Windows 전용)
        self.trans_key = "#000001"
        self.root.wm_attributes("-transparentcolor", self.trans_key)

        # 3. 타이머 라벨 (배경 농도와 글자 선명도 분리)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg="black", cursor="fleur", padx=15, pady=10)
        self.label.pack()

        # 이벤트 바인딩
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_settings)

        # 프로그램 종료 시 완전히 프로세스를 죽이도록 설정
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

        self.update_timer()
        self.apply_bg_opacity()

    def apply_bg_opacity(self):
        """글자 선명도는 유지하고 배경 농도만 조절"""
        opacity_hex = f'#{self.bg_opacity:02x}{self.bg_opacity:02x}{self.bg_opacity:02x}'
        self.label.config(bg=opacity_hex)

    def show_settings(self, event):
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#333", padx=12, pady=12)
        
        # 배경 농도 슬라이더
        tk.Label(self.settings, text="배경 농도 (0~255)", bg="#333", fg="white", font=("Arial", 9)).pack()
        bg_scale = tk.Scale(self.settings, from_=0, to=255, orient="horizontal",
                            command=self.update_bg_opacity, bg="#333", fg="white", highlightthickness=0)
        bg_scale.set(self.bg_opacity)
        bg_scale.pack(fill="x", pady=(0, 10))

        # 글자 크기 슬라이더
        tk.Label(self.settings, text="글자 크기", bg="#333", fg="white", font=("Arial", 9)).pack()
        size_scale = tk.Scale(self.settings, from_=20, to=200, orient="horizontal",
                              command=self.update_font_size, bg="#333", fg="white", highlightthickness=0)
        size_scale.set(self.font_size)
        size_scale.pack(fill="x", pady=(0, 10))

        # 기능 버튼
        btn_frame = tk.Frame(self.settings, bg="#333")
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="🎨 색상", command=self.choose_color, bg="#555", fg="white", bd=0, padx=5).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="⏱️ 시간", command=self.ask_time, bg="#555", fg="white", bd=0, padx=5).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(self.settings, text="설정창 닫기", command=self.settings.destroy, bg="#777", fg="white", bd=0).pack(fill="x", pady=(10, 0))
        tk.Button(self.settings, text="프로그램 종료", command=self.exit_program, bg="red", fg="white", bd=0).pack(fill="x", pady=(5, 0))

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def exit_program(self):
        """프로세스까지 완전히 종료"""
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def update_bg_opacity(self, val):
        self.bg_opacity = int(val)
        self.apply_bg_opacity()

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
            self.label.config(text=f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    # root.withdraw() 제거 (백그라운드 잔류 원인)
    app = UltimateTimer(root)
    root.mainloop()
