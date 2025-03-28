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
        #velocidad del rectangulo
        self.vel_cuad = pygame.Vector2(1000,3000)
        
        #Crear posición rectangulo
        self.pos_cuad = pygame.Vector2(50,50)
        size_cuad = pygame.Vector2(50,50)
        col_cuad = pygame.Color(255,255,50)
        
        #superficie rectangulo
        self.surf_cuad = pygame.Surface(size_cuad)
        self.surf_cuad.fill(col_cuad)
    

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0 #para segundos
    
    
    def _process_events(self):
        for event in pygame.event.get(): #Da una lista de eventos
            if event.type == pygame.QUIT: #cuando se cierra con la X la ventana o uno presiona alt F4
                self.is_running = False #terminar el ciclo

    def _update(self):
        # avanzamos en X       100 px         POR SEGUNDO 
        self.pos_cuad.x += self.vel_cuad.x * self.delta_time 
        # avanzamos en Y       100 px         POR SEGUNDO 
        self.pos_cuad.y += self.vel_cuad.y * self.delta_time
        
        screen_rect = self.screen.get_rect()
        cuad_rect = self.surf_cuad.get_rect(topleft=self.pos_cuad)
        
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            self.vel_cuad.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            self.pos_cuad.x = cuad_rect.x
        
        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            self.vel_cuad.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            self.pos_cuad.y = cuad_rect.y
            

    def _draw(self):
        #decirle al sistema que limpie la pantalla y dibuje lo que necesitamos
        self.screen.fill((0, 200, 128))
        
        #### DESPUES DE ####
        self.screen.blit(self.surf_cuad,self.pos_cuad) #pintar el cuadrado antes de que se presente la pantalla pero despues de haber limpiado
        #### ANTES DE #####
        
        pygame.display.flip() #voltear la imagen hacia la pantalla. coge el self screen y lo presenta
        
        #pintar el cuadrado antes de que se presente la pantalla pero despues de haber limpiado
        

    def _clean(self):
        pygame.quit()
