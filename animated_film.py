import pygame
import sys
import math
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 120
        self.speed = 2
        self.arm_angle = 0
        self.leg_angle = 0
        self.eye_glow = 0
        self.direction = 1
        self.state = "wandering"
        self.target_x = x
        self.target_y = y
        self.moving_to_target = False
        
    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.moving_to_target = True
        
    def update(self):
        # Move towards target if set
        if self.moving_to_target:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 5:
                self.x += dx * 0.05
                self.y += dy * 0.05
            else:
                self.moving_to_target = False
        
        # Update animations based on state
        if self.state == "wandering":
            self.arm_angle = math.sin(pygame.time.get_ticks() * 0.01) * 30
            self.leg_angle = math.sin(pygame.time.get_ticks() * 0.02) * 20
            self.eye_glow = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 100 + 155
            
        elif self.state == "discovering":
            self.arm_angle = math.sin(pygame.time.get_ticks() * 0.02) * 45
            self.eye_glow = 255
            
        elif self.state == "repairing":
            self.arm_angle = math.sin(pygame.time.get_ticks() * 0.05) * 60
            self.leg_angle = math.sin(pygame.time.get_ticks() * 0.1) * 10
            
        elif self.state == "celebrating":
            self.arm_angle = math.sin(pygame.time.get_ticks() * 0.1) * 90
            self.leg_angle = math.sin(pygame.time.get_ticks() * 0.15) * 30
            self.eye_glow = 255
            
        elif self.state == "sleeping":
            self.arm_angle = 0
            self.leg_angle = 0
            self.eye_glow = abs(math.sin(pygame.time.get_ticks() * 0.002)) * 50
            
    def draw(self, screen):
        # Body
        body_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, GRAY, body_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, body_rect, 3, border_radius=10)
        
        # Head
        head_radius = 30
        pygame.draw.circle(screen, GRAY, (self.x, self.y - self.height//2 - head_radius//2), head_radius)
        pygame.draw.circle(screen, DARK_GRAY, (self.x, self.y - self.height//2 - head_radius//2), head_radius, 3)
        
        # Eyes with glow effect
        eye_glow_color = (0, min(255, self.eye_glow), min(255, self.eye_glow))
        pygame.draw.circle(screen, eye_glow_color, (self.x - 10, self.y - self.height//2 - head_radius//2 - 5), 8)
        pygame.draw.circle(screen, eye_glow_color, (self.x + 10, self.y - self.height//2 - head_radius//2 - 5), 8)
        
        # Arms
        arm_length = 40
        left_arm_x = self.x - self.width//2
        left_arm_y = self.y - self.height//4
        right_arm_x = self.x + self.width//2
        right_arm_y = self.y - self.height//4
        
        left_arm_end_x = left_arm_x - arm_length * math.cos(math.radians(self.arm_angle))
        left_arm_end_y = left_arm_y + arm_length * math.sin(math.radians(self.arm_angle))
        right_arm_end_x = right_arm_x + arm_length * math.cos(math.radians(self.arm_angle))
        right_arm_end_y = right_arm_y + arm_length * math.sin(math.radians(self.arm_angle))
        
        pygame.draw.line(screen, DARK_GRAY, (left_arm_x, left_arm_y), (left_arm_end_x, left_arm_end_y), 8)
        pygame.draw.line(screen, DARK_GRAY, (right_arm_x, right_arm_y), (right_arm_end_x, right_arm_end_y), 8)
        
        # Legs
        leg_length = 35
        left_leg_x = self.x - 15
        left_leg_y = self.y + self.height//2
        right_leg_x = self.x + 15
        right_leg_y = self.y + self.height//2
        
        left_leg_end_x = left_leg_x - leg_length * math.sin(math.radians(self.leg_angle))
        left_leg_end_y = left_leg_y + leg_length * math.cos(math.radians(self.leg_angle))
        right_leg_end_x = right_leg_x + leg_length * math.sin(math.radians(self.leg_angle))
        right_leg_end_y = right_leg_y + leg_length * math.cos(math.radians(self.leg_angle))
        
        pygame.draw.line(screen, DARK_GRAY, (left_leg_x, left_leg_y), (left_leg_end_x, left_leg_end_y), 10)
        pygame.draw.line(screen, DARK_GRAY, (right_leg_x, right_leg_y), (right_leg_end_x, right_leg_end_y), 10)

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.arm_angle = 0
        self.eye_glow = 0
        self.color = (0, 255, 0)  # Green alien
        
    def update(self):
        self.arm_angle = math.sin(pygame.time.get_ticks() * 0.03) * 25
        self.eye_glow = abs(math.sin(pygame.time.get_ticks() * 0.008)) * 155 + 100
        
    def draw(self, screen):
        # Body
        body_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, self.color, body_rect, border_radius=15)
        
        # Head
        head_radius = 25
        pygame.draw.circle(screen, self.color, (self.x, self.y - self.height//2 - head_radius//2), head_radius)
        
        # Big black eyes
        pygame.draw.circle(screen, (0, 0, 0), (self.x - 8, self.y - self.height//2 - head_radius//2), 10)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 8, self.y - self.height//2 - head_radius//2), 10)
        
        # Glowing pupils
        eye_glow_color = (255, 255, min(255, self.eye_glow))
        pygame.draw.circle(screen, eye_glow_color, (self.x - 8, self.y - self.height//2 - head_radius//2), 4)
        pygame.draw.circle(screen, eye_glow_color, (self.x + 8, self.y - self.height//2 - head_radius//2), 4)
        
        # Arms
        arm_length = 35
        left_arm_x = self.x - self.width//2
        left_arm_y = self.y - 10
        right_arm_x = self.x + self.width//2
        right_arm_y = self.y - 10
        
        left_arm_end_x = left_arm_x - arm_length * math.cos(math.radians(self.arm_angle))
        left_arm_end_y = left_arm_y + arm_length * math.sin(math.radians(self.arm_angle))
        right_arm_end_x = right_arm_x + arm_length * math.cos(math.radians(self.arm_angle))
        right_arm_end_y = right_arm_y + arm_length * math.sin(math.radians(self.arm_angle))
        
        pygame.draw.line(screen, self.color, (left_arm_x, left_arm_y), (left_arm_end_x, left_arm_end_y), 6)
        pygame.draw.line(screen, self.color, (right_arm_x, right_arm_y), (right_arm_end_x, right_arm_end_y), 6)

class SpaceStation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 150
        self.window_lights = []
        self.generate_windows()
        
    def generate_windows(self):
        for i in range(8):
            for j in range(4):
                self.window_lights.append({
                    'x': self.x - self.width//2 + 30 + i * 25,
                    'y': self.y - self.height//2 + 20 + j * 30,
                    'on': random.random() > 0.3
                })
                
    def update(self):
        # Randomly toggle some windows
        for window in self.window_lights:
            if random.random() < 0.02:  # 2% chance to toggle each frame
                window['on'] = not window['on']
                
    def draw(self, screen):
        # Main structure
        main_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, LIGHT_BLUE, main_rect, border_radius=10)
        pygame.draw.rect(screen, BLUE, main_rect, 3, border_radius=10)
        
        # Solar panels
        panel_rect1 = pygame.Rect(self.x - self.width//2 - 40, self.y - 30, 30, 100)
        panel_rect2 = pygame.Rect(self.x + self.width//2 + 10, self.y - 30, 30, 100)
        pygame.draw.rect(screen, DARK_GRAY, panel_rect1)
        pygame.draw.rect(screen, DARK_GRAY, panel_rect2)
        
        # Windows
        for window in self.window_lights:
            color = YELLOW if window['on'] else DARK_GRAY
            pygame.draw.circle(screen, color, (window['x'], window['y']), 5)

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 200
        self.smoke_particles = []
        self.launched = False
        self.launch_power = 0
        self.in_space = False
        
    def launch(self):
        self.launched = True
        self.launch_power = 10
        
    def update(self):
        if self.launched:
            if not self.in_space:
                self.y -= self.launch_power
                self.launch_power *= 0.98
                
                # Add smoke particles
                if random.random() < 0.3:
                    self.smoke_particles.append({
                        'x': self.x + random.randint(-20, 20),
                        'y': self.y + self.height//2,
                        'size': random.randint(10, 30),
                        'life': 100
                    })
            
        # Update smoke particles
        for particle in self.smoke_particles[:]:
            particle['y'] += 2
            particle['life'] -= 2
            particle['size'] *= 0.95
            if particle['life'] <= 0:
                self.smoke_particles.remove(particle)
                
    def draw(self, screen):
        # Rocket body
        rocket_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, RED, rocket_rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, rocket_rect, 3, border_radius=5)
        
        # Rocket nose
        nose_points = [
            (self.x, self.y - self.height//2 - 40),
            (self.x - self.width//2, self.y - self.height//2),
            (self.x + self.width//2, self.y - self.height//2)
        ]
        pygame.draw.polygon(screen, ORANGE, nose_points)
        pygame.draw.polygon(screen, DARK_GRAY, nose_points, 2)
        
        # Fins
        fin_points_left = [
            (self.x - self.width//2, self.y + self.height//2),
            (self.x - self.width//2 - 30, self.y + self.height//2 + 50),
            (self.x - self.width//2, self.y + self.height//2 + 30)
        ]
        fin_points_right = [
            (self.x + self.width//2, self.y + self.height//2),
            (self.x + self.width//2 + 30, self.y + self.height//2 + 50),
            (self.x + self.width//2, self.y + self.height//2 + 30)
        ]
        
        pygame.draw.polygon(screen, BLUE, fin_points_left)
        pygame.draw.polygon(screen, DARK_GRAY, fin_points_left, 2)
        pygame.draw.polygon(screen, BLUE, fin_points_right)
        pygame.draw.polygon(screen, DARK_GRAY, fin_points_right, 2)
        
        # Draw smoke particles
        for particle in self.smoke_particles:
            alpha = min(255, particle['life'] * 2.55)
            smoke_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, (100, 100, 100, alpha), 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(smoke_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))

class ScrapYard:
    def __init__(self):
        self.scrap_pieces = []
        self.generate_scrap()
        
    def generate_scrap(self):
        for _ in range(20):
            self.scrap_pieces.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': SCREEN_HEIGHT - 100,
                'width': random.randint(20, 60),
                'height': random.randint(20, 60),
                'color': (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150))
            })
            
    def draw(self, screen):
        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Draw scrap pieces
        for scrap in self.scrap_pieces:
            pygame.draw.rect(screen, scrap['color'], 
                           (scrap['x'], scrap['y'] - scrap['height'], scrap['width'], scrap['height']),
                           border_radius=5)
            pygame.draw.rect(screen, DARK_GRAY, 
                           (scrap['x'], scrap['y'] - scrap['height'], scrap['width'], scrap['height']),
                           2, border_radius=5)

class Planet:
    def __init__(self, x, y, radius, color, has_rings=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.has_rings = has_rings
        self.angle = 0
        
    def update(self):
        self.angle += 0.001
        
    def draw(self, screen):
        # Draw planet
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
        # Draw rings if applicable
        if self.has_rings:
            ring_rect = pygame.Rect(self.x - self.radius * 1.5, self.y - 10, self.radius * 3, 20)
            pygame.draw.ellipse(screen, (200, 200, 200), ring_rect, 3)

class AnimatedFilm:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Lonely Robot - Extended Animated Short Film")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize all game objects
        self.robot = Robot(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 150)
        self.rocket = Rocket(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 150)
        self.scrap_yard = ScrapYard()
        self.aliens = []
        self.space_station = SpaceStation(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        self.planets = [
            Planet(200, 150, 40, (255, 200, 100)),  # Yellow planet
            Planet(1000, 200, 60, (100, 200, 255), True),  # Blue planet with rings
            Planet(400, 100, 30, (200, 100, 200))   # Purple planet
        ]
        
        # Scene management
        self.current_scene = 1
        self.scene_timer = 0
        # Extended scene durations: [wandering, discovering, repairing, launching, space, aliens, homecoming, ending]
        self.scene_durations = [180, 180, 240, 180, 240, 300, 180, 180]
        
        self.stars = []
        self.generate_stars()
        
        # Scene-specific variables
        self.meteors = []
        self.friendship_items = []
    
    def generate_stars(self):
        for _ in range(200):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 4),
                'brightness': random.randint(100, 255),
                'twinkle_speed': random.random() * 0.05
            })
    
    def generate_meteors(self):
        self.meteors = []
        for _ in range(5):
            self.meteors.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-100, 0),
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(2, 5),
                'size': random.randint(5, 15),
                'trail': []
            })
    
    def generate_friendship_items(self):
        self.friendship_items = []
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        for _ in range(8):
            self.friendship_items.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'color': random.choice(colors),
                'collected': False
            })
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.advance_scene()
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r:  # Reset to first scene
                    self.current_scene = 1
                    self.scene_timer = 0
                    self.reset_scene()
    
    def advance_scene(self):
        self.current_scene += 1
        if self.current_scene > len(self.scene_durations):
            self.current_scene = 1
        self.scene_timer = 0
        self.reset_scene()
    
    def reset_scene(self):
        # Reset objects for new scene
        if self.current_scene == 1:
            self.robot.state = "wandering"
            self.robot.x = SCREEN_WIDTH // 4
            self.robot.y = SCREEN_HEIGHT - 150
            self.rocket.launched = False
            self.rocket.in_space = False
            self.rocket.y = SCREEN_HEIGHT - 150
            self.aliens = []
            
        elif self.current_scene == 2:
            self.robot.state = "discovering"
            self.robot.set_target(SCREEN_WIDTH * 3 // 4 - 100, SCREEN_HEIGHT - 150)
            
        elif self.current_scene == 3:
            self.robot.state = "repairing"
            
        elif self.current_scene == 4:
            self.robot.state = "launching"
            self.rocket.launch()
            
        elif self.current_scene == 5:  # Space journey
            self.robot.state = "wandering"
            self.rocket.in_space = True
            self.rocket.x = SCREEN_WIDTH // 2
            self.rocket.y = SCREEN_HEIGHT + 100
            self.generate_meteors()
            
        elif self.current_scene == 6:  # Alien encounter
            self.robot.state = "celebrating"
            # Create aliens
            self.aliens = [
                Alien(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2),
                Alien(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2),
                Alien(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            ]
            self.generate_friendship_items()
            
        elif self.current_scene == 7:  # Homecoming
            self.robot.state = "celebrating"
            self.rocket.in_space = False
            self.rocket.y = SCREEN_HEIGHT - 150
            
        elif self.current_scene == 8:  # Happy ending
            self.robot.state = "sleeping"
    
    def update(self):
        self.scene_timer += 1
        
        # Auto-advance scenes
        if self.scene_timer >= self.scene_durations[self.current_scene - 1]:
            self.advance_scene()
        
        # Update all objects
        self.robot.update()
        self.rocket.update()
        self.space_station.update()
        
        for planet in self.planets:
            planet.update()
            
        for alien in self.aliens:
            alien.update()
        
        # Scene-specific updates
        if self.current_scene == 5:  # Space journey with meteors
            for meteor in self.meteors:
                meteor['x'] += meteor['speed_x']
                meteor['y'] += meteor['speed_y']
                # Add to trail
                meteor['trail'].append((meteor['x'], meteor['y']))
                if len(meteor['trail']) > 10:
                    meteor['trail'].pop(0)
                
                # Reset meteor if it goes off screen
                if (meteor['y'] > SCREEN_HEIGHT or meteor['x'] < -50 or 
                    meteor['x'] > SCREEN_WIDTH + 50):
                    meteor['x'] = random.randint(0, SCREEN_WIDTH)
                    meteor['y'] = random.randint(-100, 0)
                    meteor['trail'] = []
        
        elif self.current_scene == 6:  # Alien friendship
            # Move robot to collect friendship items
            if not any(item['collected'] for item in self.friendship_items):
                self.robot.set_target(self.friendship_items[0]['x'], self.friendship_items[0]['y'])
            
            # Check if robot collected items
            for item in self.friendship_items:
                if not item['collected']:
                    distance = math.sqrt((self.robot.x - item['x'])**2 + (self.robot.y - item['y'])**2)
                    if distance < 30:
                        item['collected'] = True
                        # Move to next item
                        next_items = [i for i in self.friendship_items if not i['collected']]
                        if next_items:
                            self.robot.set_target(next_items[0]['x'], next_items[0]['y'])
    
    def draw_stars(self, screen):
        for star in self.stars:
            brightness = star['brightness'] + math.sin(pygame.time.get_ticks() * star['twinkle_speed']) * 50
            brightness = max(50, min(255, brightness))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (star['x'], star['y']), star['size'])
    
    def draw_scene_1(self):
        # Scene 1: Wandering in scrap yard
        self.screen.fill((70, 70, 100))
        self.scrap_yard.draw(self.screen)
        self.robot.draw(self.screen)
        
        text = self.font.render("Scene 1: The Lonely Robot Wanders the Scrap Yard", True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_scene_2(self):
        # Scene 2: Discovering the rocket
        self.screen.fill((50, 50, 150))
        self.scrap_yard.draw(self.screen)
        self.rocket.draw(self.screen)
        self.robot.draw(self.screen)
        
        text = self.font.render("Scene 2: A Discovery - The Broken Rocket", True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_scene_3(self):
        # Scene 3: Repairing the rocket
        self.screen.fill((100, 100, 200))
        self.scrap_yard.draw(self.screen)
        self.rocket.draw(self.screen)
        self.robot.draw(self.screen)
        
        text = self.font.render("Scene 3: The Great Repair", True, WHITE)
        self.screen.blit(text, (20, 20))
        
        # Show repair progress
        progress = min(1.0, self.scene_timer / self.scene_durations[2])
        progress_width = 300 * progress
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH//2 - 150, 60, 300, 20))
        pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH//2 - 150, 60, progress_width, 20))
    
    def draw_scene_4(self):
        # Scene 4: Launch sequence
        self.screen.fill((0, 0, 50))
        self.draw_stars(self.screen)
        self.scrap_yard.draw(self.screen)
        self.rocket.draw(self.screen)
        
        if self.scene_timer < 60:
            self.robot.draw(self.screen)
        
        text = self.font.render("Scene 4: Blast Off!", True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_scene_5(self):
        # Scene 5: Space journey
        self.screen.fill((0, 0, 30))
        self.draw_stars(self.screen)
        
        # Draw planets
        for planet in self.planets:
            planet.draw(self.screen)
        
        # Draw meteors with trails
        for meteor in self.meteors:
            # Draw trail
            for i, (trail_x, trail_y) in enumerate(meteor['trail']):
                alpha = int(255 * (i / len(meteor['trail'])))
                trail_size = meteor['size'] * (i / len(meteor['trail']))
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (255, 255, 255, alpha), 
                                 (trail_size, trail_size), trail_size)
                self.screen.blit(trail_surface, (trail_x - trail_size, trail_y - trail_size))
            
            # Draw meteor
            pygame.draw.circle(self.screen, ORANGE, (int(meteor['x']), int(meteor['y'])), meteor['size'])
        
        self.rocket.draw(self.screen)
        
        text = self.font.render("Scene 5: Journey Through the Cosmos", True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_scene_6(self):
        # Scene 6: Alien encounter
        self.screen.fill((0, 20, 40))
        self.draw_stars(self.screen)
        self.space_station.draw(self.screen)
        
        # Draw aliens
        for alien in self.aliens:
            alien.draw(self.screen)
        
        # Draw friendship items
        for item in self.friendship_items:
            if not item['collected']:
                pygame.draw.circle(self.screen, item['color'], (item['x'], item['y']), 15)
                pygame.draw.circle(self.screen, WHITE, (item['x'], item['y']), 15, 2)
        
        self.robot.draw(self.screen)
        
        text = self.font.render("Scene 6: New Friends in Space", True, WHITE)
        self.screen.blit(text, (20, 20))
        
        collected = sum(1 for item in self.friendship_items if item['collected'])
        total = len(self.friendship_items)
        friend_text = self.small_font.render(f"Friendship Gifts: {collected}/{total}", True, YELLOW)
        self.screen.blit(friend_text, (20, 60))
    
    def draw_scene_7(self):
        # Scene 7: Homecoming
        self.screen.fill((100, 100, 200))
        self.scrap_yard.draw(self.screen)
        self.rocket.draw(self.screen)
        self.robot.draw(self.screen)
        
        # Draw aliens visiting Earth
        for i, alien in enumerate(self.aliens):
            alien.x = SCREEN_WIDTH // 2 - 150 + i * 100
            alien.y = SCREEN_HEIGHT - 200
            alien.draw(self.screen)
        
        text = self.font.render("Scene 7: Homecoming with New Friends", True, WHITE)
        self.screen.blit(text, (20, 20))
    
    def draw_scene_8(self):
        # Scene 8: Happy ending
        self.screen.fill((30, 30, 80))
        self.draw_stars(self.screen)
        self.scrap_yard.draw(self.screen)
        
        # Robot sleeping under stars
        self.robot.draw(self.screen)
        
        # Draw moon
        pygame.draw.circle(self.screen, (200, 200, 200), (SCREEN_WIDTH - 100, 100), 40)
        
        text = self.font.render("Scene 8: No Longer Lonely - A Happy Ending", True, WHITE)
        self.screen.blit(text, (20, 20))
        end_text = self.small_font.render("The robot found friendship and purpose among the stars", True, LIGHT_BLUE)
        self.screen.blit(end_text, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2))
    
    def draw(self):
        # Draw current scene
        scene_methods = [
            self.draw_scene_1, self.draw_scene_2, self.draw_scene_3,
            self.draw_scene_4, self.draw_scene_5, self.draw_scene_6,
            self.draw_scene_7, self.draw_scene_8
        ]
        
        if 1 <= self.current_scene <= len(scene_methods):
            scene_methods[self.current_scene - 1]()
        
        # Draw scene info
        scene_text = self.small_font.render(f"Scene {self.current_scene}/8 - Press SPACE to skip scene", True, YELLOW)
        self.screen.blit(scene_text, (20, SCREEN_HEIGHT - 40))
        
        # Draw scene progress
        progress_width = (self.scene_timer / self.scene_durations[self.current_scene - 1]) * 200
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 30, 200, 10))
        pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 30, progress_width, 10))
    
    def run(self):
        print("The Lonely Robot - Extended Animated Short Film")
        print("Controls:")
        print("SPACE - Advance to next scene")
        print("R - Reset to first scene")
        print("ESC - Quit")
        print("\nStory:")
        print("Scene 1: Wandering in scrap yard")
        print("Scene 2: Discovering the rocket")
        print("Scene 3: Repairing the rocket")
        print("Scene 4: Launch sequence")
        print("Scene 5: Space journey with meteors")
        print("Scene 6: Making alien friends")
        print("Scene 7: Homecoming with friends")
        print("Scene 8: Happy ending")
        
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)

# Run the extended animated film
if __name__ == "__main__":
    film = AnimatedFilm()
    film.run()