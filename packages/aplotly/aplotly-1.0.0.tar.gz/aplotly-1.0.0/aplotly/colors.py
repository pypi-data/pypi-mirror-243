
def rgba_to_hex(rgba):
    rgba = rgba.replace("rgba(", "").replace(")", "").split(",")
    r = int(rgba[0])
    g = int(rgba[1])
    b = int(rgba[2])
    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()


def hex_to_rgba(hex):
    hex = hex.replace("#", "")
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return f"rgba({r}, {g}, {b}, 1)"


def convert_palette_to_rgba(palette):
    return {key: hex_to_rgba(value) for key, value in palette.items()}


def default():
    line_colors = {
        "blue": "#022E9F",
        "dark_blue": "#041E42",
        "light_green": "#15CAD6",
        "dim_green": "#008080",
        "dark_green": "#006400",
        "light_orange": "#FFA500",
        "dim_orange": "#FF4500",
        "burgundy": "#800020",
    }

    chart_colors = {
        "background": "#FFFFFF",
        "grid": "#D3D3D3",
        "text": "#041E42",
        "axes": "#041E42",
    }

    return line_colors, chart_colors


def greys():
    line_colors = {
        "black": "#000000",
        "dark_grey": "#A9A9A9",
        "dim_grey": "#D3D3D3",
        "light_grey": "#DCDCDC",
    }

    chart_colors = {
        "background": "#FFFFFF",
        "grid": "#D3D3D3",
        "text": "#000000",
        "axes": "#000000",
    }

    return line_colors, chart_colors

def night():
    line_colors = {
        "green": "#00FF41",
        "grey": "#6E6E73",
        "white": "#F5F5F7",
    }

    chart_colors = {
        "background": "#000000",
        "grid": "#6E6E73",
        "text": "#F5F5F7",
        "axes": "#F5F5F7",
    }

    return line_colors, chart_colors


def dark_mode():
    line_colors = {
        "green": "#11A13C",
        "grey": "#6E6E73",
        "white": "#F5F5F7",
    }

    chart_colors = {
        "background": "#212121",
        "grid": "#3D3D3D",
        "text": "#F5F5F7",
        "axes": "#F5F5F7",
    }

    return line_colors, chart_colors


def available_palettes():
    return ["default", "greys", "night", "dark_mode"]


def select_palette(name, color_type="hex"):
    if color_type not in ["hex", "rgba"]:
        raise ValueError("color_type must be either 'hex' or 'rgba'")

    if name == "default" or name == "":
        if color_type == "rgba":
            return convert_palette_to_rgba(default()[0]), convert_palette_to_rgba(default()[1])
        else:
            return default()
    elif name == "greys":
        if color_type == "rgba":
            return convert_palette_to_rgba(greys()[0]), convert_palette_to_rgba(greys()[1])
        else:
            return greys()
    elif name == "night":
        if color_type == "rgba":
            return convert_palette_to_rgba(night()[0]), convert_palette_to_rgba(night()[1])
        else:
            return night()
    elif name == "dark_mode":
        if color_type == "rgba":
            return convert_palette_to_rgba(dark_mode()[0]), convert_palette_to_rgba(dark_mode()[1])
        else:
            return dark_mode()
    else:
        raise ValueError("palette name not found")
