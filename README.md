# Craig Reynolds’ Boids System

### General

Our program begins the implementation of Boids by initially setting all of the weights and constants as
global variables. The main function builds all of the required boids (stored in the global BOIDS array) and
initializes the graph used throughout the program. Every boid created has a random X and Y location
((0,0) being the top left corner), a randomly generated X and Y velocity, and a randomly generated
hexadecimal colour. Throughout the program, the functions ruleOne, ruleTwo, and ruleThree implement
logic that changes each boid’s velocity and location accordingly to increase cohesion with the group,
separation from immediate neighbours, and align velocity with local flockmates.

### Bad Boy-d

The Bad Boy-d is a creative element added that builds one boid that all the other boids choose to avoid.
This behaviour is immediately noticeable once the program is run with “BADBOY = True”. To truly enjoy 
this experience, please have “bad_boys_song.wav” in the same directory. The Bad Boy-ds still desires to 
be cohesive and close to the group, however all of the other boids choose to avoid them, especially when 
they are within a certain radius. You can change the number of bad boy-ds by increasing or decreasing the 
BADBOYNUM global variable. You can also change the influence of the bad boy-ds and the radius in which 
other boids feel their presence.

### Wind

Wind is a random gust of wind that happens according to the value of WINDTIMER, which is by default
set to 100. To see this behaviour, you must wait around 30 seconds. WINDCNT is incremented every
time the new locations of the boids are drawn to the graph, and once WINDCNT = WINDTIMER, a
random gust will occur. This behaviour only occurs when “WIND = True”.
The wind affects every boid on the graph with a random velocity according to the global variables; you
can also change the weight of the impact of the wind. A higher value of WINDWEIGHT means that the 
boids are more affected, and vice versa.

### Output

The output of the boids system is drawn to the screen using tkinter. Each boid is randomly assigned a
distinct colour, with Bad Boy-ds appearing in red.




