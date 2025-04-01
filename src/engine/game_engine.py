import pygame
import esper

from src.create.prefab_creator import crear_cuadrado
from src.create.prefab_creator import crear_enemigos
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

import json

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
#F5 para correr
        
class GameEngine:
    
    def __init__(self) -> None:
        pygame.init()
        #lectura de los datos de la ventana
        lectura_json_window(self)
        
        self.screen = pygame.display.set_mode(self.size, pygame.SCALED)
        #Reloj para el motor
        self.clock = pygame.time.Clock()
        self.is_running = False
        
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
        crear_enemigos(self.ecs_world)


    def _calculate_time(self):
        self.delta_time = self.clock.tick(self.framerate) / 1000.0  # Delta en segundos
    
    
    def _process_events(self):
        for event in pygame.event.get(): #Da una lista de eventos
            if event.type == pygame.QUIT: #cuando se cierra con la X la ventana o uno presiona alt F4
                self.is_running = False #terminar el ciclo

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
            

    def _draw(self):
        #decirle al sistema que limpie la pantalla y dibuje lo que necesitamos
        self.screen.fill(self.bg_color)
        
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip() #voltear la imagen hacia la pantalla. coge el self screen y lo presenta
        
        #pintar el cuadrado antes de que se presente la pantalla pero despues de haber limpiado
        

    def _clean(self):
        pygame.quit()

def lectura_json_window(self):
        
        with open('assets/cfg/window.json','r') as file:
            data = json.load(file)

        self.title = data["title"]
        self.size = (data["size"]["w"], data["size"]["h"])  # Tupla (ancho, alto)
        self.bg_color = (data["bg_color"]["r"], data["bg_color"]["g"], data["bg_color"]["b"])  # Tupla (R, G, B)
        
        #FPS
        self.framerate = data["framerate"]