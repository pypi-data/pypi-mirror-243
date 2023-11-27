from tkadw.windows.canvas.widget import AdwWidget
from tkadw_material.element import MElement
from tkinter import Entry, StringVar


class MInput(AdwWidget, MElement):
    def __init__(self, *args, width=120, height=40, value: str = "", cursor: str = "xterm", **kwargs):
        super().__init__(*args, width=width, height=height, highlightthickness=False, cursor=cursor, **kwargs)

        self._args = {
            "value": value,
            "styles": {
                "rounded": False,
                "outline": False,
            },
            "colors": {
                "primary": "#5593cd",
                "second": "#a3a4a6",
                "third": "#ffffff",
                "text": "#ffffff"
            }
        }

        self.entry_value = StringVar(value=value)
        self.entry = Entry(self, highlightthickness=False, border=0, textvariable=self.entry_value)

        self.on_mouse = False
        self.on_enter = False
        self.on_focus = False

        self.bind("<Button>", self._on_mouse, add="+")
        self.bind("<ButtonRelease>", self._off_mouse, add="+")
        self.bind("<Enter>", self._enter, add="+")
        self.bind("<Leave>", self._leave, add="+")
        self.bind("<FocusIn>", self._focus_in, add="+")
        self.bind("<FocusOut>", self._focus_out, add="+")

    def text(self, value: str = None):
        if value is None:
            return self.entry_value.get()
        else:
            self.entry_value.set(value)

    def _on_mouse(self, event=None):
        self.on_mouse = True
        self.update()
        if self.on_enter:
            self.entry.focus_set()

    def _off_mouse(self, event=None):
        self.on_mouse = False
        self.update()

    def _enter(self, event=None):
        self.on_enter = True
        self.update()

    def _leave(self, event=None):
        self.on_enter = False
        self.update()

    def _focus_in(self, event=None):
        self.on_focus = True
        self.update()

    def _focus_out(self, event=None):
        self.on_focus = False
        self.update()

    def _draw(self, evt=None):
        self.delete("all")  # 初始清除

        if self.on_enter:
            if self.on_focus:
                _primary = self.color("primary")
            else:
                _primary = self.color("third")
        else:
            if self.on_focus:
                _primary = self.color("primary")
            else:
                _primary = self.color("second")

        if self.style("outline"):
            from tkadw_material.style import style
            fill = self.master.cget("background")
            fill_t = _primary
        else:
            from tkadw_material.style import style
            fill = self.master.cget("background")
            fill_t = self.color("text")

        if self.style("rounded"):
            self.create_round_rect4(
                1, 1,
                self.winfo_width() - 1,
                self.winfo_height() - 1,
                8,
                width=1,
                outline=_primary, fill=fill,
            )
        else:
            if self.style("outline"):
                self.create_rectangle(
                    1, 1,
                    self.winfo_width() - 1,
                    self.winfo_height() - 1,
                    width=1,
                    outline=_primary, fill=fill,
                )

        self.entry_text = self.create_window(
            self.winfo_width() / 2 + 1, self.winfo_height() / 2 + 1,
            width=self.winfo_width() - 6,
            height=self.winfo_height() - 6,
            window=self.entry
        )

        if not self.style("outline") and not self.style("rounded"):
            self.entry_bottom = self.create_rectangle(1 + 8 / 5,
                                                      self.winfo_height(),
                                                      self.winfo_width(),
                                                      self.winfo_height() - 1,
                                                      fill=_primary, outline=_primary,
                                                      width=0)

        self.entry.configure(background=self.master.cget("background"), foreground=self.color("text"),
                             insertbackground=self.color("text"))


if __name__ == '__main__':
    from tkadw_material.window import MWindow
    root = MWindow()

    input_tf = MInput(root, value="Rounded | No Outline").style("rounded", True)
    input_tf.pack(fill="x", padx=5, pady=5)

    input_tt = MInput(root, value="Rounded | Outline").style("rounded", True).style("rounded", True)
    input_tt.pack(fill="x", padx=5, pady=5)

    input_ff = MInput(root, value="No Rounded | No Outline")
    input_ff.pack(fill="x", padx=5, pady=5)

    input_ft = MInput(root, value="No Rounded | Outline").style("outline", True)
    input_ft.pack(fill="x", padx=5, pady=5)

    root.mainloop()
