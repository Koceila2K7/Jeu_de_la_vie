import tkinter as tk
import customtkinter
import os
from PIL import Image

COULEUR_QUADR = "grey60"
DEFAULT_DEAD_CELL_COLOR = "#FFFFFF"
DEFAULT_ALIVE_CELL_COLOR = "#000000"

LARGEUR = 320
HAUTEUR = 320
COTE = 20
NB_COL = LARGEUR // COTE
NB_LIG = HAUTEUR // COTE


DESCRIPTION = """
Codé par Koceila, Nabil et Anis. Licence Apache2.0. Paris-Saclay
"""


def from_matrix_to_str(tableau: list[list[int]]) -> str:
    final_result = ""

    for i in range(len(tableau)):
        line_result = ''
        for j in range(len(tableau[0])):
            v = tableau[i][j] if tableau[i][j] == 0 else 1
            if line_result == '':
                line_result = str(v)
            else:
                line_result = line_result+' '+str(v)

        if final_result == '':
            final_result = line_result
        else:
            final_result = final_result + '; '+line_result

    return final_result


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.tableau = []
        self.reset_tableau()
        self.title("image_example.py")
        self.geometry("750x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "./test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(
            image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, "paris-saclay-logo.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        self.add_grille_image = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, "edit-tools.png")), size=(20, 20))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Koceila Nabil Anis", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="A propos",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)

        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(
            row=0, column=0, padx=20, pady=10)
        self.grid_names = self.get_map_file_names()
        self.selected_value = self.grid_names[0]

        self.select_map_menu = customtkinter\
            .CTkOptionMenu(self.home_frame,
                           values=self.grid_names,
                           command=self.set_selected_value)

        self.select_map_menu.grid(row=3, column=0, padx=20, pady=10)

        self.select_mode_d_execution = "Mode avec barrière"

        self.select_mode_d_execution_menu = customtkinter\
            .CTkOptionMenu(self.home_frame,
                           values=["Mode avec barrière", "Mode sans barrière"],
                           command=self.set_mode_d_execution)

        self.select_mode_d_execution_menu.grid(
            row=4, column=0, padx=20, pady=10)

        self.entry_tour_nbr = customtkinter.CTkEntry(
            self.home_frame, placeholder_text="Nombre de tours")

        self.entry_tour_nbr.grid(
            row=5, column=0, padx=20, pady=10, sticky="nsew")

        self.home_frame_button_start_game = customtkinter.CTkButton(
            self.home_frame, text="Démarrer", compound="right", command=self.lancement_de_la_grille)

        self.home_frame_button_start_game.grid(
            row=6, column=0, padx=20, pady=10)

        self.home_frame_button_2 = customtkinter.CTkButton(
            self.home_frame, text="Creer une autre grille",
            image=self.add_grille_image, compound="right", command=self.set_create_map_frame)

        self.home_frame_button_2.grid(row=7, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.canvas = tk.Canvas(
            self.second_frame, bg=DEFAULT_DEAD_CELL_COLOR, width=LARGEUR, height=HAUTEUR)
        self.canvas.grid()
        self.canvas.bind("<Button-1>", self.chg_case)
        self.quadrillage()
        self.button_validate_creation = customtkinter.CTkButton(
            self.second_frame, text="Valider", compound="right", command=self.validation_creation_de_grille)

        self.entry = customtkinter.CTkEntry(
            self.second_frame, placeholder_text="Donnez un titre")

        self.entry.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.button_validate_creation.grid(row=5, column=0, padx=20, pady=10)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.text_view = customtkinter.CTkLabel(self.third_frame, text=DESCRIPTION,
                                                )
        self.text_view.grid(row=0, column=0, )
        # select default frame
        self.select_frame_by_name("home")
        customtkinter.set_appearance_mode("Dark")

    def set_mode_d_execution(self, x):
        self.select_mode_d_execution = x

    def set_selected_value(self, x):
        self.selected_value = x

    def get_map_file_names(self):
        from os import listdir
        directory = "../assets/maps"
        return [f.replace('.json', '') for f in listdir(directory) if f.endswith('.json')]

    def reset_tableau(self):
        for _ in range(NB_COL):
            self.tableau.append([0] * NB_LIG)

    def xy_to_ij(self, x, y):
        """Retourne la colonne et la ligne du tableau correspondant aux coordonnées (x,y) du canevas"""
        # A FAIRE
        return x // COTE, y // COTE

    def chg_case(self, event):
        """Modifier l'état de la case aux coordonnées (event.x, event.y)"""
        i, j = self.xy_to_ij(event.x, event.y)
        try:
            if self.tableau[i][j] > 0:
                # si case vivante
                self.canvas.delete(self.tableau[i][j])
                self.tableau[i][j] = 0
            else:
                # si case morte
                x, y = COTE * i, COTE * j
                carre = self.canvas.create_rectangle(
                    (x, y), (x + COTE, y + COTE), fill=DEFAULT_ALIVE_CELL_COLOR,
                    outline=COULEUR_QUADR)
                self.tableau[i][j] = carre
        except IndexError:
            # Gestion des petits dépacement à cause de la taille des ligne de grille
            pass

    def reset_canva(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[0])):
                self.canvas.delete(self.tableau[i][j])
                self.tableau[i][j] = 0

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.reset_tableau()
            self.reset_canva()
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_3")

    def set_create_map_frame(self):
        self.select_frame_by_name("frame_2")

    def quadrillage(self):
        """Affiche un quadrillage constitué de carrés de côté COTE"""
        y = 0
        while y <= HAUTEUR:
            self.canvas.create_line((0, y), (LARGEUR, y), fill=COULEUR_QUADR)
            y += COTE
        x = 0
        while x <= LARGEUR:
            self.canvas.create_line((x, 0), (x, HAUTEUR), fill=COULEUR_QUADR)
            x += COTE

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def validation_creation_de_grille(self):
        import json
        new_map = {'map': from_matrix_to_str(self.tableau)}
        with open('../assets/maps/'+str(self.entry.get())+".json", 'w',
                  encoding='utf8') as \
                json_file:
            json.dump(new_map, json_file)
        self.grid_names = self.get_map_file_names()

        self.select_map_menu.configure(values=self.grid_names)

    def lancement_de_la_grille(self):
        import threading

        def thread_target(selected_value, mode, nb_tour_str):
            import subprocess
            nb_tour = 10
            try:
                nb_tour = int(nb_tour_str)
            except:
                pass

            cmd_base = 'python'
            args = ".\display test_numero2 1"
            p = subprocess.Popen(
                [cmd_base, '.\display.py', selected_value, mode, str(nb_tour)])

        threading.Thread(target=thread_target, args=(
            self.selected_value, "1" if self.select_mode_d_execution == "Mode avec barrière" else "0", self.entry_tour_nbr.get())).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
