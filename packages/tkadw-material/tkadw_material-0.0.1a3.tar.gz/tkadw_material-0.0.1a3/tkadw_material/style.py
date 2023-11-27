from os import environ

light_theme = {
    "name": "light",
    "dark": False,
    "background": "#ffffff"
}

dark_theme = {
    "name": "dark",
    "dark": True,
    "background": "#181c21"
}

if "ADW_MATERIAL_STYLE" not in environ:
    from json import dumps
    from darkdetect import isDark
    if isDark():
        environ["ADW_MATERIAL_STYLE"] = dumps(dark_theme)
    else:
        environ["ADW_MATERIAL_STYLE"] = dumps(light_theme)


def style(value: dict = None) -> dict:
    from json import loads
    if value:
        environ["ADW_MATERIAL_STYLE"] = dumps(value)
    else:
        return loads(environ["ADW_MATERIAL_STYLE"])
