import customtkinter as ctk
import calendar
from datetime import datetime
from theme import THEME, FONTS
from utils import PoetryManager


class SmoothSidebar(ctk.CTkFrame):
    def __init__(self, master, on_date_select, on_search_click, **kwargs):
        super().__init__(master, fg_color=THEME["sidebar"], corner_radius=0, **kwargs)
        self.on_date_select = on_date_select
        self.on_search_click = on_search_click
        self.expanded_width = 270
        self.collapsed_width = 65
        self.current_width = self.expanded_width
        self.is_expanded = True
        self.animation_running = False

        self.selected_date_obj = datetime.now()

        self.grid_propagate(False)
        self.pack_propagate(False)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.top_frame.pack(fill="x", pady=10)

        self.menu_btn = ctk.CTkButton(
            self.top_frame, text="≡", width=40, height=40,
            fg_color="transparent", hover_color=THEME["hover"],
            font=FONTS["icon_lg"], text_color=THEME["text_main"],
            command=self.toggle_sidebar
        )
        self.menu_btn.pack(side="left", padx=(10, 5))

        self.logo_lbl = ctk.CTkLabel(self.top_frame, text="MoonTask", font=FONTS["title"],
                                     text_color=THEME["text_main"])
        self.logo_lbl.pack(side="left", padx=5)

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.render_expanded_view()
        self.search_btn = ctk.CTkButton(
            self, text="🔍  Search Tasks...", fg_color=THEME["card"],
            text_color=THEME["text_dim"], hover_color=THEME["hover"],
            height=40, anchor="w", command=self.on_search_click
        )
        self.search_btn.pack(side="bottom", fill="x", padx=10, pady=20)

    def toggle_sidebar(self):
        if self.animation_running: return

        self.clear_content()

        target = self.collapsed_width if self.is_expanded else self.expanded_width
        step = -25 if self.is_expanded else 25

        self.is_expanded = not self.is_expanded
        if not self.is_expanded:
            self.logo_lbl.pack_forget()
            self.search_btn.configure(text="🔍", width=40, anchor="center")

        self.animate(target, step, callback=self.on_animation_end)

    def animate(self, target, step, callback):
        self.animation_running = True

        if (step < 0 and self.current_width > target) or (step > 0 and self.current_width < target):
            self.current_width += step
            self.configure(width=self.current_width)
            self.update_idletasks()
            self.after(10, lambda: self.animate(target, step, callback))
        else:
            self.current_width = target
            self.configure(width=target)
            self.animation_running = False
            if callback: callback()

    def on_animation_end(self):
        if self.is_expanded:
            self.logo_lbl.pack(side="left", padx=5)
            self.search_btn.configure(text="🔍  Search Tasks...", width=200, anchor="w")
            self.render_expanded_view()
        else:
            self.render_collapsed_view()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def render_expanded_view(self):
        self.clear_content()

        # 月份标题
        ctk.CTkLabel(self.content_frame, text=self.selected_date_obj.strftime("%B %Y"),
                     font=("Arial", 14, "bold"), text_color=THEME["accent"]).pack(pady=(5, 10))

        grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid.pack()

        # 星期头
        for i, d in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            ctk.CTkLabel(grid, text=d, width=28, text_color=THEME["text_dim"], font=("Arial", 10)).grid(row=0, column=i)

        cal = calendar.monthcalendar(self.selected_date_obj.year, self.selected_date_obj.month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    self.create_day_btn(grid, day, r + 1, c)

    def render_collapsed_view(self):
        self.clear_content()

        cal = calendar.monthcalendar(self.selected_date_obj.year, self.selected_date_obj.month)
        target_day = self.selected_date_obj.day
        current_week = []
        for week in cal:
            if target_day in week:
                current_week = week
                break

        if not current_week: return

        days_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        for i, day in enumerate(current_week):
            if day != 0:
                row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
                row.pack(pady=2)
                ctk.CTkLabel(row, text=days_str[i], font=("Arial", 9), text_color=THEME["text_dim"]).pack()
                self.create_day_btn(row, day, 0, 0, pack_mode=True)

    def create_day_btn(self, parent, day, r, c, pack_mode=False):
        d_str = f"{self.selected_date_obj.year}-{self.selected_date_obj.month:02d}-{day:02d}"
        now = datetime.now()
        is_today = (
                    self.selected_date_obj.year == now.year and self.selected_date_obj.month == now.month and day == now.day)
        is_selected = (day == self.selected_date_obj.day)

        fg = THEME["today_highlight"] if is_today else "transparent"
        fg = THEME["selected"] if is_selected else fg
        txt = "#FFF" if (is_today or is_selected) else THEME["text_dim"]
        btn = ctk.CTkButton(
            parent, text=str(day), width=28, height=28, fg_color=fg,
            text_color=txt, corner_radius=8, font=("Arial", 11),
            hover_color=THEME["hover"],
            command=lambda d=d_str: self.handle_click(d)
        )
        if pack_mode:
            btn.pack()
        else:
            btn.grid(row=r, column=c, padx=1, pady=1)

    def handle_click(self, date_str):
        self.selected_date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if self.is_expanded:
            self.render_expanded_view()
        else:
            self.render_collapsed_view()
        self.on_date_select(date_str)


class CelebrationFrame(ctk.CTkFrame):
    def __init__(self, master, reset_command, **kwargs):
        super().__init__(master, fg_color=THEME["bg"], **kwargs)
        self.reset_command = reset_command
        self.poem_manager = PoetryManager()

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center, text="🌕", font=("Arial", 64)).pack(pady=(0, 20))
        self.poem_content = ctk.CTkLabel(center, text="...", font=FONTS["poem"], text_color=THEME["text_main"],
                                         wraplength=500, justify="center")
        self.poem_content.pack(pady=15)
        self.poem_info = ctk.CTkLabel(center, text="", font=("Microsoft YaHei UI", 12), text_color=THEME["text_dim"])
        self.poem_info.pack(pady=(0, 30))

        ctk.CTkButton(center, text="返回清单", fg_color="transparent", border_width=1, border_color=THEME["text_dim"],
                      text_color=THEME["text_dim"], command=self.reset_command).pack(pady=20)

    def refresh(self):
        self.poem_content.configure(text="正在寻觅佳句...")
        self.poem_manager.fetch_poem(self.update_ui)

    def update_ui(self, data):
        self.poem_content.configure(text=data.get("content", ""))
        self.poem_info.configure(text=f"—— {data.get('author', '')} · 《{data.get('origin', '')}》")