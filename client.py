# client.py

import pygame
import threading
import socketio

# Server URL
SERVER_URL = 'http://localhost:5000'

# Create a Socket.IO client
sio = socketio.Client()

# Player's position
player_pos = {'x': 375, 'y': 375}

# Other players' positions
other_players = {}

@sio.event
def connect():
    print('Connected to server')
    sio.emit('connect_player')
    # Start the background task for sending player position
    sio.start_background_task(update_position)

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('update_players')
def on_update_players(data):
    global other_players
    other_players = data
    # Remove own player from the list
    other_players.pop(sio.sid, None)

def update_position():
    while True:
        sio.emit('set_player_position', player_pos)
        sio.sleep(0.01)  # Sleep for 10ms to reduce CPU usage

def network_thread():
    sio.connect(SERVER_URL)
    sio.wait()

def game_thread():
    global player_pos, other_players
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Multiplayer Game")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos['x'] -= 5
        if keys[pygame.K_RIGHT]:
            player_pos['x'] += 5
        if keys[pygame.K_UP]:
            player_pos['y'] -= 5
        if keys[pygame.K_DOWN]:
            player_pos['y'] += 5

        # Keep player within bounds
        player_pos['x'] = max(0, min(player_pos['x'], 750))
        player_pos['y'] = max(0, min(player_pos['y'], 750))

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw own player
        pygame.draw.rect(screen, (255, 0, 0), (player_pos['x'], player_pos['y'], 50, 50))

        # Draw other players
        for pid, pos in other_players.items():
            pygame.draw.rect(screen, (0, 0, 255), (pos['x'], pos['y'], 50, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sio.disconnect()

if __name__ == '__main__':
    threading.Thread(target=network_thread, daemon=True).start()
    game_thread()
