import tkinter as tk
from tkinter import simpledialog, colorchooser
import sys

class TextOnlyTimer:
    def __init__(self, root):
        self.root = root
        
        # 1. 초기 설정값
        self.remaining = 600
        self.font_size = 60
        self.font_color = "#FFFFFF" # 기본 흰색 (제일 잘 보임)
        self.running = True
        self.time_str = "00:10:00"

        if not self.ask_time():
            self.remaining = 600 

        # 2. 윈도우 설정 (배경을 완전히 날려버리는 핵심 설정)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # [핵심] 특정 색상을 투명 구멍으로 만듭니다.
        # 배경색을 '초록색(system)'으로 잡고, 그 색을 투명하게 뚫어버립니다.
        self.transparent_color = '#abcdef' 
        self.root.config(bg=self.transparent_color)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)

        # 3. 타이머 라벨 (배경색을 위에서 지정한 투명색으로 설정)
        self.label = tk.Label(self.root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.transparent_color, cursor="fleur")
        self.label.pack(expand=True, fill='both')

        # 마우스 이벤트 (글자를 잡고 드래그하면 이동 가능)
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_settings)

        self.update_timer()

    def show_settings(self, event):
        """우클릭 시 나오는 간단 설정창"""
        if hasattr(self, 'settings') and self.settings.winfo_exists():
            self.settings.destroy()

        self.settings = tk.Toplevel(self.root)
        self.settings.overrideredirect(True)
        self.settings.geometry(f"+{event.x_root}+{event.y_root}")
        self.settings.attributes("-topmost", True)
        self.settings.config(bg="#333", padx=10, pady=10)
        
        # 글자 크기 조절
        tk.Label(self.settings, text="글자 크기", bg="#333", fg="white").pack()
        sz_sc = tk.Scale(self.settings, from_=20, to=300, orient="horizontal",
                         command=self.set_font_size, bg="#333", fg="white", highlightthickness=0)
        sz_sc.set(self.font_size)
        sz_sc.pack(fill="x", pady=5)

        # 버튼들
        tk.Button(self.settings, text="🎨 글자색 변경", command=self.choose_color, bg="#555", fg="white", bd=0).pack(fill="x", pady=2)
        tk.Button(self.settings, text="⏱️ 시간 설정", command=self.ask_time, bg="#555", fg="white", bd=0).pack(fill="x", pady=2)
        tk.Button(self.settings, text="❌ 프로그램 종료", command=self.exit_app, bg="red", fg="white", bd=0).pack(fill="x", pady=5)

        self.settings.bind("<FocusOut>", lambda e: self.settings.destroy())

    def set_font_size(self, val):
        self.font_size = int(val)
        self.label.config(font=("Helvetica", self.font_size, "bold"))

    def choose_color(self):
        color = colorchooser.askcolor(title="글자 색상")[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def ask_time(self):
        input_time = simpledialog.askstring("시간", "HH:MM:SS", initialvalue="00:10:00")
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
