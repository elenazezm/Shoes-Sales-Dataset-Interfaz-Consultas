import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from queries import CONSULTAS


class AppWindow(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"Shoes Sales Analytics — {usuario}")
        self.geometry("1200x700")
        self.minsize(900, 550)

        self._build_ui()

    # ── Construcción de UI ─────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Panel izquierdo (menú) ─────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(20, weight=1)

        ctk.CTkLabel(sidebar, text="Shoes Sales",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(
                         row=0, column=0, pady=(24, 4), padx=16)
        ctk.CTkLabel(sidebar, text=f"Hola, {self.usuario}",
                     font=ctk.CTkFont(size=12), text_color="gray").grid(
                         row=1, column=0, pady=(0, 20), padx=16)

        ctk.CTkLabel(sidebar, text="CONSULTAS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="gray").grid(row=2, column=0, sticky="w",
                                             padx=20, pady=(0, 6))

        for i, nombre in enumerate(CONSULTAS.keys(), start=3):
            btn = ctk.CTkButton(
                sidebar, text=nombre, anchor="w",
                fg_color="transparent", hover_color=("gray75", "gray25"),
                text_color=("gray10", "gray90"), corner_radius=6,
                height=36, command=lambda n=nombre: self._ejecutar_consulta(n)
            )
            btn.grid(row=i, column=0, padx=12, pady=2, sticky="ew")

        # Cerrar sesión
        ctk.CTkButton(sidebar, text="Cerrar sesión", fg_color="transparent",
                      text_color="gray", hover_color=("gray75", "gray25"),
                      command=self._cerrar_sesion).grid(
                          row=21, column=0, padx=12, pady=(0, 16), sticky="ew")

        # ── Panel derecho ──────────────────────────────────────────────────
        right = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # Título de consulta activa
        self.lbl_titulo = ctk.CTkLabel(right, text="Selecciona una consulta del menú",
                                       font=ctk.CTkFont(size=17, weight="bold"),
                                       anchor="w")
        self.lbl_titulo.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Frame de tabla
        table_frame = ctk.CTkFrame(right, corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Treeview con scrollbars
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background="#2b2b2b", fieldbackground="#2b2b2b",
                        foreground="white", rowheight=28,
                        font=("Arial", 11))
        style.configure("Dark.Treeview.Heading",
                        background="#1f6aa5", foreground="white",
                        font=("Arial", 11, "bold"))
        style.map("Dark.Treeview", background=[("selected", "#1f6aa5")])

        self.tree = ttk.Treeview(table_frame, style="Dark.Treeview",
                                 show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # ── Panel de justificación ─────────────────────────────────────────
        self.lbl_just = ctk.CTkTextbox(right, height=70, corner_radius=8,
                                       font=ctk.CTkFont(size=12))
        self.lbl_just.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.lbl_just.insert("0.0", "La justificación de cada consulta aparecerá aquí.")
        self.lbl_just.configure(state="disabled")

    # ── Lógica de consultas ────────────────────────────────────────────────
    def _ejecutar_consulta(self, nombre):
        try:
            func = CONSULTAS[nombre]
            df, justificacion = func()
            self.lbl_titulo.configure(text=nombre)
            self._poblar_tabla(df)
            self.lbl_just.configure(state="normal")
            self.lbl_just.delete("0.0", "end")
            self.lbl_just.insert("0.0", f{justificacion}")
            self.lbl_just.configure(state="disabled")
        except Exception as e:
            self.lbl_titulo.configure(text=f"Error: {e}")

    def _poblar_tabla(self, df):
        self.tree.delete(*self.tree.get_children())
        cols = list(df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            max_w = max(len(str(col)), df[col].astype(str).str.len().max())
            self.tree.column(col, width=min(max(max_w * 9, 80), 220),
                             anchor="center")
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Alternar colores de filas
        self.tree.tag_configure("odd",  background="#333333")
        self.tree.tag_configure("even", background="#2b2b2b")
        for i, iid in enumerate(self.tree.get_children()):
            tag = "odd" if i % 2 else "even"
            self.tree.item(iid, tags=(tag,))

    def _cerrar_sesion(self):
        self.destroy()
        import main
        main.iniciar()
