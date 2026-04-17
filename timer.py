import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class advancedtimer:
    def __init__(self, root):
        self.root = root
        self.root.title("PPT Timer Pro")
        
        # 기본값 설정
        self.remaining = 600
        self.alpha = 0.8
        self.font_size = 35
        self.font_color = "white"
        self.bg_color = "black"
        self.running = True

        # 시간 입력 받기
        input_time = simpledialog.askstring("시간 설정", "발표 시간을 입력하세요 (HH:MM:SS)", initialvalue="00:10:00")
        if not input_time:
            self.root.destroy()
            return
        try:
            h, m, s = map(int, input_time.split(':'))
            self.remaining = h * 3600 + m * 60 + s
        except:
            messagebox.showerror("에러", "시간 형식이 잘못되었습니다.")
            self.root.destroy()
            return

        # 윈도우 초기 설정
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", self.alpha)
        self.root.geometry("250x80+10+10")

        self.label = tk.Label(root, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg=self.font_color, bg=self.bg_color, cursor="fleur")
        self.label.pack(expand=True, fill="both")
        
        # 마우스 바인딩
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        self.label.bind("<Button-3>", self.show_menu) # 우클릭 메뉴

        # 우클릭 메뉴 구성
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="글자 크기 키우기 (+)", command=lambda: self.change_font(5))
        self.menu.add_command(label="글자 크기 줄이기 (-)", command=lambda: self.change_font(-5))
        self.menu.add_separator()
        self.menu.add_command(label="글자 색상 변경", command=self.choose_font_color)
        self.menu.add_command(label="배경 투명도 높이기", command=lambda: self.change_alpha(0.1))
        self.menu.add_command(label="배경 투명도 낮추기", command=lambda: self.change_alpha(-0.1))
        self.menu.add_separator()
        self.menu.add_command(label="타이머 종료 (X)", command=self.root.destroy)

        self.update_timer()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def change_font(self, delta):
        self.font_size += delta
        self.label.config(font=("Helvetica", self.font_size, "bold"))
        # 글자 크기에 맞춰 창 크기 자동 조절
        self.root.geometry(f"{self.font_size*6}x{self.font_size*2}")

    def choose_font_color(self):
        color = colorchooser.askcolor(title="색상 선택")[1]
        if color:
            self.font_color = color
            self.label.config(fg=self.font_color)

    def change_alpha(self, delta):
        self.alpha = max(0.2, min(1.0, self.alpha + delta))
        self.root.attributes("-alpha", self.alpha)

    def update_timer(self):
        if self.running and self.remaining >= 0:
            h, rem = divmod(self.remaining, 3600)
            m, s = divmod(rem, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            self.label.config(text=time_str)
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining < 0:
            self.label.config(text="00:00", fg="red")
            messagebox.showinfo("종료", "시간이 종료되었습니다!")

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    timer = advancedtimer(root)
    root.deiconify()
    root.mainloop()
