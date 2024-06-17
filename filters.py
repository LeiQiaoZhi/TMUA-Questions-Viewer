import customtkinter
from styling import *

PADDING = 6


class FilterFrame(customtkinter.CTkFrame):

    def __init__(self, master, title, options):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        header_frame = customtkinter.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="nsew")
        title_label = customtkinter.CTkLabel(header_frame,
                                             text=title,
                                             font=(FONT, 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=4, sticky="w")
        reset_button = customtkinter.CTkLabel(header_frame,
                                              text="Reset",
                                              font=(FONT, 12, "italic"))
        reset_button.bind("<Button-1>", lambda e: self.reset())
        reset_button.grid(row=0, column=1, padx=10, pady=4, sticky="nse")

        scroll_frame = customtkinter.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.checkboxes = []
        for i, option in enumerate(options):
            checkbox = customtkinter.CTkCheckBox(scroll_frame, text=option)
            checkbox.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.checkboxes.append(checkbox)

    def get_selected_options(self):
        return [
            checkbox.cget("text") for checkbox in self.checkboxes
            if checkbox.get()
        ]

    def reset(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()


class PaperFilterFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.P1 = customtkinter.CTkCheckBox(self, text="P1")
        self.P1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.P2 = customtkinter.CTkCheckBox(self, text="P2")
        self.P2.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def get_selected_options(self):
        return [
            child.cget("text") for child in self.winfo_children()
            if child.get()
        ]

    def reset(self):
        self.P1.deselect()
        self.P2.deselect()


class FilterBarFrame(customtkinter.CTkFrame):

    def __init__(self, master, filter_options):
        super().__init__(master)
        self.filter_options = filter_options

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=100)
        self.grid_rowconfigure(1, weight=0)
        for i in range(len(filter_options)):
            self.grid_rowconfigure(i + 2, weight=1)

        filter_button = customtkinter.CTkButton(
            self,
            text="Filter",
            command=master.on_filter_button_click,
            font=(FONT, 16, "bold"))
        filter_button.grid(row=0, column=1, pady=(0, PADDING), sticky="nsew")
        reset_all_btn = customtkinter.CTkButton(
            self,
            text="Reset All",
            width=60,
            command=self.reset_all,
            fg_color=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"],
            font=(FONT, 12, "italic"))
        reset_all_btn.grid(row=0,
                           column=0,
                           padx=(0, PADDING),
                           pady=(0, PADDING),
                           sticky="nsew")

        self.paper_filter_frame = PaperFilterFrame(self)
        self.paper_filter_frame.grid(row=1,
                                     column=0,
                                     **FILTER_FRAME_GRID_OPTIONS,
                                     columnspan=2)
        self.filter_frames = []
        for i in range(len(filter_options)):
            title = list(filter_options.keys())[i]
            options = list(filter_options.values())[i]
            filter_frame = FilterFrame(self, title, options)
            filter_frame.grid(row=i + 2,
                              column=0,
                              **FILTER_FRAME_GRID_OPTIONS,
                              columnspan=2)
            self.filter_frames.append(filter_frame)

    def get_selected_options(self):
        selected = {"Paper": self.paper_filter_frame.get_selected_options()}
        for i, filter_frame in enumerate(self.filter_frames):
            selected[list(self.filter_options.keys())
                     [i]] = filter_frame.get_selected_options()
        return selected

    def reset_all(self):
        self.paper_filter_frame.reset()
        for filter_frame in self.filter_frames:
            filter_frame.reset()
