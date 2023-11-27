from tkadw.windows.canvas.widget import AdwWidget
from tkadw_material.element import MElement


class MBtn(AdwWidget, MElement):
    def __init__(self, *args, width=120, height=40, text: str = "", command=None, cursor: str = "hand2", **kwargs):
        super().__init__(*args, width=width, height=height, highlightthickness=False, cursor=cursor, **kwargs)

        self._args = {
            "text": text,
            "styles": {
                "rounded": True,
                "outline": False,
            },
            "colors": {
                "primary": "#5898d4",
                "second": "#6fa5d8",
                "third": "#92b6d8",
                "text": "#ffffff"
            }
        }

        self.on_mouse = False
        self.on_enter = False

        self.bind("<Button>", self._on_mouse, add="+")
        self.bind("<ButtonRelease>", self._off_mouse, add="+")
        self.bind("<Enter>", self._enter, add="+")
        self.bind("<Leave>", self._leave, add="+")

        if command is not None:
            self.bind("<<Click>>", lambda event: command())

    def update(self) -> None:
        super().update_idletasks()
        self.configure(background=self.master.cget("background"))
        self._draw(None)

    def _on_mouse(self, event=None):
        self.on_mouse = True
        self.update()

    def _off_mouse(self, event=None):
        self.on_mouse = False
        self.update()
        if self.on_enter:
            self.event_generate("<<Click>>")
            self.focus_set()

    def _enter(self, event=None):
        self.on_enter = True
        self.update()

    def _leave(self, event=None):
        self.on_enter = False
        self.update()

    def text(self, value: str = None):
        if value:
            self._args["text"] = value
        else:
            return self._args["text"]

    def _draw(self, evt=None):
        self.delete("all")
        if self.on_enter:
            if self.on_mouse:
                _primary = self.color("third")
            else:
                _primary = self.color("second")
        else:
            _primary = self.color("primary")

        if self.style("outline"):
            from tkadw_material.style import style
            fill = style()["background"]
            fill_t = _primary
        else:
            from tkadw_material.style import style
            fill = _primary
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
            self.create_rectangle(
                1, 1,
                self.winfo_width() - 1,
                self.winfo_height() - 1,
                width=1,
                outline=_primary, fill=fill,
            )

        from tkinter.font import nametofont
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text(), fill=fill_t,
            font=nametofont("TkDefaultFont").config(weight="bold", size=10)
        )


if __name__ == '__main__':
    from tkadw_material.window import MWindow
    root = MWindow()

    btn_tf = MBtn(root, text="Rounded | No Outline")
    btn_tf.pack(fill="x", padx=5, pady=5)

    btn_tt = MBtn(root, text="Rounded | Outline").style("outline", True)
    btn_tt.pack(fill="x", padx=5, pady=5)

    btn_ff = MBtn(root, text="No Rounded | No Outline").style("rounded", False)
    btn_ff.pack(fill="x", padx=5, pady=5)

    btn_ft = MBtn(root, text="No Rounded | Outline").style("outline", True).style("rounded", False)
    btn_ft.pack(fill="x", padx=5, pady=5)

    root.mainloop()
