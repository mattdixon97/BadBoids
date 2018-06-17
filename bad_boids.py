from tkinter import *
from random import randint, uniform
from math import sqrt
from winsound import *

BOIDS = []              # Array to store all boids
BOIDNUM = 50            # Number of boids to make
RADIUS = 5              # Radius of each boid
MAXVEL = 5              # Max initial velocity of each boid
WIDTH = 700             # Width of grid
HEIGHT = 700            # Height of grid
BUFFER = 50             # Inital buffer between sides of grid
FRAMERATE = 40          # Refresh rate for graph
WALLFORCE = 5           # Acceleration per frame rate
RULE1 = 0.5             # Weight applied to rule one
RULE2 = 3               # Weight applied to rule two
RULE3 = 0.5             # Weight applied to rule three

# Global variables specific to bad boy functionality
# Make sure "bad_boys_song.wav" is in the directory
# We recommend having volume on :)
BADBOY = True           # Set True/False to see bad boy
BADBOYNUM = 2           # How many bad boy-ds do you want
BBWEIGHT = 3            # Weight of bad boy-d's influence
BADBOYDRADIUS = 50      # Radius of bad boy-d's influence

# Global variables specific to wind functionality
WIND = True             # Set True/False to see wind
WINDTIMER = 100         # Number of loops between random gusts of wind
WINDCNT = 0             # Keeps track of number of loops
WINDWEIGHT = 50         # Weighting of wind on velcity


def main():
    build_boids()
    initialise()


# Initialise the graph
def initialise():
    global graph
    root = Tk()
    root.title("BOIDS")
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.pack(expand=YES, fill=BOTH)
    graph.after(40, update)
    graph.pack()
    mainloop()


# Randomly generate the boids and append to BOIDS
def build_boids():
    global BOIDS
    global BOIDNUM
    global MAXVEL
    global BADBOYNUM
    # Randomly generate starting boid locations on perimeter
    for i in range(BOIDNUM):
        # If it is the last boid and BADBOY is True
        if (BADBOY and BADBOYNUM > 0):
            BADBOYNUM = BADBOYNUM -1
            build_bad_boyd()
        else:
            x =  uniform(0+BUFFER,WIDTH-BUFFER)
            y = uniform(0+BUFFER, HEIGHT-BUFFER)
            xVel = uniform(-MAXVEL,MAXVEL)/(FRAMERATE)
            yVel = uniform(-MAXVEL,MAXVEL)/(FRAMERATE)
            colour = randomColour()
            badboy = False
            BOIDS.append([x, y, xVel, yVel, colour, badboy])


# Build a bad boy-d and append to BOIDS
def build_bad_boyd():
    x = uniform(0+BUFFER,WIDTH-BUFFER)
    y = uniform(0+BUFFER, HEIGHT-BUFFER)
    xVel = uniform(-MAXVEL,MAXVEL)/(FRAMERATE)
    yVel = uniform(-MAXVEL,MAXVEL)/(FRAMERATE)
    colour = '#ff0000' #randomColour()
    badboyd = True
    playSong("bad_boys_song.wav")
    BOIDS.append([x, y, xVel, yVel, colour, badboyd])


# Generate a random hexadecimal colour
def randomColour():
    colour = "#" + "%06x" % randint(0, 0xFFFFFF)
    return colour

# Calculate the new velocity and location for each boid
# Update graph with the new information
def update():
    global BOIDS
    global RADIUS
    global FRAMERATE
    # Clear graph contents
    graph.delete("all")
    for boid in BOIDS:
        # Get the inital X,Y, velocity, and colour values
        X,Y,xVel,yVel,colour,badboy = boid

        # Check boundary, change location & velocity if close to edge
        X,Y,xVel,yVel = checkBoundaryAndVelocities(X,Y, xVel, yVel)

        # Update boid contents
        boid[0] = X
        boid[1] = Y
        boid[2] = xVel
        boid[3] = yVel

    # Calculate new locations for each boids
    updatedBoids = []

    # Calculate wind (if applicable)
    windX = 0
    windY = 0
    if (WIND):
        windX, windY = wind()

    for boid in BOIDS:
        # Get the inital X,Y, velocity, and colour values
        X,Y,xVel,yVel,colour,badboy = boid
        # Calculate the resulting vectors from the rules
        v1 = rule1(boid) # Cohesion
        v2 = rule2(boid) # Seperation
        v3 = rule3(boid) # Alignment

        # Calculate bad boy-d influence (if applicable)
        bb = [0,0]
        if (BADBOY and badboy == False):
            bb = badBoydInfluence(boid)

        # Update velocity vector with rules and weights
        xVel += (RULE1*v1[0] + RULE2*v2[0] + RULE3*v3[0] + WINDWEIGHT*windX + BBWEIGHT*bb[0]) / FRAMERATE
        yVel += (RULE1*v1[1] + RULE2*v2[1] + RULE3*v3[1] + WINDWEIGHT*windY + BBWEIGHT*bb[1]) / FRAMERATE

        # Update position vector according to the new velocity
        X += xVel
        Y += yVel

        # Update boid contents
        updatedBoids.append([X,Y,xVel,yVel,colour,badboy])

        # Draw new oval on graph
        graph.create_oval(X-RADIUS, Y-RADIUS, X+RADIUS, Y+RADIUS, width = 1, fill=colour)

    # Update graph
    BOIDS = updatedBoids
    graph.after(FRAMERATE, update)


# Cohesion - Steer to move toward the average position of local flockmates
def rule1(thisBoid):
    # Get the inital X,Y values
    X = thisBoid[0]
    Y = thisBoid[1]
    avgX = 0
    avgY = 0
    for boid in BOIDS:
        if (thisBoid != boid):
            avgX += boid[0]
            avgY += boid[1]
    # Normalize resulting X,Y values
    avgX = avgX / (BOIDNUM-1)
    avgY = avgY / (BOIDNUM-1)
    # Merge with previous X,Y values
    X = avgX - X
    Y = avgY - Y
    # Return resulting vector
    return [X,Y]

# Separation - Steer to avoid crowding local flockmates
def rule2(thisBoid):
    # Get the inital X,Y values
    X = thisBoid[0]
    Y = thisBoid[1]
    avgX = 0
    avgY = 0
    numNeighbours = 0
    for boid in BOIDS:
        if (boid != thisBoid):
            eucDistance = sqrt((abs(X-boid[0])**2) + (abs(Y-boid[1])**2))
            if (eucDistance < 30):
                avgX += boid[0]
                avgY += boid[1]
                numNeighbours += 1
    if (numNeighbours > 0):
        avgX = avgX / numNeighbours
        avgY = avgY / numNeighbours
        X = (X - avgX)
        Y = (Y - avgY)
        return [X,Y]
    elif (numNeighbours == 0):
        return [0,0]


# Alignment - Steer towards average heading of local flockmates
def rule3(thisBoid):
    # Get the inital X,Y values
    xVel = thisBoid[2]
    yVel = thisBoid[3]
    newXVel = 0
    newYVel = 0
    # Iterate through each boid
    for boid in BOIDS:
        if (thisBoid != boid):
            newXVel += boid[2]
            newYVel += boid[3]
    # Normalize resulting X,Y values
    newXVel = newXVel / (BOIDNUM-1)
    newYVel = newYVel / (BOIDNUM-1)
    # Merge with previous X,Y values
    newXVel = (xVel - (newXVel / 8))
    newYVel = (yVel - (newYVel / 8))
    # Return resulting vector
    return [newXVel,newYVel]

# Calculate a random effect of wind if applicable
# Increment WINDCNT everytime wind() is called
# If WINDCNT % WINDTIMER == 0, return random gust, else return [0,0]
def wind():
    global WINDCNT
    global WINDTIMER
    WINDCNT = WINDCNT+1
    if ((WINDCNT % WINDTIMER) == 0):
        WINDCNT = 0
        windX = uniform(-MAXVEL,MAXVEL)
        windY = uniform(-MAXVEL,MAXVEL)
        print("Random gust of wind:")
        print("   X Velocity: " +str(windX))
        print("   Y Velocity: " +str(windY) + "\n")
        return [windX,windY]
    return [0,0]


# Calculate the effect of the bad boy-d on the passed in boid
def badBoydInfluence(thisBoid):
    # Get the inital X,Y values
    X = thisBoid[0]
    Y = thisBoid[1]
    badboy = thisBoid[5]
    avgX = 0
    avgY = 0
    numNeighbours = 0
    for boid in BOIDS:
        if (boid[5] == True):
            # Calculate distance to bad boy-d
            eucDistance = sqrt((abs(X-boid[0])**2) + (abs(Y-boid[1])**2))
            if (eucDistance < BADBOYDRADIUS):
                avgX += boid[0]
                avgY += boid[1]
                avgX = avgX
                avgY = avgY
                X = (X - avgX)
                Y = (Y - avgY)
                return [X,Y]
    # If not close to bad boy-d, return [0,0]
    return [0,0]


# Play bad boys song if BADBOYD is True
def playSong(audio_file):
    PlaySound(audio_file, SND_ALIAS | SND_ASYNC)
    return


# Check that X,Y are within the boundary of the boid
# And that velocities are not above the maximum
# If not, bring within and correct velocities accordingly
def checkBoundaryAndVelocities(X,Y, xVel, yVel):
    # Limit velocities
    if (xVel > MAXVEL):
        xVel = MAXVEL
    elif (xVel < -MAXVEL):
        xVel = -MAXVEL
    if (yVel > MAXVEL):
        yVel = MAXVEL
    elif (yVel < -MAXVEL):
        yVel = -MAXVEL

    # Initialize new values
    newX = X
    newY = Y
    newXVel = xVel
    newYVel = yVel

    # Check boundary, adjust location and velocity accordingly
    if (X < 0 + BUFFER):
        newX = BUFFER
        newXVel = -newXVel
        newXVel += WALLFORCE
    elif (X > WIDTH - BUFFER):
        newX = WIDTH - BUFFER
        newXVel = -newXVel
        newXVel -= WALLFORCE
    if (Y < 0 + BUFFER):
        newY = BUFFER
        newYVel = -newYVel
        newYVel += WALLFORCE
    elif (Y > HEIGHT - BUFFER):
        newY = HEIGHT - BUFFER
        newYVel = -newYVel
        newYVel -= WALLFORCE

    # Return new values
    return newX, newY, newXVel, newYVel


main()
