import pygame
import esper

from src.create.prefab_creator import crear_spawner, create_bullet_square, create_input_player, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_border import system_collision_bullet_screen
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_hunter_persecution import system_persecution_player_hunter
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

import json

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_screen_limit import system_screen_limit
#F5 para correr
        
class GameEngine:
    
    def __init__(self) -> None:
        self._load_config_files()
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 0)
        #Reloj para el motor
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.title = pygame.display.set_caption(self.window_cfg["title"])
        #Tiempo que ha pasado entre cuadro y cuadro (deltatime)
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.current_bullet = 0
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
        
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        
        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_limit(self.ecs_world,self.screen)
        system_collision_player_enemy(self.ecs_world,self._player_entity, self.level_01_cfg)
        system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg)
        
        system_persecution_player_hunter(self.ecs_world,self._player_entity, self.level_01_cfg, self.enemies_cfg["Hunter"])
         
        system_collision_bullet_screen(self.ecs_world,self.screen)
        system_animation(self.ecs_world, self.delta_time)
        system_explosion_state(self.ecs_world, self.delta_time)
        self.ecs_world._clear_dead_entities()
            

    def _draw(self):
        #decirle al sistema que limpie la pantalla y dibuje lo que necesitamos
        self.screen.fill(self.bg_color)
        
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip() #voltear la imagen hacia la pantalla. coge el self screen y lo presenta
        

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input:CInputCommand):
        
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x = -self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                if self._player_c_vel.vel.x < 0:
                    self._player_c_vel.vel.x = 0

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x = self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                if self._player_c_vel.vel.x > 0:
                    self._player_c_vel.vel.x = 0

                
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.y = -self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                if self._player_c_vel.vel.y < 0:
                    self._player_c_vel.vel.y = 0

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.y = self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                if self._player_c_vel.vel.y > 0:
                    self._player_c_vel.vel.y = 0
        
        if c_input.name == "PLAYER_FIRE":
            active_bullets = len(self.ecs_world.get_components(CTagBullet))

            if active_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]:
                if c_input.phase == CommandPhase.START:
                    mouse_pos = pygame.mouse.get_pos()
                    create_bullet_square(self.ecs_world, self._player_entity, self.bullet_cfg, mouse_pos)


    def _load_config_files(self):
        with open('assets/cfg/window.json','r') as window_file:
                self.window_cfg = json.load(window_file)       
        with open('assets/cfg/level_01.json','r') as level_file:
            self.level_01_cfg = json.load(level_file)
        with open('assets/cfg/enemies.json','r') as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open('assets/cfg/player.json','r') as player_file:
            self.player_cfg = json.load(player_file)
        with open('assets/cfg/bullet.json','r') as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open('assets/cfg/explosion.json','r') as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
    
        

        