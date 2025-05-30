import esper

from src.create.prefab_creator import create_explosion_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_dash import CTagDash
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World, explosion_cfg:dict):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)
    for bullet_entity, (bu_s, bu_t, _) in bullet_components:
        bu_rect = CSurface.get_area_relative(bu_s.area, bu_t.pos)
        bu_rect.topleft = bu_t.pos

        for enemy_entity, (c_s, c_t, _) in enemy_components:
            ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            ene_rect.topleft = c_t.pos

            if ene_rect.colliderect(bu_rect): 
                world.delete_entity(enemy_entity) 
                world.delete_entity(bullet_entity) 
                explosion_entity = create_explosion_square(world, explosion_cfg,c_t.pos)
                break 
    dash_components = world.get_components(CSurface, CTransform, CTagDash)
    for dash_entity, (bu_s, bu_t, _) in dash_components:
        bu_rect = CSurface.get_area_relative(bu_s.area, bu_t.pos)
        bu_rect.topleft = bu_t.pos

        for enemy_entity, (c_s, c_t, _) in enemy_components:
            ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            ene_rect.topleft = c_t.pos

            if ene_rect.colliderect(bu_rect): 
                world.delete_entity(enemy_entity) 
                world.delete_entity(dash_entity) 
                explosion_entity = create_explosion_square(world, explosion_cfg,c_t.pos)
                break 
    
    