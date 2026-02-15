# main.py
import customtkinter as ctk
from datetime import datetime
from theme import THEME, FONTS
from utils import DataManager
from components import SmoothSidebar, CelebrationFrame


class MoonTaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MoonTask Desktop Pro")
        self.geometry("1000x680")
        self.configure(fg_color=THEME["bg"])

        self.data = DataManager.load_data()
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        # 布局配置
        self.grid_columnconfigure(0, weight=0)  # 侧边栏列 (宽度由侧边栏组件自己控制)
        self.grid_columnconfigure(1, weight=1)  # 主内容列
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()
        self.refresh_task_list()

    def setup_ui(self):
        # 1. 侧边栏
        self.sidebar = SmoothSidebar(
            self,
            on_date_select=self.switch_date,
            on_search_click=self.handle_search
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 2. 主区域
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # 标题
        self.date_title = ctk.CTkLabel(self.main_area, text="Today", font=("Microsoft YaHei UI", 32, "bold"),
                                       text_color=THEME["text_main"])
        self.date_title.pack(anchor="w", pady=(0, 20))

        # 任务滚动区
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent",
                                                   scrollbar_button_color=THEME["sidebar"])
        self.scroll_frame.pack(fill="both", expand=True)

        # 输入框
        input_frame = ctk.CTkFrame(self.main_area, fg_color=THEME["sidebar"], height=60, corner_radius=30)
        input_frame.pack(fill="x", pady=(20, 0))

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Add a new task...", border_width=0,
                                  fg_color="transparent",
                                  text_color=THEME["text_main"], font=FONTS["main"], height=50)
        self.entry.pack(side="left", fill="x", expand=True, padx=20)
        self.entry.bind("<Return>", lambda e: self.add_task())

        # 祝贺遮罩
        self.celebration = CelebrationFrame(self, reset_command=self.hide_celebration)

    def switch_date(self, date_str):
        self.current_date = date_str
        self.date_title.configure(text=date_str if date_str != datetime.now().strftime("%Y-%m-%d") else "Today")
        self.refresh_task_list()
        self.hide_celebration()

    def handle_search(self):
        print("Search button clicked! Implement your search logic here.")
        dialog = ctk.CTkInputDialog(text="Search tasks:", title="Search")
        query = dialog.get_input()
        print(f"Searching for: {query}")

    def refresh_task_list(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        tasks = self.data.get(self.current_date, [])
        for t in tasks: self.create_task_row(t)

    def create_task_row(self, text):
        f = ctk.CTkFrame(self.scroll_frame, fg_color=THEME["card"], corner_radius=10)
        f.pack(fill="x", pady=5)
        ctk.CTkCheckBox(f, text="", width=24, height=24, corner_radius=12, fg_color=THEME["accent"],
                        border_color=THEME["accent"],
                        hover_color=THEME["gold"], command=lambda: self.complete_task(text, f)).pack(side="left",
                                                                                                     padx=15, pady=15)
        ctk.CTkLabel(f, text=text, font=FONTS["main"], text_color=THEME["text_main"]).pack(side="left", pady=15)

    def add_task(self):
        text = self.entry.get().strip()
        if not text: return
        if self.current_date not in self.data: self.data[self.current_date] = []
        self.data[self.current_date].append(text)
        DataManager.save_data(self.data)
        self.refresh_task_list()
        self.entry.delete(0, "end")

    def complete_task(self, text, widget):
        self.after(500, lambda: self._remove(text, widget))

    def _remove(self, text, widget):
        if text in self.data.get(self.current_date, []):
            self.data[self.current_date].remove(text)
        widget.destroy()
        DataManager.save_data(self.data)

        if self.current_date == datetime.now().strftime("%Y-%m-%d") and not self.data[self.current_date]:
            self.celebration.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.celebration.refresh()

    def hide_celebration(self):
        self.celebration.place_forget()


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = MoonTaskApp()
    app.mainloop()