import os


def get_base_path():
    """Get the base path for assets, works both in development and when packaged"""
    try:
        # Quando executado como script normal
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except NameError:
        # Quando executado como executável PyInstaller
        import sys
        base_path = sys._MEIPASS
    
    return base_path


assets_path = os.path.join(get_base_path(), 'assets')
fonts_path = os.path.join(assets_path, 'fonts')
hud_path = os.path.join(assets_path, 'hud')
icons_path = os.path.join(assets_path, 'icons')


def path(file):
    return os.path.join(assets_path, file).replace('\\', '/')


def font(file):
    return os.path.join(fonts_path, file).replace('\\', '/')


def hud(file):
    return os.path.join(hud_path, file).replace('\\', '/')


def icon(file):
    icon_full_path = os.path.join(icons_path, file).replace('\\', '/')
    # Verificar se o arquivo existe
    if not os.path.exists(icon_full_path):
        # Tentar caminho alternativo
        alt_path = os.path.join(assets_path, 'icons', file).replace('\\', '/')
        if os.path.exists(alt_path):
            return alt_path
        print(f"Warning: Icon not found: {icon_full_path}")
    return icon_full_path


def get_icon_path(icon_name):
    """Helper function to get icon path with error checking"""
    return icon(icon_name)