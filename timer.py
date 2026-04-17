import tkinter as tk
from tkinter import messagebox, simpledialog

class MinimalTimer:
    def __init__(self, root):
        self.root = root
        
        # 기본값 설정
        self.remaining = 600
        self.bg_alpha = 0.8
        self.fg_alpha = 255
        self.font_size = 45
        self.running = True

        # 초기 시간 설정
        self.ask_time()

        # 윈도우 설정
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.bg_alpha)
        self.root.config(bg="black")

        # 메인 컨테이너
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack()

        # 숫자 라벨
        self.label = tk.Label(self.frame, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg="white", bg="black", cursor="fleur", padx=10, pady=5)
        self.label.pack(side="left")

        # 종료 버튼 (평소에는 숨김)
        self.close_btn = tk.Button(self.frame, text="✕", command=self.root.destroy, 
                                   bg="#333", fg="white", bd=0, font=("Arial", 10),
                                   padx=5, pady=5, activebackground="red")
        
        # 마우스 이벤트 바인딩
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        
        # 마우스 진입/이탈 감지 (중요!)
        self.root.bind("<Enter>", self.show_exit)
        self.root.bind("<Leave>", self.hide_exit)

        # 우클릭 메뉴
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="시간 다시 설정", command=self.ask_time)
        self.menu.add_separator()
        self.menu.add_command(label="배경 투명도 (+)", command=lambda: self.adjust_bg(0.1))
        self.menu.add_command(label="배경 투명도 (-)", command=lambda: self.adjust_bg(-0.1))
        self.menu.add_command(label="글자 농도 조절", command=self.ask_fg_alpha)
        self.menu.add_command(label="글자 크기 조절", command=self.ask_font_size)
        self.menu.add_separator()
        self.menu.add_command(label="종료", command=self.root.destroy)
        self.label.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.update_timer()

    def show_exit(self, event):
        self.close_btn.pack(side="right", padx=5)

    def hide_exit(self, event):
        self.close_btn.pack_forget()

    def ask_time(self):
        input_time = simpledialog.askstring("시간 설정", "HH:MM:SS", initialvalue="00:10:00")
        if input_time:
            try:
                h, m, s = map(int, input_time.split(':'))
                self.remaining = h * 3600 + m * 60 + s
            except: pass
        elif not hasattr(self, 'remaining'): self.root.destroy()

    def adjust_bg(self, delta):
        self.bg_alpha = max(0.1, min(1.0, self.bg_alpha + delta))
        self.root.attributes("-alpha", self.bg_alpha)

    def ask_fg_alpha(self):
        val = simpledialog.askinteger("글자 농도", "0~255", initialvalue=self.fg_alpha)
        if val is not None:
            self.fg_alpha = max(0, min(255, val))
            color = f'#{self.fg_alpha:02x}{self.fg_alpha:02x}{self.fg_alpha:02x}'
            self.label.config(fg=color)

    def ask_font_size(self):
        val = simpledialog.askinteger("크기", "글자 크기 입력", initialvalue=self.font_size)
        if val:
            self.font_size = val
            self.label.config(font=("Helvetica", self.font_size, "bold"))

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
    app = MinimalTimer(root)
    root.mainloop()
