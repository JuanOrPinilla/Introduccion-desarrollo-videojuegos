import pygame

#F5 para correr

class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        #Pantalla
        self.screen = pygame.display.set_mode((640,360), pygame.SCALED)
        #Reloj para el motor
        self.clock = pygame.time.Clock()
        self.is_running = False
        #FPS
        self.framerate = 60
        #Tiempo que ha pasado entre cuadro y cuadro (deltatime)
        self.delta_time = 0
        

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        pass

    def _calculate_time(self):
        pass
    
    
    def _process_events(self):
        for event in pygame.event.get(): #Da una lista de eventos
            if event.type == pygame.QUIT: #cuando se cierra con la X la ventana o uno presiona alt F4
                self.is_running = False #terminar el ciclo

    def _update(self):
        pass

    def _draw(self):
        #decirle al sistema que limpie la pantalla y dibuje lo que necesitamos
        self.screen.fill((0, 200, 128))
        pygame.display.flip() #voltear la imagen hacia la pantalla. coge el self screen y lo presenta
        

    def _clean(self):
        pygame.quit()
