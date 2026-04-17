import tkinter as tk
from tkinter import messagebox

class PresentationTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("PPT Timer")
        self.remaining = 600
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.8)
        self.root.geometry("200x60+10+10")

        self.label = tk.Label(root, text="", font=("Helvetica", 30, "bold"), 
                              fg="white", bg="black", cursor="fleur")
        self.label.pack(expand=True, fill="both")
        
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Double-Button-1>", self.toggle_timer)

        self.running = True
        self.update_timer()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_timer(self):
        if self.running and self.remaining >= 0:
            mins, secs = divmod(self.remaining, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.label.config(text=time_str)
            if self.remaining < 60:
                self.label.config(fg="red")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining < 0:
            self.label.config(text="00:00")
            messagebox.showinfo("종료", "발표 시간이 종료되었습니다!")

    def toggle_timer(self, event):
        self.running = not self.running
        if self.running:
            self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    timer = PresentationTimer(root)
    root.mainloop()
