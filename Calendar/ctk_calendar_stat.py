import customtkinter as ctk
import calendar
from datetime import datetime
import tkinter as tk
import locale


class CTkCalendarStat(ctk.CTkFrame):
    """
    CalendarStat widget displays months with each day rendered as Label. The background of the label is determined
    by the data parameter. If the value of the date differs from the average by 20% it takes 2nd color of
    data_colors, if less 1st color and if more 3rd color.
    """
    def __init__(self, master,
                 data: dict,
                 data_colors: tuple[str, str, str] = ("grey50", "grey30", "grey10"),
                 width=250,
                 height=250,
                 fg_color=None,
                 corner_radius=8,
                 border_width=None,
                 border_color=None,
                 bg_color="transparent",
                 background_corner_colors=None,
                 title_bar_fg_color=None,
                 title_bar_border_width=None,
                 title_bar_border_color=None,
                 title_bar_corner_radius=None,
                 title_bar_text_color=None,
                 title_bar_button_fg_color=None,
                 title_bar_button_hover_color=None,
                 title_bar_button_text_color=None,
                 title_bar_button_border_width=None,
                 title_bar_button_border_color=None,
                 calendar_fg_color=None,
                 calendar_border_width=None,
                 calendar_border_color=None,
                 calendar_corner_radius=None,
                 calendar_text_color=None,
                 calendar_text_fg_color=None,
                 calendar_label_pad=1):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         fg_color=fg_color,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         border_color=border_color,
                         bg_color=bg_color,
                         background_corner_colors=background_corner_colors)

        # data
        self.data = data
        if data is not None:
            self.avg = self.find_avg()
        self.data_colors = data_colors
        self.today = self.current_date()
        self.day, self.month, self.year = self.today[:]
        self.labels_by_date = dict()
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        self.month_label = ctk.StringVar(value=calendar.month_name[self.month].replace("Ã§", "ç").capitalize())
        self.year_label = ctk.IntVar(value=self.year)

        # data for title bar
        self.title_bar_fg_color = title_bar_fg_color
        self.title_bar_border_width = title_bar_border_width
        self.title_bar_border_color = title_bar_border_color
        self.title_bar_text_color = title_bar_text_color
        self.title_bar_button_fg_color = title_bar_button_fg_color
        self.title_bar_button_hover_color = title_bar_button_hover_color
        self.title_bar_button_text_color = title_bar_button_text_color
        self.title_bar_button_border_width = title_bar_button_border_width
        self.title_bar_button_border_color = title_bar_button_border_color
        self.title_bar_corner_radius = title_bar_corner_radius

        # data for calendar frame
        self.calendar_fg_color = calendar_fg_color
        self.calendar_border_width = calendar_border_width
        self.calendar_border_color = calendar_border_color
        self.calendar_corner_radius = calendar_corner_radius
        self.calendar_text_fg_color = calendar_text_fg_color
        self.calendar_text_color = calendar_text_color
        self.calendar_label_pad = calendar_label_pad

        # creating header and calendar frames
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent", width=width, height=height)
        self.content_frame.pack(expand=True, fill="both", padx=corner_radius/3, pady=corner_radius/3)
        self.setup_header_frame()
        self.create_calendar_frame()

    # setting up the header frame
    def setup_header_frame(self):
        header_frame = ctk.CTkFrame(self.content_frame, fg_color=self.title_bar_fg_color,
                                    corner_radius=self.title_bar_corner_radius,
                                    border_color=self.title_bar_border_color, border_width=self.title_bar_border_width)

        ctk.CTkButton(header_frame, text="<", text_color="black", width=45, height=45, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont("Arial", 16, "bold"),
                      command=lambda: self.change_month(-1)).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, textvariable=self.month_label, font=ctk.CTkFont("Arial", 19, "bold"),
                     fg_color="transparent").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(header_frame, textvariable=self.year_label, font=ctk.CTkFont("Arial", 19, "bold"),
                     fg_color="transparent").pack(side="left", fill="x")
        ctk.CTkButton(header_frame, text=">", text_color="black", width=45, height=45, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont("Arial", 16, "bold"),
                      command=lambda: self.change_month(1)).pack(side="right", padx=10)

        header_frame.place(relx=0.5, rely=0.02, anchor="n", relheight=0.18, relwidth=0.95)

    def create_calendar_frame(self):
        # "updating" frames
        calendar_frame = ctk.CTkFrame(self.content_frame, fg_color=self.calendar_fg_color,
                                      corner_radius=self.calendar_corner_radius,
                                      border_width=self.calendar_border_width, border_color=self.calendar_border_color)
        current_month = calendar.monthcalendar(self.year, self.month)

        # grid
        calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="b")
        rows = tuple([i for i in range(len(current_month) + 1)])  # Add one row for days of the week
        calendar_frame.rowconfigure(rows, weight=1, uniform="b")

        # labels for days of the week
        days_of_week = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        for i, day in enumerate(days_of_week):
            ctk.CTkLabel(calendar_frame, text=day, font=ctk.CTkFont("Arial", 13, "bold"),
                         fg_color="transparent", text_color=self.calendar_text_color).grid(row=0, column=i, sticky="nsew")

        # labels for days
        for row in range(1, len(current_month) + 1):
            for column in range(7):
                if current_month[row - 1][column] != 0:
                    self.setup_label_with_data(calendar_frame, current_month[row - 1][column], row, column)

        calendar_frame.place(relx=0.5, rely=0.97, anchor="s", relheight=0.75, relwidth=0.95)

    def change_month(self, amount):
        self.month += amount
        if self.month < 1:
            self.year -= 1
            self.month = 12
            self.day = 1
        elif self.month > 12:
            self.year += 1
            self.month = 1
            self.day = 1

        self.month_label.set(calendar.month_name[self.month].replace("Ã§", "ç").capitalize())
        self.year_label.set(self.year)

        self.create_calendar_frame()

    # Atualiza a exibição do calendário
    def replot_current_month(self):
        # Remove o frame atual do calendário, se existir
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Cria novamente o frame do calendário
        self.setup_header_frame()
        self.create_calendar_frame()

    def current_date(self) -> tuple[int, int, int]:
        date = str(datetime.now()).split()
        year, month, day = date[0].split("-")
        return int(day), int(month), int(year)

    def date_is_today(self, date: tuple) -> bool:
        if date[2] == self.today[2] and date[1] == self.today[1] and date[0] == self.today[0]:
            return True
        return False

    # setting up date labels if certain data exists
    def setup_label_with_data(self, frame, day, row, column):
        fg_color = '#2b2b2b'
        border_width = 0
        border_color = None

        if self.data.get((day, self.month, self.year)) is not None:
            if self.data[(day, self.month, self.year)] < self.avg * 0.8:
                fg_color = self.data_colors[0]  # Primeira cor de dados
            elif self.data[(day, self.month, self.year)] > self.avg * 1.2:
                fg_color = self.data_colors[2]  # Terceira cor de dados
            else:
                fg_color = self.data_colors[1]  # Segunda cor de dados
        
        if (day, self.month, self.year) == (self.day, self.month, self.year):
            fg_color = '#6e6b6b'  # Cor cinza claro para o dia atual
            if (day, self.month, self.year) in self.data.keys():
                border_width = 2
                border_color = "red"  # Cor da borda para o dia atual

        label = ctk.CTkButton(frame, text=str(day), corner_radius=5,
                            fg_color=fg_color, font=ctk.CTkFont("Arial", 13, "bold"),
                            text_color=self.calendar_text_color,
                            hover=False,
                            border_width=border_width,
                            border_color=border_color)
        
        label.grid(row=row, column=column, sticky="nsew", padx=self.calendar_label_pad,
                pady=self.calendar_label_pad)


    def find_avg(self):
        s = 0
        counter = 0
        for value in self.data.values():
            s += value
            counter += 1
        return s / counter