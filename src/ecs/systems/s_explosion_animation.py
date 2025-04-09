from esper import Processor
import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_explosion import CTagExplosion  # Si tienes el renderizado aparte

def system_explosion_animation(world:esper.World, delta_time: float):
    components = world.get_components(CSurface, CAnimation,CTagExplosion)
    
    for entity, (c_s, c_a, _) in components:
        print(c_a.curr_frame)
        if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
            world.delete_entity(entity)
            continue

        c_a.curr_anim_time -= delta_time

        if c_a.curr_anim_time <= 0:
            c_a.curr_frame += 1
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate

            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.finished = True
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].end
                continue  # esperar al siguiente frame para eliminar

            # Actualizar área del sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame