__author__ = 'amirbar'

import os
import random
import sys

# Load correct package for python 3.0 or higher
if sys.version_info > (3, 0):
    from tkinter import *
else:
    from Tkinter import *

ROUNDS_PER_GAME = 20
CHOICES_NUM = 4
TEXT_POS = 0
IMG_POS = 1


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Define a container to show the different pages
        container = Frame(self)
        container.pack(side=TOP, fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Define the window properties
        self.geometry("700x500+200+200")
        self.title("Functional group games")

        self.frames = {}

        self.load_data()

        # Add all the pages
        for frame_type in [MainPage]:
            frame = frame_type(container, self)
            self.frames[frame_type] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        for frame_type in [NameToGroupPage, GroupToNamePage]:
            frame = frame_type(container, self, self.names_and_pictures)
            self.frames[frame_type] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def load_data(self):
        directory = os.path.dirname(__file__)
        groups_and_paths = [("Methyl", os.path.join(directory, "pics", "methyl.gif")),
                            ("Ethyl", os.path.join(directory, "pics", "ethyl.gif")),
                            ("Phenyl", os.path.join(directory, "pics", "phenyl.gif")),
                            ("Carbonyl (aldehyde)", os.path.join(directory, "pics", "carbonyl-aldehyde.gif")),
                            ("Carbonyl (ketone)", os.path.join(directory, "pics", "carbonyl-ketone.gif")),
                            ("Carboxylate", os.path.join(directory, "pics", "carboxylate.gif")),
                            ("Hydroxyl", os.path.join(directory, "pics", "hydroxyl.gif")),
                            ("Enol", os.path.join(directory, "pics", "enol.gif")),
                            ("Ether", os.path.join(directory, "pics", "ether.gif")),
                            ("Ester", os.path.join(directory, "pics", "ester.gif")),
                            ("Acetyl", os.path.join(directory, "pics", "acetyl.gif")),
                            ("Anhydride", os.path.join(directory, "pics", "anhydride.gif")),
                            ("Amino", os.path.join(directory, "pics", "amino.gif")),
                            ("Amido", os.path.join(directory, "pics", "amido.gif")),
                            ("Imine", os.path.join(directory, "pics", "imine.gif")),
                            ("N-Substituted Imine", os.path.join(directory, "pics", "n-substituted-imine.gif")),
                            ("Guanidinium", os.path.join(directory, "pics", "guanidinium.gif")),
                            ("Imidazole", os.path.join(directory, "pics", "imidazole.gif")),
                            ("Sulfhydryl", os.path.join(directory, "pics", "sulfhydryl.gif")),
                            ("Disulfide", os.path.join(directory, "pics", "disulfide.gif")),
                            ("Thioester", os.path.join(directory, "pics", "thioester.gif")),
                            ("Phosphoryl", os.path.join(directory, "pics", "phosphoryl.gif")),
                            ("Phosphoanhydride", os.path.join(directory, "pics", "phosphoanhydride.gif")),
                            ("Mixed Anhydride", os.path.join(directory, "pics", "mixed-anhydride.gif"))]

        self.names_and_pictures = [(group_name, PhotoImage(file=path)) for group_name, path in groups_and_paths]
            #self.label = Label(self, image=img)
            #self.label.image = img

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.on_switch()

class Page(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

    def on_switch(self):
        raise NotImplementedError


class MainPage(Page):

    def __init__(self, parent, controller):

        Page.__init__(self, parent)
        self.controller = controller

        self.pages = [NameToGroupPage,
                      GroupToNamePage]

        buttons_texts = ["Match the functional group name to the picture",
                         "Match the picture to the functional group name"]

        # Generate the multiple options choice
        self.radio_choice = IntVar()

        for index, text in enumerate(buttons_texts):
            option = Radiobutton(self,
                                 text=text,
                                 variable=self.radio_choice,
                                 value=index,
                                 command=self.update_button_page)
            option.pack(side=TOP, anchor="w")

        self.radio_choice.set(0)

        # Add a button to go next page
        self.start_button = Button(self,
                                   text="Play",
                                   command=lambda: self.controller.show_frame(self.pages[self.radio_choice.get()]))
        self.start_button.pack(side=BOTTOM)

    def update_button_page(self):

        self.start_button.configure(command=lambda: self.controller.show_frame(self.pages[self.radio_choice.get()]))

    def on_switch(self):

        pass

class NameToGroupPage(Page):
    def __init__(self, parent, controller, names_and_pictures):
        Page.__init__(self, parent)

        self.names_and_pictures = names_and_pictures

        label = Label(self, text="Match the functional group name to the picture")
        label.grid(row=0, column=0)

        self.points_label = Label(self, text="points: 0")
        self.points_label.grid(row=0, column=3)

        self.answer_status_label = Label(self)
        self.answer_status_label.grid(row=1, column=0)

        # random next question
        self.asked_text, self.result_id, self.options_image = self.random_question()

        self.question_label = Label(self, text="which one is %s?" % self.asked_text)
        self.question_label.grid(row=2, column=0)

        self.choice = IntVar()
        self.choice.set(0)

        # Generate the multiple options choice

        self.option_1 = Radiobutton(self,
                                    image=self.options_image[0],
                                    variable=self.choice,
                                    command=self.commit_answer,
                                    value=0)
        self.option_1.grid(row=5, column=0)

        self.option_2 = Radiobutton(self,
                                    image=self.options_image[1],
                                    variable=self.choice,
                                    command=self.commit_answer,
                                    value=1)
        self.option_2.grid(row=5, column=5)

        self.option_3 = Radiobutton(self,
                                    image=self.options_image[2],
                                    variable=self.choice,
                                    command=self.commit_answer,
                                    value=2)
        self.option_3.grid(row=10, column=0)

        self.option_4 = Radiobutton(self,
                                    image=self.options_image[3],
                                    variable=self.choice,
                                    command=self.commit_answer,
                                    value=3)
        self.option_4.grid(row=10, column=5)

        # Add a button to go back
        start_button = Button(self, text="Back to main page", command=lambda: controller.show_frame(MainPage))
        start_button.grid(row=20, column=0)

    def on_switch(self):
        self.score = 0
        self.points_label.configure(text="points %d" % self.score)
        self.answer_status_label.configure(text="")
        self.rounds_left = ROUNDS_PER_GAME
        self.option_1.configure(state="normal")
        self.option_2.configure(state="normal")
        self.option_3.configure(state="normal")
        self.option_4.configure(state="normal")

    def commit_answer(self):

        # Update points
        if self.choice.get() == self.result_id:
            self.score += 1
            self.points_label.configure(text="points %d" % self.score)
            self.answer_status_label.configure(text="Correct!")
        else:
            self.answer_status_label.configure(text="Wrong!")

        # Advance next round
        self.rounds_left -= 1

        # Random next question
        if self.rounds_left > 0:
            self.asked_text, self.result_id, self.options_image = self.random_question()

            # update radio buttons and set result value
            self.question_label.configure(text="which one is %s?" % self.asked_text)
            self.option_1.configure(image=self.options_image[0])
            self.option_2.configure(image=self.options_image[1])
            self.option_3.configure(image=self.options_image[2])
            self.option_4.configure(image=self.options_image[3])

        # Game finished
        else:
            self.option_1.configure(state="disabled")
            self.option_2.configure(state="disabled")
            self.option_3.configure(state="disabled")
            self.option_4.configure(state="disabled")

    def random_question(self):

        answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

        asked_text = answer[TEXT_POS]
        result_id = random.randint(1, CHOICES_NUM) - 1

        options = []

        for i in range(0, CHOICES_NUM):

            # Add correct answer at random place
            if i == result_id:
                options.append(answer[IMG_POS])

            # Random Wrong answer
            else:
                wrong_answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

                while wrong_answer == answer or wrong_answer[IMG_POS] in options:
                    wrong_answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

                options.append(wrong_answer[IMG_POS])


        return asked_text, result_id, options

class GroupToNamePage(Page):
    def __init__(self, parent, controller, names_and_pictures):
        Page.__init__(self, parent)

        self.names_and_pictures = names_and_pictures

        label = Label(self, text="Match the picture to the functional group name")
        label.grid(row=0, column=0)


        self.points_label = Label(self, text="points: 0")
        self.points_label.grid(row=0, column=3)

        self.answer_status_label = Label(self)
        self.answer_status_label.grid(row=1, column=0)

        # random next question
        self.asked_image, self.result_id, self.options_text = self.random_question()

        self.question_text = Label(self, text="Which functional group match the following:")
        self.question_text.grid(row=2, column=0)
        self.question_label = Label(self, image=self.asked_image)
        self.question_label.grid(row=3, column=0)

        self.choice = IntVar()
        self.choice.set(0)

        # Generate the multiple options choice

        self.option_1 = Radiobutton(self,
                             text=self.options_text[0],
                             variable=self.choice,
                             value=0)
        self.option_1.grid(row=5, column=0)

        self.option_2 = Radiobutton(self,
                             text=self.options_text[1],
                             variable=self.choice,
                             value=1)
        self.option_2.grid(row=5, column=5)

        self.option_3 = Radiobutton(self,
                             text=self.options_text[2],
                             variable=self.choice,
                             value=2)
        self.option_3.grid(row=10, column=0)

        self.option_4 = Radiobutton(self,
                             text=self.options_text[3],
                             variable=self.choice,
                             value=3)
        self.option_4.grid(row=10, column=5)

        # Add commit answer button
        self.commit_button = Button(self, text="commit", command=self.commit_answer)
        self.commit_button.grid(row=19, column=0)

        # Add a button to go back
        start_button = Button(self, text="Back to main page", command=lambda: controller.show_frame(MainPage))
        start_button.grid(row=20, column=0)

    def on_switch(self):
        self.score = 0
        self.points_label.configure(text="points %d" % self.score)
        self.rounds_left = ROUNDS_PER_GAME
        self.commit_button.configure(state="normal")

    def commit_answer(self):

        # Update points
        if self.choice.get() == self.result_id:
            self.score += 1
            self.points_label.configure(text="points %d" % self.score)
            self.answer_status_label.configure(text="Correct!")
        else:
            self.answer_status_label.configure(text="Wrong!")

        # Advance next round
        self.rounds_left -= 1

        # Random next question
        if self.rounds_left > 0:
            self.asked_image, self.result_id, self.options_text = self.random_question()

            # update radio buttons and set result value
            self.question_label.configure(image=self.asked_image)
            self.option_1.configure(text=self.options_text[0])
            self.option_2.configure(text=self.options_text[1])
            self.option_3.configure(text=self.options_text[2])
            self.option_4.configure(text=self.options_text[3])

        # Game finished
        else:
            self.commit_button.configure(state="disabled")

    def random_question(self):

        answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

        asked_image = answer[IMG_POS]
        result_id = random.randint(1, CHOICES_NUM) - 1

        options = []

        for i in range(0, CHOICES_NUM):

            # Add correct answer at random place
            if i == result_id:
                options.append(answer[TEXT_POS])

            # Random Wrong answer
            else:
                wrong_answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

                while wrong_answer == answer or wrong_answer[TEXT_POS] in options:
                    wrong_answer = self.names_and_pictures[random.randint(1, len(self.names_and_pictures)) - 1]

                options.append(wrong_answer[TEXT_POS])


        return asked_image, result_id, options


app = App()
app.mainloop()
