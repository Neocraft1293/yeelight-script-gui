import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
import yeelight
import json

# Remplacez ceci par l'adresse IP de votre lampe Yeelight
ip_address = "192.168.0.239"

# Fonction pour établir la connexion à la lampe Yeelight en gérant les exceptions
def connect_to_bulb():
    try:
        bulb = yeelight.Bulb(ip_address)
        return bulb
    except yeelight.BulbException as e:
        print("Erreur lors de la connexion à la lampe Yeelight :", str(e))
        return None

# Connexion à la lampe Yeelight
bulb = connect_to_bulb()

# Fonction pour charger les préréglages depuis un fichier JSON
def load_presets(filename):
    try:
        with open(filename, "r") as file:
            presets = json.load(file)
        return presets
    except FileNotFoundError:
        return {}

# Charger les préréglages depuis un fichier JSON (présupposant que le fichier s'appelle "presets.json" dans le même répertoire)
presets = load_presets("presets.json")

# Fonction pour sauvegarder l'état actuel de la lampe dans un préréglage avec un nom personnalisé
def save_current_state_to_preset():
    preset_name = simpledialog.askstring("Sauvegarder le préréglage", "Entrez un nom pour le préréglage :")
    if preset_name:
        current_state = bulb.get_properties()

        # Convertir les données dans le format souhaité
        rgb_value = int(current_state["rgb"])
        converted_state = {
            "power": "on" if current_state["power"] == "on" else "off",
            "brightness": int(current_state["bright"]),
            "color_temp": int(current_state["ct"]),
            "rgb": [rgb_value & 255, (rgb_value >> 8) & 255, (rgb_value >> 16) & 255],
            "hue": int(current_state["hue"]),
            "sat": int(current_state["sat"]),
            "color_mode": int(current_state["color_mode"]),
            "flowing": int(current_state["flowing"]),
            "delayoff": int(current_state["delayoff"]),
            "music_on": int(current_state["music_on"])
        }
        print(rgb_value)
        print(current_state["rgb"])
        print(converted_state)

        presets[preset_name] = converted_state
        with open("presets.json", "w") as file:
            json.dump(presets, file, indent=4)
        print(f"Préréglage '{preset_name}' sauvegardé avec succès.")


# Fonction pour appliquer une configuration prédéfinie
def apply_preset(preset_key):
    preset = presets.get(preset_key)
    if preset:
        if "power" in preset:
            power = preset["power"]
            if power == "on":
                bulb.turn_on()
                print("Lampe allumée.")
            else:
                bulb.turn_off()
                print("Lampe éteinte.")
        if "rgb" in preset:
            rgb = preset["rgb"]
            bulb.set_rgb(rgb[2], rgb[1], rgb[0])
            print(f"Couleur RVB définie à ({rgb[2]}, {rgb[1]}, {rgb[0]}).")
        if "brightness" in preset:
            brightness = preset["brightness"]
            bulb.set_brightness(brightness)
            print(f"Luminosité définie à {brightness}.")
        #if "color_temp" in preset:
        #    color_temp = preset["color_temp"]
        #    bulb.set_color_temp(color_temp)
        #    print(f"Température de couleur définie à {color_temp}K.")

# Fonction pour ouvrir la liste des préréglages
def open_preset_list():
    preset_list_window = tk.Toplevel(root)
    preset_list_window.title("Liste des Préréglages")

    # Créez un bouton pour chaque préréglage
    for preset_key in presets:
        preset_button = tk.Button(preset_list_window, text=preset_key, command=lambda key=preset_key: apply_preset(key))
        preset_button.pack(pady=5)

# Fonction pour afficher l'état de la lampe dans une fenêtre séparée
def show_status(status):
    status_window = tk.Toplevel(root)
    status_window.title("État de la lampe")
    status_text = tk.Text(status_window, height=10, width=40)
    status_text.pack(pady=10)
    status_str = json.dumps(status, indent=4)
    status_text.insert(tk.END, status_str)

# Interface utilisateur
root = tk.Tk()
root.title("Contrôle de la lampe Yeelight")

# Bouton pour choisir la couleur
color_button = tk.Button(root, text="Choisir une couleur", command=lambda: bulb.set_rgb(*colorchooser.askcolor()[0]))
color_button.pack(pady=10)

# Bouton pour choisir la luminosité
brightness_button = tk.Button(root, text="Choisir la luminosité", command=lambda: bulb.set_brightness(simpledialog.askinteger("Luminosité", "Entrez une valeur de luminosité (1-100):", minvalue=1, maxvalue=100)))
brightness_button.pack(pady=10)

# Bouton pour allumer la lampe
on_button = tk.Button(root, text="Allumer", command=lambda: [bulb.turn_on(), print("Lampe allumée.")])
on_button.pack(pady=10)

# Bouton pour éteindre la lampe
off_button = tk.Button(root, text="Éteindre", command=lambda: [bulb.turn_off(), print("Lampe éteinte.")])
off_button.pack(pady=10)

# Bouton pour sauvegarder l'état actuel de la lampe
save_button = tk.Button(root, text="Sauvegarder l'état actuel", command=save_current_state_to_preset)
save_button.pack(pady=10)

# Bouton pour afficher l'état de la lampe
status_button = tk.Button(root, text="Afficher l'état de la lampe", command=lambda: [show_status(bulb.get_properties()), print("État de la lampe affiché.")])
status_button.pack(pady=10)

# Bouton pour ouvrir la liste des préréglages
presets_button = tk.Button(root, text="Préréglages", command=lambda: [open_preset_list(), print("Liste des préréglages ouverte.")])
presets_button.pack(pady=10)



# Boucle principale de la fenêtre
root.mainloop()
