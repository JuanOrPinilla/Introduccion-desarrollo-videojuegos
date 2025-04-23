import os
import pygame
import esper

from src.create.prefab_creator import crear_spawner, create_bullet_square, create_dash_effect, create_input_player, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_border import system_collision_bullet_screen
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_dash import system_dash
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
from src.engine.service_locator import ServiceLocator
#F5 para correr
        
class GameEngine:
    
    def __init__(self) -> None:
        self._load_config_files()
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 0)
        
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.title = pygame.display.set_caption(self.window_cfg["title"])
        
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.current_bullet = 0
        self.ecs_world = esper.World()
        
        self.font_title = ServiceLocator.fonts_service.get(self.interface_cfg["font"],self.interface_cfg["title_size"] )
        
        self.text_title = self.font_title.render(self.interface_cfg["title"], True, (self.interface_cfg["title_color"]["r"],
                                                                                self.interface_cfg["title_color"]["g"],
                                                                                self.interface_cfg["title_color"]["b"])) 
        
        self.font_instr = ServiceLocator.fonts_service.get(self.interface_cfg["font"],self.interface_cfg["instr_size"] )
        
        self.text_instr = self.font_instr.render(self.interface_cfg["instr"], True, (self.interface_cfg["instr_color"]["r"],
                                                                                self.interface_cfg["instr_color"]["g"],
                                                                                self.interface_cfg["instr_color"]["b"])) 
        self._is_dashing = False
        self._dash_duration = 0.2
        self._dash_timer = 0
        self._dash_counter =3
        self._dash_max = 3
        
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
            if event.type == pygame.QUIT: 
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world,self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        
        if self._is_dashing:
            self._dash_timer += self.delta_time
            if self._dash_timer >= self._dash_duration:
                self._player_c_vel.vel.x = 0
                self._player_c_vel.vel.y = 0
                self._is_dashing = False
        
        self._dash_counter += self.delta_time
        if self._dash_counter >= self._dash_max:
            self._dash_counter = self._dash_max


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
        self.screen.fill(self.bg_color)
        self.screen.blit(self.text_title, (20, 20))
        self.screen.blit(self.text_instr, (20, 50))
        self.draw_dash_timer(self.screen)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()
        

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
        
        if c_input.name == "DASH":
            if self._dash_counter == self._dash_max:
                if c_input.phase == CommandPhase.START:
                    mouse_pos = pygame.mouse.get_pos()
                    create_dash_effect(self.ecs_world, self._player_entity, -60, mouse_pos)
                    create_dash_effect(self.ecs_world, self._player_entity, -30, mouse_pos)
                    create_dash_effect(self.ecs_world, self._player_entity, 0, mouse_pos)
                    create_dash_effect(self.ecs_world, self._player_entity, 30, mouse_pos)
                    create_dash_effect(self.ecs_world, self._player_entity, 60, mouse_pos)
                    ServiceLocator.sounds_service.play("assets/snd/dash.ogg")

                    system_dash(self.ecs_world, self._player_entity, mouse_pos, self.delta_time)
                    self._dash_counter = 0  
                    self._is_dashing = True
                    self._dash_timer = 0  # reiniciar el contador
                elif c_input.phase == CommandPhase.END:
                    self._player_c_vel.vel.x = 0
                    self._player_c_vel.vel.y = 0


    def draw_dash_timer(self, surface):
        if self._dash_counter < self._dash_max:
            porcentaje = int((self._dash_counter / self._dash_max) * 100)
            text = self.font_instr.render(f"Dash: {porcentaje}%", True, (self.interface_cfg["prct_color_1"]["r"],
                                                                                self.interface_cfg["prct_color_1"]["g"],
                                                                                self.interface_cfg["prct_color_1"]["b"]))
        else:
            text = self.font_instr.render("Dash protector Listo!", True, (self.interface_cfg["prct_color_2"]["r"],
                                                                                self.interface_cfg["prct_color_2"]["g"],
                                                                                self.interface_cfg["prct_color_2"]["b"]))
        surface.blit(text, (20, 340))

        
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
        with open('assets/cfg/interface.json','r') as interface_file:
            self.interface_cfg = json.load(interface_file)
    
        

        