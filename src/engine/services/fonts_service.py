import pygame


class FontsService:
    def __init__(self) -> None:
        self._fonts = {}
    
    def get(self, path: str, size: int):
        key = (path, size)
        # Si la fuente no ha sido cargada, cargarla y almacenarla
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path, size)
        
        return self._fonts[key]