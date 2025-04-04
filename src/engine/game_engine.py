import pygame
import esper

from src.create.prefab_creator import crear_spawner, create_input_player, create_player_square
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

import json

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
#F5 para correr
        
class GameEngine:
    
    def __init__(self) -> None:
        self._load_config_files()
        pygame.init()

        self.screen = pygame.display.set_mode((self.window_cfg["size"]["w"],self.window_cfg["size"]["h"]), pygame.SCALED)
        #Reloj para el motor
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        #Tiempo que ha pasado entre cuadro y cuadro (deltatime)
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
    
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
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg,self.level_01_cfg["player_spawn"])
        self._player_c_vel = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        crear_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)


    def _calculate_time(self):
        self.delta_time = self.clock.tick(self.framerate) / 1000.0  # Delta en segundos
    
    
    def _process_events(self):
        for event in pygame.event.get(): #Da una lista de eventos
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT: #cuando se cierra con la X la ventana o uno presiona alt F4
                self.is_running = False #terminar el ciclo

    def _update(self):
        system_enemy_spawner(self.ecs_world,self.enemies_cfg, self.delta_time)
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

    def _do_action(self, c_input:CInputCommand):
        print(c_input.name + " " + str(c_input.phase))

    def _load_config_files(self):
        with open('assets/cfg/window.json','r') as window_file:
                self.window_cfg = json.load(window_file)       
        with open('assets/cfg/level_01.json','r') as level_file:
            self.level_01_cfg = json.load(level_file)
        with open('assets/cfg/enemies.json','r') as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open('assets/cfg/player.json','r') as player_file:
            self.player_cfg = json.load(player_file)
    
        

        