import tkinter as tk
import os
import ctypes
from PIL import Image, ImageTk

CANDIDATES = {
    "13": {"name": "LULA", "party": "PT", "image": "images/lula.webp"},
    "14": {"name": "RENAN SANTOS", "party": "MISSÃO", "image": "images/renan.jpg"},
    "22": {"name": "FLÁVIO BOLSONARO", "party": "PL", "image": "images/flavio.jpg"},
    "30": {"name": "ROMEU ZEMA", "party": "NOVO", "image": "images/romeu.jpg"},
    "55": {"name": "RONALDO CAIADO", "party": "PSD", "image": "images/Ronaldo.jpg"},
}

SOUND_BOTOES = os.path.abspath("sound/botoes_audio.mp3")
SOUND_CONFIRMA = os.path.abspath("sound/confirma_audio.mp3")

def play_sound(file_path):
    if not os.path.exists(file_path):
        return
    short_path = ctypes.create_unicode_buffer(260)
    ctypes.windll.kernel32.GetShortPathNameW(file_path, short_path, 260)
    path = short_path.value
    
    ctypes.windll.winmm.mciSendStringW(f"close {path}", None, 0, 0)
    ctypes.windll.winmm.mciSendStringW(f"open {path} type mpegvideo alias {path}", None, 0, 0)
    ctypes.windll.winmm.mciSendStringW(f"play {path}", None, 0, 0)

class UrnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Urna Eletrônica")
        
        self.bg_image_pil = Image.open("images/urna.png")
        self.bg_width, self.bg_height = self.bg_image_pil.size
        
        self.root.geometry(f"{self.bg_width}x{self.bg_height}")
        self.root.resizable(False, False)

        self.bg_image = ImageTk.PhotoImage(self.bg_image_pil)
        
        self.canvas = tk.Canvas(self.root, width=self.bg_width, height=self.bg_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.current_digits = ""
        self.is_voted = False
        self.is_branco = False

        self.setup_ui()

    def setup_ui(self):
        
        self.screen_frame = tk.Frame(self.canvas, bg="white", width=405, height=254)
        self.screen_frame.place(x=27, y=146)
        self.screen_frame.pack_propagate(False) # Prevent shrinking

        self.setup_screen()
        self.setup_invisible_buttons()

    def setup_screen(self):
        self.status_label = tk.Label(self.screen_frame, text="PRESIDENTE", font=("Arial", 12, "bold"), bg="white", anchor="w")
        self.status_label.place(x=10, y=10)

        self.digits_label = tk.Label(self.screen_frame, text="", font=("Courier", 32, "bold"), bg="white", bd=2, relief="solid", width=5)
        self.digits_label.place(x=10, y=50)

        self.name_label = tk.Label(self.screen_frame, text="", font=("Arial", 12), bg="white", anchor="w", justify="left", wraplength=250)
        self.name_label.place(x=10, y=110)

        self.party_label = tk.Label(self.screen_frame, text="", font=("Arial", 12), bg="white", anchor="w", justify="left", wraplength=250)
        self.party_label.place(x=10, y=150)

        self.photo_label = tk.Label(self.screen_frame, bg="white")
        self.photo_label.place(x=270, y=10)

        self.footer_label = tk.Label(self.screen_frame, text="Aperte a tecla:\nCONFIRMA para CONFIRMAR\nCORRIGE para REINICIAR", 
                                     font=("Arial", 8), bg="white", justify="left")
        self.footer_label.place(x=10, y=210)
        self.footer_label.place_forget()

        self.votou_label = tk.Label(self.screen_frame, text="FIM", font=("Arial", 60, "bold"), bg="white", fg="black")
        self.votou_label.place(relx=0.5, rely=0.5, anchor="center")
        self.votou_label.place_forget()

    def setup_invisible_buttons(self):
        
        btn_config = {
            'bg': '', 'activebackground': '', 'bd': 0, 'highlightthickness': 0, 'relief': 'flat',
        }

        key_coords = {
            '1': (515, 187, 42, 35), '2': (572, 187, 42, 35), '3': (628, 187, 42, 35),
            '4': (515, 235, 42, 35), '5': (572, 235, 42, 35), '6': (628, 235, 42, 35),
            '7': (515, 283, 42, 35), '8': (572, 283, 42, 35), '9': (628, 283, 42, 35),
            '0': (572, 330, 42, 35),
            'BRANCO': (488, 378, 61, 33),
            'CORRIGE': (565, 378, 60, 33),
            'CONFIRMA': (640, 369, 61, 42)
        }

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.key_coords = key_coords

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        for key, (bx, by, bw, bh) in self.key_coords.items():
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.animate_click(bx, by, bw, bh)
                self.handle_keypress(key)
                break

    def animate_click(self, x, y, w, h):
        overlay = self.canvas.create_rectangle(x, y, x+w, y+h, outline="black", width=4)
        self.root.after(120, lambda: self.canvas.delete(overlay))

    def handle_keypress(self, key):
        if key in '0123456789':
            self.press_digit(key)
        elif key == 'BRANCO':
            self.press_white()
        elif key == 'CORRIGE':
            self.press_correct()
        elif key == 'CONFIRMA':
            self.press_confirm()

    def press_digit(self, digit):
        if self.is_voted or self.is_branco or len(self.current_digits) >= 2:
            return
        
        play_sound(SOUND_BOTOES)
        self.current_digits += digit
        self.update_screen()

    def press_white(self):
        if self.is_voted:
            return
        
        play_sound(SOUND_BOTOES)
        self.is_branco = True
        self.current_digits = ""
        self.update_screen()

    def press_correct(self):
        if self.is_voted:
            return
        
        play_sound(SOUND_BOTOES)
        self.current_digits = ""
        self.is_branco = False
        self.update_screen()

    def press_confirm(self):
        if self.is_voted:
            return
        
        is_valid = self.is_branco or (len(self.current_digits) == 2)
        
        if is_valid:
            play_sound(SOUND_CONFIRMA)
            self.show_voted()

    def update_screen(self):
        self.digits_label.config(text=self.current_digits.ljust(2, "_"))
        self.name_label.config(text="")
        self.party_label.config(text="")
        self.photo_label.config(image="")
        self.footer_label.place_forget()

        if self.is_branco:
            self.digits_label.config(text="")
            self.name_label.config(text="VOTO EM BRANCO", font=("Arial", 18, "bold"))
            self.footer_label.place(x=10, y=210)
        elif len(self.current_digits) == 2:
            candidate = CANDIDATES.get(self.current_digits)
            if candidate:
                self.name_label.config(text=f"Nome: {candidate['name']}")
                self.party_label.config(text=f"Partido: {candidate['party']}")
                try:
                    img = Image.open(candidate['image'])
                    img = img.resize((100, 130))
                    self.photo = ImageTk.PhotoImage(img)
                    self.photo_label.config(image=self.photo)
                except:
                    pass
                self.footer_label.place(x=10, y=210)
            else:
                self.name_label.config(text="NÚMERO ERRADO", font=("Arial", 16))
                self.party_label.config(text="VOTO NULO")
                self.footer_label.place(x=10, y=210)

    def show_voted(self):
        self.is_voted = True
        for widget in self.screen_frame.winfo_children():
            widget.place_forget()
        
        self.votou_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(3000, self.reset_all)

    def reset_all(self):
        self.is_voted = False
        self.is_branco = False
        self.current_digits = ""
        self.votou_label.place_forget()
        
        self.status_label.place(x=10, y=10)
        self.digits_label.place(x=10, y=50)
        self.name_label.place(x=10, y=110)
        self.party_label.place(x=10, y=150)
        self.photo_label.place(x=270, y=10)
        
        self.update_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = UrnaApp(root)
    root.mainloop()
