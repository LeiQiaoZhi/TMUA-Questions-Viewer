import customtkinter
from data import TMUADataLoader
from filters import FilterBarFrame
from styling import *
from questions import QuestionsFrame


class App(customtkinter.CTk):

    def __init__(self, data_loader):
        super().__init__()
        self.data_loader = data_loader

        self.title("TMUA Data Viewer")
        self.geometry("1000x1000")
        self.grid_columnconfigure(0, weight=0, minsize=200)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self.filterbar_frame = FilterBarFrame(self,
                                              data_loader.get_filter_options())
        self.filterbar_frame.grid(row=0,
                                  column=0,
                                  padx=(PADDING, PADDING / 2),
                                  pady=PADDING,
                                  sticky="nsew")

        self.question_frame = QuestionsFrame(self,
                                             data_loader.get_all_questions(),
                                             data_loader.lists_files)
        self.question_frame.grid(row=0,
                                 column=1,
                                 padx=(PADDING / 2, PADDING),
                                 pady=PADDING,
                                 sticky="nsew")

    def on_filter_button_click(self):
        selected_options = self.filterbar_frame.get_selected_options()
        print(selected_options)
        filtered_questions = self.data_loader.get_filtered_questions(
            selected_options)
        print(f"filtered: {len(filtered_questions)}")
        self.question_frame.update_questions(filtered_questions)


customtkinter.set_default_color_theme("dark-blue")
data_loader = TMUADataLoader("questions.csv")
app = App(data_loader)
app.mainloop()
