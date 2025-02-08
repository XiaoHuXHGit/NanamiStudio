from templates.items.ArisStudio import ArisStudio


class Scene(ArisStudio):
    def __init__(self, screen, scene, position=(0, 0), scale=1.0, zoom_mode=ArisStudio.FILL):
        super().__init__(screen, scene, position, scale, zoom_mode)
