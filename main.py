from customtkinter import *
from PIL import Image
from words import word_list
from random import shuffle


class TypingTest:
    def __init__(self):
        self.time = 15
        self.preset_time = 15
        self.timer = None

        self.number_word = 0
        self.word_list = word_list
        shuffle(self.word_list)
        self.typing_list = []

        self.correct = 0
        self.incorrect = 0
        self.change_color = None

        set_default_color_theme("theme/custom_theme.json")

        self.app = CTk(fg_color="#262a33")
        self.app.title("Typing Test")
        self.app.iconbitmap("img/icon.ico")
        self.app.geometry("650x500")

        self.frame = CTkFrame(self.app, fg_color="transparent")
        self.frame.pack(padx=40, pady=40)

        self.show_word = CTkLabel(self.frame, text=self.word_list[self.number_word], font=CTkFont(size=24),
                                  text_color="#e5f7ef")
        self.show_word.grid(column=0, row=2, columnspan=2, pady=(0, 40))

        self.show_next_word = CTkLabel(self.frame, text=self.word_list[self.number_word + 1], font=CTkFont(size=24),
                                       text_color="#526777")
        self.show_next_word.grid(column=2, row=2, columnspan=2, pady=(0, 40))

        self.label_count = CTkLabel(self.frame, text=f"{self.preset_time}", text_color="#43ffaf")
        self.label_count.grid(column=0, row=3)

        self.entry_word = CTkEntry(self.frame, state="disabled", width=160)
        self.entry_word.grid(column=1, row=3, columnspan=2)

        self.label_result = CTkLabel(self.frame, text="", text_color="#e5f7ef", font=CTkFont(size=24), anchor="e")
        self.label_result.grid(column=1, row=4, pady=(40, 0))

        self.result = CTkLabel(self.frame, text="", text_color="#43ffaf", font=CTkFont(size=24), anchor="w")
        self.result.grid(column=2, row=4, pady=(40, 0))

    def create_gui(self):
        icon = CTkImage(Image.open("img/icon.ico"), size=(40, 40))
        icon = CTkLabel(self.frame, text="", image=icon, width=icon.cget("size")[0], height=icon.cget("size")[1])
        icon.grid(column=0, row=0, pady=(10, 40))

        title = CTkLabel(self.frame, text="Typing Test", font=CTkFont(size=36))
        title.grid(column=1, row=0, columnspan=3, pady=(10, 40))

        fifteen_seconds = CTkButton(self.frame, text="15", font=CTkFont(weight="bold"), width=70,
                                    command=lambda: self.select_timer(15))
        fifteen_seconds.grid(column=0, row=1, pady=(0, 60), padx=10)

        thirty_seconds = CTkButton(self.frame, text="30", font=CTkFont(weight="bold"), width=70,
                                   command=lambda: self.select_timer(30))
        thirty_seconds.grid(column=1, row=1, pady=(0, 60), padx=10)

        one_minute = CTkButton(self.frame, text="60", font=CTkFont(weight="bold"), width=70,
                               command=lambda: self.select_timer(60))
        one_minute.grid(column=2, row=1, pady=(0, 60), padx=10)

        two_minutes = CTkButton(self.frame, text="120", font=CTkFont(weight="bold"), width=70,
                                command=lambda: self.select_timer(120))
        two_minutes.grid(column=3, row=1, pady=(0, 60), padx=10)

        start_button = CTkButton(self.frame, text="Start", width=70, command=self.preset)
        start_button.grid(column=3, row=3)

    def next_word(self, event):
        typed_word = self.entry_word.get().strip(" ")
        self.typing_list.append(typed_word)
        self.entry_word.delete(0, END)

        if typed_word == self.word_list[self.number_word]:
            self.correct += 1
            self.show_response("Correct")
        else:
            self.incorrect += 1
            self.show_response("Incorrect")

        self.number_word += 1
        self.show_word.configure(text=self.word_list[self.number_word])
        self.show_next_word.configure(text=self.word_list[self.number_word + 1])

    def back_word(self, event):
        current_position = self.entry_word.index(INSERT)
        if self.number_word > 0 and current_position == 0:
            if self.word_list[self.number_word - 1] != self.typing_list[self.number_word - 1]:
                self.number_word -= 1
                self.show_word.configure(text=self.word_list[self.number_word])
                self.show_next_word.configure(text=self.word_list[self.number_word + 1])

                self.entry_word.insert(0, self.typing_list[self.number_word])
                self.typing_list.remove(self.typing_list[self.number_word])

    def show_response(self, response=None):
        if response == "Correct":
            self.entry_word.configure(border_color="#43ffaf")
        elif response == "Incorrect":
            self.entry_word.configure(border_color="#ff5f5f")
        else:
            self.entry_word.configure(border_color="#e5f7ef")
            self.app.after_cancel(self.change_color)

        self.change_color = self.app.after(200, self.show_response)

    def select_timer(self, time):
        self.preset_time = time
        self.label_count.configure(text=str(time))
        try:
            self.app.after_cancel(self.timer)
            self.entry_word.configure(state="disabled")
        except ValueError:
            pass

    def preset(self):
        shuffle(self.word_list)

        self.entry_word.configure(state="normal")
        self.entry_word.delete(0, END)
        self.entry_word.focus()

        self.show_word.configure(text=self.word_list[0])
        self.show_next_word.configure(text=self.word_list[1])

        self.time = self.preset_time
        self.typing_list = []

        self.result.configure(text="")
        self.label_result.configure(text="")

        self.number_word = 0

        try:
            self.app.after_cancel(self.timer)
        except ValueError:
            self.entry_word.bind("<space>", self.next_word)
            self.entry_word.bind("<BackSpace>", self.back_word)

        def start_test():
            self.time -= 1
            self.label_count.configure(text=str(self.time))
            if self.time > 0:
                self.timer = self.app.after(1000, start_test)
            else:
                self.entry_word.configure(state="disabled")
                total_words = len(self.typing_list)
                try:
                    accuracy = round(self.correct / total_words * 100, 2)
                    wpm = total_words * (60 / self.preset_time)
                    total_characters = 0
                    for word in self.typing_list:
                        total_characters += len(word)
                    cpm = total_characters * (60 / self.preset_time)
                except ZeroDivisionError:
                    accuracy = 100
                    wpm = 0
                    cpm = 0
                self.label_result.configure(text="wpm\ncpm\nacc")
                self.result.configure(text=f"{wpm}\n{cpm}\n{accuracy}%")

        start_test()

    def run(self):
        self.app.mainloop()


app = TypingTest()
app.create_gui()
app.run()
