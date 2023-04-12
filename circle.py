import math

points = 9
r = 18
start = 90
end = 360
clockwise = False
twice=True
reverse = True

# Calculate the angular interval between consecutive points
if clockwise:
    interval = -1 * (end - start) / (points - 1)
else:
    interval = (end - start) / (points - 1)

# Convert start angle to radians
start_rad = math.radians(start)

# Generate the coordinates of the points
runs = 0
def print_cord():
    global runs
    runs += 1
    if reverse:
        rng=range(points,0, -1)
    else:
        rng=range(points)
    for i in rng:
        #print(i)
        # Calculate the angle for this point
        if clockwise:
            angle = start_rad + math.radians(i * interval)
        else:
            angle = start_rad + math.radians((points - 1 - i) * interval)
        
        # Calculate the x and y coordinates for this point
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        # Print the coordinates
        if twice and runs==1:
            print(f"{x:.2f}")
        elif twice and runs==2:
            print(f"{y:.2f}")
        else:    
            print(f"{x:.2f} {y:.2f}")
    if runs == 1:
        print_cord()
            
print_cord()