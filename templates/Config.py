import ctypes


class SystemConfig(object):
    __user32 = ctypes.windll.user32
    __screen_width = __user32.GetSystemMetrics(0)
    __screen_height = __user32.GetSystemMetrics(1)
    DEBUG = True
    window_width = __screen_width * 2 // 3
    window_height = __screen_height * 2 // 3
    title = 'Airs Studio'
    assets_folder = 'assets'
    icon = 'assets/images/icon.png'
    window_aspect_ratio_lock = True
