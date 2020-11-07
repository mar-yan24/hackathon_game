import pygame, sys, random

#make the floor move to the left at a constant rate
def move_floor():
	screen.blit(floor, (floor_x_pos, 625))
	screen.blit(floor, (floor_x_pos + 450, 625))

#add a rect to the list
def create_pipe():
	random_pipe_pos = random.randint(250, 600)
	bot_pipe = pipe_surface.get_rect(midtop = (525, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (525, random_pipe_pos - 200))
	return bot_pipe, top_pipe

#influences all the rectangles and then makes a new list of new rects
def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

#draws the pipes
def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 700:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

#checks if two rects collide
def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top < -50 or bird_rect.bottom > 625:
		can_score = True
		return False

	return True

#rotate the bird depending on whether or not it is falling or flying
def rotated_bird(bird):
	return pygame.transform.rotozoom(bird, bird_movement * -4, 1)

#cycle through the animation of the bird and create a new rect around the different bird
def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (70, bird_rect.centery))
	return new_bird, new_bird_rect

#display the score on the screen
def score_display(game_state):
	#just print the regular score
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (225, 80))
		screen.blit(score_surface, score_rect)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (225, 80))
		screen.blit(score_surface, score_rect)

		#print the high score that has been achieved
		high_score_surface = game_font.render(f'High  Score: {int(high_score)}', True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect(center = (225, 575))
		screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score

	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

#initialize the screen so that it cna actually display stuff
pygame.init()
screen = pygame.display.set_mode((450, 700))
#set up a clock that can control the framerate that the screen is running at
clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.ttf', 40)

#game variabes
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#setup bg and floor to fit the display surface
bg = pygame.transform.scale((pygame.image.load('sprites/background-day.png').convert()), (450, 700))
floor = pygame.transform.scale((pygame.image.load('sprites/base.png').convert()), (500, 100))
floor_x_pos = 0

#initialize multiple different birds in different flap motion and cycle through them
bird_downflap = pygame.transform.scale((pygame.image.load('sprites/yellowbird-downflap.png').convert_alpha()), (55, 40))
bird_midflap = pygame.transform.scale((pygame.image.load('sprites/yellowbird-midflap.png').convert_alpha()), (55, 40))
bird_upflap = pygame.transform.scale((pygame.image.load('sprites/yellowbird-upflap.png').convert_alpha()), (55, 40))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]

#create a rectangle around the bird so you can rotate and check for collision
bird_rect = bird_surface.get_rect(center = (70, 350))

#set up the flapping cycle
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#make a list for pipe rects
pipe_surface = pygame.transform.scale((pygame.image.load('sprites/pipe-green.png').convert()), (70, 500))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

#import the message screen
game_over_surface = pygame.transform.scale((pygame.image.load('sprites/message.png').convert_alpha()), (300, 400))
game_over_rect = game_over_surface.get_rect(center = (225, 350))

#import sounds
flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

#we want the game to run until some event happens (like a death or a mouse click) and then we close the game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0 
				bird_movement -= 8
				flap_sound.play()

			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (70, 350)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface, bird_rect = bird_animation()

	#display the surface on the display surface (backgorund surface at (0,0))
	screen.blit(bg,(0,0))

	if game_active:

		#make the bird move down
		#d = -8*bird_movement + 1.5*bird_movement**2

		#if d >= 16:
			#d = 16

		#if d < 0:
			#d -= 2

		bird_movement += gravity
		rotate_bird = rotated_bird(bird_surface)
		bird_rect .centery += bird_movement
		screen.blit(rotate_bird, bird_rect)
		game_active = check_collision(pipe_list)

		#making/moving pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		score_display('main_game')

		pipe_score_check()
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')



	#floor constantly moves
	floor_x_pos -= 1
	move_floor()
	if floor_x_pos <= -450:
		floor_x_pos = 0

	#constantly update the display
	pygame.display.update()

	#controls the framerate
	clock.tick(100)