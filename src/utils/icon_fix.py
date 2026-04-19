import ctypes


def icon_fix():
    myappid = 'Bigelli.HeroSiegeStats.2026.04.19'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
