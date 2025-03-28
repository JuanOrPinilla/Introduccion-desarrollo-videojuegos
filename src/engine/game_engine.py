import pygame
import esper

from src.create.prefab_creator import crear_cuadrado
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

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
        
        self.ecs_world = esper.World()
        
        

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
        crear_cuadrado(self.ecs_world, 
                       pygame.Vector2(50,50), pygame.Vector2(150,300),pygame.Vector2(500,500), pygame.Color(100,100,255))
        crear_cuadrado(self.ecs_world, 
                       pygame.Vector2(50,50), pygame.Vector2(0,0),pygame.Vector2(1000,100), pygame.Color(255,100,255))
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0 #para segundos
    
    
    def _process_events(self):
        for event in pygame.event.get(): #Da una lista de eventos
            if event.type == pygame.QUIT: #cuando se cierra con la X la ventana o uno presiona alt F4
                self.is_running = False #terminar el ciclo

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
            

    def _draw(self):
        #decirle al sistema que limpie la pantalla y dibuje lo que necesitamos
        self.screen.fill((0, 200, 128))
        
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip() #voltear la imagen hacia la pantalla. coge el self screen y lo presenta
        
        #pintar el cuadrado antes de que se presente la pantalla pero despues de haber limpiado
        

    def _clean(self):
        pygame.quit()
