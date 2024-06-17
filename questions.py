import pandas as pd
import customtkinter
from styling import *
import math
from PIL import Image, ImageGrab
import io
import win32clipboard


class LazyQuestionToggleFrame(customtkinter.CTkFrame):

    def __init__(self, master, image_path):
        super().__init__(master)

        self.state = False
        self.image_loaded = False
        self.image_path = image_path

        self.grid_columnconfigure(0, weight=1)

        # Create a button to toggle the frame
        self.toggle_button = customtkinter.CTkButton(self,
                                                     text="Show Question",
                                                     command=self.toggle_image)
        self.toggle_button.grid(row=0,
                                column=0,
                                padx=10,
                                pady=PADDING,
                                sticky="ew")

    def load_image(self):
        self.frame_to_toggle = customtkinter.CTkFrame(self)
        self.frame_to_toggle.grid(row=1,
                                  column=0,
                                  padx=10,
                                  pady=5,
                                  sticky="nsew")
        print(f"Loading image: {self.image_path}")
        self.question_image = Image.open(self.image_path)
        self.original_width, self.original_height = self.question_image.size
        scale = 0.5
        self.ctk_image = customtkinter.CTkImage(
            self.question_image,
            size=(self.original_width * scale, self.original_height * scale))

        # Create a label for the image, initially hidden
        self.image_label = customtkinter.CTkLabel(self.frame_to_toggle,
                                                  image=self.ctk_image,
                                                  text="")
        self.image_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.image_label.bind("<Button-3>",
                              lambda e: self.copy_image_to_clipboard())
        self.image_loaded = True

        self.slider = customtkinter.CTkSlider(self.frame_to_toggle,
                                              orientation="horizontal")
        self.slider.bind(
            "<ButtonRelease-1>",
            lambda event: self.on_slider_change(self.slider.get()))
        self.slider.grid(row=1, column=0, padx=10, pady=PADDING, sticky="ew")

    def on_slider_change(self, value):
        if not self.image_loaded:
            return
        scale = float(value)
        self.ctk_image.configure(size=(self.original_width * scale,
                                       self.original_height * scale))

    def toggle_image(self):
        if not self.image_loaded:
            self.load_image()
        if self.state:
            self.frame_to_toggle.grid_remove()
            self.toggle_button.configure(text="Show Question")
        else:
            self.frame_to_toggle.grid()
            self.toggle_button.configure(text="Hide Question")
        self.state = not self.state

    def copy_image_to_clipboard(self):
        output = io.BytesIO()
        # Save the image to the stream in BMP format
        self.question_image.save(output, 'BMP')
        data = output.getvalue()[14:]  # Remove BMP header

        # Open the clipboard and set the data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        # Create a label to show the message
        info_label = customtkinter.CTkLabel(
            self,
            text="Image copied to clipboard!",
            bg_color="transparent",
            corner_radius=10,
        )
        # Place the label at a fixed position (e.g., bottom-right corner)
        info_label.place(relx=0.5, rely=0.5, anchor="center")

        # Schedule the label to be destroyed after the given duration (milliseconds)
        self.after(500, info_label.destroy)


class LazySolutionToggleFrame(customtkinter.CTkFrame):

    def __init__(self, master, image_path, answer):
        super().__init__(master)

        self.state = False
        self.image_loaded = False
        self.image_path = image_path
        self.answer = answer

        self.grid_columnconfigure(0, weight=1)

        # Create a button to toggle the frame
        self.toggle_button = customtkinter.CTkButton(self,
                                                     text="Show Solution",
                                                     command=self.toggle_image)
        self.toggle_button.grid(row=0,
                                column=0,
                                padx=10,
                                pady=PADDING,
                                sticky="ew")

    def load_image(self):
        self.frame_to_toggle = customtkinter.CTkFrame(self)
        self.frame_to_toggle.grid(row=1,
                                  column=0,
                                  padx=10,
                                  pady=5,
                                  sticky="nsew")
        self.answer_label = customtkinter.CTkLabel(self.frame_to_toggle,
                                                   text=self.answer,
                                                   font=(FONT, 16, "bold"))
        self.answer_label.grid(row=0,
                               column=0,
                               padx=10,
                               pady=PADDING,
                               sticky="w")

        print(f"Loading image: {self.image_path}")
        self.solution_image = Image.open(self.image_path)
        self.original_width, self.original_height = self.solution_image.size
        scale = 0.5
        self.ctk_image = customtkinter.CTkImage(
            self.solution_image,
            size=(self.original_width * scale, self.original_height * scale))

        # Create a label for the image, initially hidden
        self.image_label = customtkinter.CTkLabel(self.frame_to_toggle,
                                                  image=self.ctk_image,
                                                  text="")
        self.image_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.slider = customtkinter.CTkSlider(self.frame_to_toggle,
                                              orientation="horizontal")
        self.slider.bind(
            "<ButtonRelease-1>",
            lambda event: self.on_slider_change(self.slider.get()))
        self.slider.grid(row=2, column=0, padx=10, pady=PADDING, sticky="ew")

        self.image_loaded = True

    def on_slider_change(self, value):
        if not self.image_loaded:
            return
        scale = float(value)
        self.ctk_image.configure(size=(self.original_width * scale,
                                       self.original_height * scale))

    def toggle_image(self):
        if not self.image_loaded:
            self.load_image()
        if self.state:
            self.frame_to_toggle.grid_remove()
            self.slider.grid_remove()
            self.toggle_button.configure(text="Show Solution")
        else:
            self.frame_to_toggle.grid()
            self.slider.grid()
            self.toggle_button.configure(text="Hide Solution")
        self.state = not self.state


class QuestionCardFrame(customtkinter.CTkFrame):

    def __init__(self, master, year, paper, question, category, sub_category,
                 approach, answer, type, in_list, list_colors):
        border_color = customtkinter.ThemeManager.theme["CTkFrame"][
            "border_color"]
        super().__init__(master, border_color=border_color, border_width=1)

        row = 0
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        question_text = f"{year} {paper} Q{question}"
        question_label = customtkinter.CTkLabel(self,
                                                text=question_text,
                                                font=(FONT, 16, "bold"))
        question_label.grid(row=row,
                            column=0,
                            padx=10,
                            pady=2,
                            sticky="w",
                            columnspan=10)
        row += 1

        category_text = category + (f", {sub_category}"
                                    if not pd.isnull(sub_category) else "")
        category_label = customtkinter.CTkLabel(self,
                                                text=category_text,
                                                font=(FONT, 12, "bold"))
        category_label.grid(row=row, column=0, padx=10, pady=1, sticky="w")

        if not pd.isnull(type):
            type_label = customtkinter.CTkLabel(self,
                                                text=type,
                                                font=(FONT, 12))
            type_label.grid(row=row, column=1, padx=10, pady=1, sticky="e")

        if not pd.isnull(approach):
            approach_label = customtkinter.CTkLabel(self,
                                                    text=approach,
                                                    font=(FONT, 12))
            approach_label.grid(row=row, column=2, padx=10, pady=1, sticky="e")
        row += 1

        if len(in_list) > 0:
            in_list_frame = customtkinter.CTkFrame(self)
            in_list_frame.grid(row=0, column=2, padx=10, pady=1, sticky="e")
            for i in range(len(in_list)):
                in_list_label = customtkinter.CTkLabel(
                    in_list_frame,
                    text=in_list[i],
                    fg_color=list_colors[in_list[i]],
                    text_color="white",
                    font=(FONT, 16, "italic"))
                in_list_label.grid(row=0,
                                   column=0,
                                   padx=10,
                                   pady=1,
                                   sticky="e")

        self.image_path = f"TMUA_Questions/{year}{paper}/{question}.png"
        self.question_image_frame = LazyQuestionToggleFrame(
            self, self.image_path)
        self.question_image_frame.grid(row=row,
                                       column=0,
                                       padx=10,
                                       pady=PADDING,
                                       sticky="nsew",
                                       columnspan=10)
        row += 1

        self.solution_image_path = f"TMUA_Questions/{year}{paper}-solutions/{question}.png"
        self.solution_image_frame = LazySolutionToggleFrame(
            self, self.solution_image_path, answer=answer)
        self.solution_image_frame.grid(row=row,
                                       column=0,
                                       padx=10,
                                       pady=PADDING,
                                       sticky="nsew",
                                       columnspan=10)
        row += 1


class QuestionsFrame(customtkinter.CTkFrame):

    def __init__(self, master, questions, lists_files):
        super().__init__(master)

        self.questions_per_page = 10
        self.list_colors = {}
        for i, list_file in enumerate(lists_files):
            self.list_colors[list_file] = get_hex_colors_from_cmap(
                CMAP, len(lists_files))[i]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.update_questions(questions)

    def update_questions(self, questions, page=1):
        """
        questions: DataFrame containing the questions to display
        """
        for child in self.winfo_children():
            child.destroy()

        # pages
        self.num_questions = len(questions)
        question_start = (page - 1) * self.questions_per_page
        question_end = min(question_start + self.questions_per_page,
                           self.num_questions)
        print(
            f"Displaying questions {question_start} to {question_end-1} of {self.num_questions}"
        )
        self.num_pages = math.ceil(self.num_questions /
                                   self.questions_per_page)
        pages_frame = customtkinter.CTkFrame(self)
        for i in range(self.num_pages):
            page_button = customtkinter.CTkButton(
                pages_frame,
                text=f"{i + 1}" if i != page - 1 else f"[{i + 1}]",
                fg_color=customtkinter.ThemeManager.theme["CTkButton"]
                ["fg_color"] if i == page - 1 else
                customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"],
                text_color=customtkinter.ThemeManager.theme["CTkLabel"]
                ["text_color"] if i != page - 1 else
                customtkinter.ThemeManager.theme["CTkButton"]["text_color"],
                command=lambda i=i: self.update_questions(questions,
                                                          page=i + 1))
            pages_frame.grid_columnconfigure(i, weight=1)
            page_button.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
        pages_frame.grid(row=1, column=0, padx=10, pady=PADDING, sticky="nsew")

        # stats bar
        stats_frame = customtkinter.CTkFrame(self)
        stats_frame.grid(row=0, column=0, padx=10, pady=PADDING, sticky="nsew")
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=0)
        num_questions_label = customtkinter.CTkLabel(
            stats_frame,
            text=f"{self.num_questions} questions",
            font=(FONT, 12))
        num_questions_label.grid(row=0,
                                 column=0,
                                 padx=10,
                                 pady=PADDING,
                                 sticky="w")
        theme_button = customtkinter.CTkButton(stats_frame,
                                               text="Change Theme",
                                               command=self.change_theme)
        theme_button.grid(row=0, column=1, padx=10, pady=PADDING, sticky="e")

        # questions
        questions_scroll_frame = customtkinter.CTkScrollableFrame(self)
        questions_scroll_frame.grid(row=2,
                                    column=0,
                                    padx=10,
                                    pady=PADDING,
                                    sticky="nsew")
        questions_scroll_frame.grid_columnconfigure(0, weight=1)
        for i in range(self.questions_per_page):
            questions_scroll_frame.grid_rowconfigure(i, weight=1)

        for i in range(question_start, question_end):
            question_row = questions.iloc[i]
            question_frame = QuestionCardFrame(
                questions_scroll_frame,
                year=question_row.Year,
                paper=question_row.P,
                question=question_row.Q,
                category=question_row.Category,
                sub_category=question_row['Sub-Category'],
                approach=question_row['Approach'],
                type=question_row['Type'],
                in_list=question_row['in_list'],
                list_colors=self.list_colors,
                answer=question_row['Answer'])
            question_frame.grid(row=i,
                                column=0,
                                padx=0,
                                pady=PADDING / 2,
                                sticky="nsew")

    def change_theme(self):
        current = customtkinter.get_appearance_mode().lower()
        new = "dark" if current == "light" else "light"
        customtkinter.set_appearance_mode(new)
