from tkadw.windows.widgets.adw import Adw


class MWindow(Adw):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from tkadw_material.style import style

        self.configure(background=style()["background"])

    def material_dark(self, enable: bool = None):
        if enable is not None:
            if enable:
                from tkadw_material.style import style, dark_theme
                style(dark_theme)
            else:
                from tkadw_material.style import style, light_theme
                style(light_theme)
            self.configure(background=style()["background"])
            for child in self.winfo_children():
                child.update()
        else:
            from tkadw_material.style import style
            return style()["dark"]