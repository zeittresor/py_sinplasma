import pygame
import math
import colorsys
import sys

pygame.init()

infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Demoscene Effect")

FPS = 60
clock = pygame.time.Clock()

phase_left = 0.0
speed_left = 0.02  
frequency_left = 0.01  
amplitude_left = height * 0.1 

phase_right = 0.0
speed_right = 0.025  
frequency_right = 0.012  
amplitude_right = height * 0.1  

base_x_left = width * 0.25
base_x_right = width * 0.75

num_samples = height

max_freq_change = 0.0001
max_amp_change = height * 0.0005

frequency_min = 0.005
frequency_max = 0.015
amplitude_min = height * 0.05
amplitude_max = height * 0.15

def hsb_to_rgb(h, s, v):
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple([int(c * 255) for c in rgb])

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    screen.fill((0, 0, 0))

    phase_left += speed_left
    phase_right += speed_right

    frequency_left += max_freq_change * (math.sin(phase_left) * 0.5)  
    frequency_left = max(frequency_min, min(frequency_left, frequency_max))  

    frequency_right += max_freq_change * (math.cos(phase_right) * 0.5)  
    frequency_right = max(frequency_min, min(frequency_right, frequency_max))  

    amplitude_left += max_amp_change * (math.cos(phase_left) * 0.5)  
    amplitude_left = max(amplitude_min, min(amplitude_left, amplitude_max))

    amplitude_right += max_amp_change * (math.sin(phase_right) * 0.5)  
    amplitude_right = max(amplitude_min, min(amplitude_right, amplitude_max)) 

    for y in range(num_samples):
        x_left = base_x_left + amplitude_left * math.sin(frequency_left * y + phase_left)
        x_right = base_x_right + amplitude_right * math.sin(frequency_right * y + phase_right)

        distance = x_right - x_left

        max_distance = 2 * (amplitude_left + amplitude_right)
        min_distance = -2 * (amplitude_left + amplitude_right)

        hue = ((distance - min_distance) / (max_distance - min_distance)) * 360
        hue = hue % 360  

        saturation = 1.0
        brightness = 1.0

        color = hsb_to_rgb(hue / 360, saturation, brightness)

        pygame.draw.line(screen, color, (int(x_left), y), (int(x_right), y))

    pygame.display.flip()

pygame.quit()
sys.exit()
