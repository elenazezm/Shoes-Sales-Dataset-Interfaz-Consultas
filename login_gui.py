import customtkinter as ctk
from tkinter import messagebox
import os

USUARIOS_PATH = "data/usuarios.txt"

def cargar_usuarios():
    """Lee usuarios desde archivo usuario:contraseña"""
    usuarios = {}
    if not os.path.exists(USUARIOS_PATH):
        messagebox.showerror("Error", f"No se encontró {USUARIOS_PATH}")
        return usuarios
    with open(USUARIOS_PATH, "r") as f:
        for linea in f:
            linea = linea.strip()
            if ":" in linea:
                user, pwd = linea.split(":", 1)
                usuarios[user.strip()] = pwd.strip()
    return usuarios


class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.usuarios = cargar_usuarios()

        self.title("Shoes Sales — Iniciar Sesión")
        self.geometry("420x500")
        self.resizable(False, False)

        # ── Frame central ──────────────────────────────────────────────────
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        ctk.CTkLabel(frame, text="", font=("Arial", 48)).pack(pady=(30, 0))
        ctk.CTkLabel(frame, text="Shoes Sales Analytics",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(8, 4))
        ctk.CTkLabel(frame, text="Accede con tus credenciales",
                     font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 24))

        # Usuario
        ctk.CTkLabel(frame, text="Usuario", anchor="w").pack(fill="x", padx=30)
        self.entry_user = ctk.CTkEntry(frame, placeholder_text="Escribe tu usuario",
                                       height=40, corner_radius=8)
        self.entry_user.pack(fill="x", padx=30, pady=(4, 12))

        # Contraseña
        ctk.CTkLabel(frame, text="Contraseña", anchor="w").pack(fill="x", padx=30)
        self.entry_pwd = ctk.CTkEntry(frame, placeholder_text="Escribe tu contraseña",
                                      show="*", height=40, corner_radius=8)
        self.entry_pwd.pack(fill="x", padx=30, pady=(4, 6))

        # Mostrar contraseña
        self.show_pwd = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(frame, text="Mostrar contraseña", variable=self.show_pwd,
                        command=self._toggle_pwd).pack(anchor="w", padx=30, pady=(0, 20))

        # Botón
        self.btn_login = ctk.CTkButton(frame, text="Entrar", height=42,
                                       corner_radius=8, command=self._validar)
        self.btn_login.pack(fill="x", padx=30)

        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="#FF4444",
                                      font=ctk.CTkFont(size=12))
        self.lbl_error.pack(pady=(10, 0))

        # Atajos de teclado
        self.entry_pwd.bind("<Return>", lambda e: self._validar())
        self.entry_user.bind("<Return>", lambda e: self.entry_pwd.focus())

    def _toggle_pwd(self):
        self.entry_pwd.configure(show="" if self.show_pwd.get() else "*")

    def _validar(self):
        usuario = self.entry_user.get().strip()
        pwd = self.entry_pwd.get().strip()

        if not usuario or not pwd:
            self.lbl_error.configure(text="⚠ Completa todos los campos.")
            return

        if usuario not in self.usuarios:
            self.lbl_error.configure(text="✗ Usuario no encontrado.")
            return

        if self.usuarios[usuario] != pwd:
            self.lbl_error.configure(text="✗ Contraseña incorrecta.")
            self.entry_pwd.delete(0, "end")
            return

        self.destroy()
        self.on_login_success(usuario)
