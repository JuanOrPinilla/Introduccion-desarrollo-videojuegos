import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_velocity import CVelocity

def system_hunter_state(world:esper.World):
    components = world.get_components(CVelocity, CAnimation, CHunterState)
    for _, (c_v,c_a, c_pst) in components:
        if c_pst.state == HunterState.IDLE:
            _do_idle_state(c_v,c_a, c_pst)
        elif c_pst.state == HunterState.MOVE:
            _do_move_state(c_v, c_a, c_pst)
            
def _do_idle_state(c_v:CVelocity, c_a:CAnimation, c_pst: CHunterState):
    _set_animation(c_a, 1)
    if c_v.vel.magnitude_squared() > 0:
        c_pst.state = HunterState.MOVE
    
    
def _do_move_state(c_v:CVelocity, c_a:CAnimation, c_pst: CHunterState):
    _set_animation(c_a, 0)
    if c_v.vel.magnitude_squared() <= 0:
        c_pst.state = HunterState.IDLE
    
def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.curr_anim == num_anim:
        return 
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start