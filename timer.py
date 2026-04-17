import tkinter as tk
from tkinter import messagebox, simpledialog

class UltimateTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("PPT Timer Pro") # 이제 작업 표시줄에 이름이 뜹니다.
        
        # 설정 초기값
        self.remaining = 600
        self.bg_alpha = 0.8    # 배경 투명도
        self.fg_alpha = 1.0    # 글자 투명도 (색상 농도로 조절)
        self.font_size = 35
        self.running = True

        # 시간 입력 받기
        input_time = simpledialog.askstring("시간 설정", "발표 시간 (HH:MM:SS)", initialvalue="00:10:00")
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

        # 메인 윈도우 설정
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(False) # 작업 표시줄 아이콘 표시를 위해 True -> False 변경
        # 제목 표시줄만 없애기 위한 윈도우 스타일 (Windows 전용)
        self.root.attributes("-alpha", self.bg_alpha)
        
        # 배경 프레임
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(expand=True, fill="both")

        # 타이머 라벨 (왼쪽)
        self.label = tk.Label(self.main_frame, text="", font=("Helvetica", self.font_size, "bold"), 
                              fg="white", bg="black", cursor="fleur")
        self.label.pack(side="left", padx=10, expand=True)
        
        # 제어 패널 (오른쪽)
        self.ctrl_frame = tk.Frame(self.main_frame, bg="#222")
        self.ctrl_frame.pack(side="right", fill="y")

        # 투명도 조절 버튼 (+/-)
        tk.Button(self.ctrl_frame, text="+", command=lambda: self.adjust_alpha(0.05), bg="#444", fg="white", bd=0).pack(fill="x")
        self.alpha_label = tk.Label(self.ctrl_frame, text=f"{int(self.bg_alpha*100)}%", font=("Arial", 8), bg="#222", fg="gray")
        self.alpha_label.pack()
        tk.Button(self.ctrl_frame, text="-", command=lambda: self.adjust_alpha(-0.05), bg="#444", fg="white", bd=0).pack(fill="x")

        # 마우스 바인딩 (이동)
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)
        
        # 우클릭 종료 메뉴
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="글자 투명도 조절", command=self.set_fg_alpha)
        self.menu.add_command(label="종료", command=self.root.destroy)
        self.label.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.update_timer()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def adjust_alpha(self, delta):
        self.bg_alpha = max(0.1, min(1.0, self.bg_alpha + delta))
        self.root.attributes("-alpha", self.bg_alpha)
        self.alpha_label.config(text=f"{int(self.bg_alpha*100)}%")

    def set_fg_alpha(self):
        val = simpledialog.askinteger("글자 농도", "글자 진하기를 입력하세요 (10-100)", initialvalue=int(self.fg_alpha*100))
        if val:
            self.fg_alpha = val / 100
            # 색상을 RGBA 느낌으로 변환할 수 없으므로 회색조로 농도 표현
            gray_val = int(255 * self.fg_alpha)
            hex_color = f'#{gray_val:02x}{gray_val:02x}{gray_val:02x}'
            self.label.config(fg=hex_color)

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

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running: self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    # 타이틀바 제거를 원하시면 아래 주석을 해제하세요. (단, 아이콘이 다시 사라질 수 있음)
    # root.overrideredirect(True) 
    timer = UltimateTimer(root)
    root.mainloop()
