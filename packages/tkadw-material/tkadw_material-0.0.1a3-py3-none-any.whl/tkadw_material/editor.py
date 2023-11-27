from tkadw_material.input import MInput
from tkinter import Text


class MEditor(MInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.entry_value
        self.entry = Text(self, highlightthickness=False, border=0)

    def text(self, value: str = None):
        if value is None:
            return self.entry.get(1.0, "end")
        else:
            self.entry.delete(1.0, "end")
            self.entry.insert(1.0, value)


if __name__ == '__main__':
    from tkadw_material import *

    root = MWindow()

    editor = MEditor()
    editor.text("MEditor")
    print(editor.text())
    editor.row(padx=15, pady=15)

    root.mainloop()