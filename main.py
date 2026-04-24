import customtkinter as ctk
from login_gui import LoginWindow
from app_gui import AppWindow

# Tema global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def iniciar():
    def on_login(usuario):
        app = AppWindow(usuario)
        app.mainloop()

    login = LoginWindow(on_login_success=on_login)
    login.mainloop()

if __name__ == "__main__":
    iniciar()
