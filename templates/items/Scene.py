from templates.items.NanamiStudio import NanamiStudio


class Scene(NanamiStudio):
    def __init__(self, screen, scene, position=(0, 0), scale=1.0, zoom_mode=NanamiStudio.FILL):
        super().__init__(screen, scene, position, scale, zoom_mode)
