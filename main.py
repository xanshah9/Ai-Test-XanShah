#!/usr/bin/env python3
"""
Super Mario Bros - Python Edition
Entry point: main.py

Run with: python main.py
Requires: pip install pygame
"""

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)

    # Try to create a resizable window with a nice icon color
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()

    # Set window icon (simple red square as placeholder)
    icon = pygame.Surface((32, 32))
    icon.fill((220, 30, 30))
    pygame.draw.rect(icon, (255, 220, 0), (8, 8, 16, 16))
    pygame.display.set_icon(icon)

    # Show a splash/loading frame
    screen.fill((30, 80, 160))
    font = pygame.font.SysFont("Arial", 36, bold=True)
    loading = font.render("Loading...", True, (255, 255, 255))
    screen.blit(loading, (SCREEN_WIDTH//2 - loading.get_width()//2,
                           SCREEN_HEIGHT//2 - loading.get_height()//2))
    pygame.display.flip()

    # Create and run game
    game = Game(screen, clock)
    game.run()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
