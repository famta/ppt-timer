import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class ProfessionalTimer:
    def __init__(self, root):
        self.root = root
        
        # 설정 초기값
        self.remaining = 600
        self.bg_alpha = 0.8
        self.font_size = 45
        self.font_color = "#FFFFFF"
        self.running = True

        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.bg_alpha)
        self.root.config(bg="black")

        # 메인 컨테이너
        self.container = tk.Frame(self.root, bg="black")
        self.container.pack()

        # 숫자 라벨
        self.label = tk.Label(self.container, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg="black", cursor="fleur", padx=15, pady=10)
        self.label.grid(row=0, column=0)

        # 조절 패널 (마우스 오버 시만 노출)
        self.side_panel = tk.Frame(self.container, bg="black")
        
        # 1. 투명도 슬라이더 (T)
        tk.Label(self.side_panel, text="T", font=("Arial", 7), bg="black", fg="gray").pack()
        self.alpha_scale = tk.Scale(self.side_panel, from_=1.0, to=0.1, resolution=0.05,
                                    orient="vertical", showvalue=0, command=self.update_alpha,
                                    bg="#333", fg="white", highlightthickness=0, width=6, length=40)
        self.alpha_scale.set(self.bg_alpha)
        self.alpha_scale.pack(pady=(0, 5))

        # 2. 글자 크기 슬라이더 (S)
        tk.Label(self.side_panel, text="S", font=("Arial", 7), bg="black", fg="gray").pack()
        self.size_scale = tk.Scale(self.side_panel, from_=150, to=20, resolution=1,
                                   orient="vertical", showvalue=0, command=self.update_font_size,
                                   bg="#333", fg="white", highlightthickness=0, width=6, length=40)
        self.size_scale.set(self.font_size)
        self.size_scale.pack()

        # 마우스 이벤트
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        
        # 마우스 오버 시 사이드 패널 노출/숨김
        self.root.bind("<Enter>", lambda e: self.side_panel.grid(row=0, column=1, padx=(0, 5)))
        self.root.bind("<Leave>", lambda e: self.side_panel.grid_forget())

        # 우클릭 메뉴 (종료 및 색상)
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🎨 글자 색상 변경", command=self.choose_color)
        self.menu.add_command(label="⏱️ 시간 다시 설정", command=self.ask_time)
        self.menu.add_separator()
        self.menu.add_command(label="종료 (Exit)", command=self.root.destroy)
        self.label.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.update_timer()

    def update_alpha(self, val):
        self.bg_alpha = float(val)
        self.root.attributes("-alpha", self.bg_alpha)

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
        elif not hasattr(self, 'remaining'): self.root.destroy()

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
    root.title("Timer")
    app = ProfessionalTimer(root)
    root.mainloop()
