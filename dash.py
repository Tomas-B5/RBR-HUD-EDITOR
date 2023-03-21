from enum import Enum
import os
import math
from Point import *
from debug import dbg

GEAR_COUNT = 9
REVMETER_COUNT = 28
TURBOMETER_COUNT = 9
RPM_COUNT = 8
ORDERED_OBJ_COUNT = 99
DEBUG=False

class LineType(Enum):
    X = 0,
    Y = 1,
    XY = 2,
    ALPHA = 3

class Dash_Object():
    name = ""
    hide = False

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name

    def Up(self, step):
        return 0

    def Down(self, step):
        return 0

    def Left(self, step):
        return 0

    def Right(self, step):
        return 0


class Group(Dash_Object):
    children = 0
    
    def __init__(self, name):
        self.name = name
        #If its declared in the class it is shared with all instances of the class -_-
        self.children = {}

    def Up(self, step):
        for o in self.children:
            self.children[o].Up(step)

    def Down(self, step):
        for o in self.children:
            self.children[o].Down(step)

    def Left(self, step):
        for o in self.children:
            self.children[o].Left(step)

    def Right(self, step):
        for o in self.children:
            self.children[o].Right(step)


class Simple(Dash_Object):
    Position = Point2D(-1000, -1000)
    # Limit_min = -9999
    # Limit_Max = 9999

    def __init__(self, name, pos):
        self.name = name
        self.Position = pos

    def Up(self, step):
        self.Position.y -= step
        return 0

    def Down(self, step):
        self.Position.y += step
        return 0

    def Left(self, step):
        self.Position.x -= step
        return 0

    def Right(self, step):
        self.Position.x += step
        return 0


class Alpha(Dash_Object):
    Alpha = 1.0

    def __init__(self, name, alpha):
        self.name = name
        self.Alpha = alpha


class RBR_DASH():
    # Array of all objects for drawing/etc
    filename=""
    obj_array_grouped = []
    obj_array_ordered = []

    HUD_Pos = Simple("HUD pos", Point2D(0, 0))
    HUD_Size = Simple("HUD size", Point2D(0, 0))
    obj_array_grouped.append(HUD_Pos)
    obj_array_grouped.append(HUD_Size)

    Group_gears = Group(">Gear Indicators")
    Group_gears.children["GEAR_R"] = (Simple("GEAR_R", Point2D(0, 0)))
    Group_gears.children["GEAR_N"] = (Simple("GEAR_N", Point2D(0, 0)))
    Group_gears.children["GEAR_1"] = (Simple("GEAR_1", Point2D(0, 0)))
    Group_gears.children["GEAR_2"] = (Simple("GEAR_2", Point2D(0, 0)))
    Group_gears.children["GEAR_3"] = (Simple("GEAR_3", Point2D(0, 0)))
    Group_gears.children["GEAR_4"] = (Simple("GEAR_4", Point2D(0, 0)))
    Group_gears.children["GEAR_5"] = (Simple("GEAR_5", Point2D(0, 0)))
    Group_gears.children["GEAR_6"] = (Simple("GEAR_6", Point2D(0, 0)))
    Group_gears.children["GEAR_Backlight"] = (Simple("GEAR_Backlight", Point2D(0, 0)))
    obj_array_grouped.append(Group_gears)

    Group_REV = Group(">Revmeter")
    for i in range(REVMETER_COUNT, 0, -1):
        Group_REV.children["REV_" + str(i)] = (Simple("REV_" + str(i), Point2D(0, 0)))
    obj_array_grouped.append(Group_REV)

    Group_turbo = Group(">Turbo(might be in reverse)")
    for i in range(TURBOMETER_COUNT, 0, -1):
        Group_turbo.children["TURBO_" + str(i)] = (Simple("TURBO_" + str(i), Point2D(0, 0)))
    obj_array_grouped.append(Group_turbo)

    Group_numbers = Group(">Numbers")
    Group_numbers.children["Speedo"] = (Simple("Speedo", Point2D(0, 0)))
    Group_numbers.children["Dist1"] = (Simple("Dist1", Point2D(0, 0)))
    Group_numbers.children["Dist2"] = (Simple("Dist2", Point2D(0, 0)))
    Group_numbers.children["EngineTemp"] = (
        Simple("EngineTemp", Point2D(0, 0)))
    obj_array_grouped.append(Group_numbers)

    Group_lights = Group(">Lights(add names)")
    Group_lights.children["LIGHT_1"] = (Simple("LIGHT_1", Point2D(0, 0)))
    Group_lights.children["LIGHT_2"] = (Simple("LIGHT_2", Point2D(0, 0)))
    Group_lights.children["LIGHT_3"] = (Simple("LIGHT_3", Point2D(0, 0)))
    Group_lights.children["LIGHT_4"] = (Simple("LIGHT_4", Point2D(0, 0)))
    Group_lights.children["LIGHT_5"] = (Simple("LIGHT_5", Point2D(0, 0)))
    Group_lights.children["LIGHT_6"] = (Simple("LIGHT_6", Point2D(0, 0)))
    obj_array_grouped.append(Group_lights)

    Group_labels = Group(">Labels")
    Group_labels.children["Speed"] = (Simple("Speed", Point2D(0, 0)))
    Group_labels.children["Turbo"] = (Simple("Turbo", Point2D(0, 0)))
    Group_labels.children["Temp"] = (Simple("Temp", Point2D(0, 0)))
    Group_labels.children["Dist1"] = (Simple("Dist1", Point2D(0, 0)))
    Group_labels.children["Dist2"] = (Simple("Dist2", Point2D(0, 0)))
    Group_labels.children["Dist3"] = (Simple("Dist3", Point2D(0, 0)))
    Group_labels.children["RPM"] = (Simple("RPM", Point2D(0, 0)))
    Group_labels.children["X1000"] = (Simple("X1000", Point2D(0, 0)))
    obj_array_grouped.append(Group_labels)

    Group_labels_RPM = Group(">RPM labels(might be in reverse)")
    for i in range(RPM_COUNT, 0, -1):
        Group_labels_RPM.children["RPM_LABEL_" + str(i)] = (Simple("RPM_LABEL_" + str(i), Point2D(0, 0)))
    obj_array_grouped.append(Group_labels_RPM)

    Group_alphas = Group(">Alpha Values")
    Group_alphas.children["Background"] = (Alpha("Background", 1))
    Group_alphas.children["Unlit"] = (Alpha("Unlit", 1))
    Group_alphas.children["Lit"] = (Alpha("Lit", 1))
    obj_array_grouped.append(Group_alphas)

    Group_shift_lights = Group(">Shift lights")
    Group_shift_lights.children["SHIFT_1"] = (Simple("SHIFT_1", Point2D(0, 0)))
    Group_shift_lights.children["SHIFT_2"] = (Simple("SHIFT_2", Point2D(0, 0)))
    obj_array_grouped.append(Group_shift_lights)

    # This one is for file read/write order
    def Build_Ordered_Array(self):
        ordered = []

        # Dashboard stuff
        ordered.append([self.HUD_Pos, LineType.X])
        ordered.append([self.HUD_Pos, LineType.Y])
        ordered.append([self.HUD_Size, LineType.X])
        ordered.append([self.HUD_Size, LineType.Y])

        # Gears X
        ordered.append([self.Group_gears.children["GEAR_R"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_N"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_1"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_2"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_3"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_4"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_5"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_6"], LineType.X])
        ordered.append([self.Group_gears.children["GEAR_Backlight"], LineType.X])

        # Gears Y
        ordered.append([self.Group_gears.children["GEAR_R"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_N"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_1"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_2"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_3"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_4"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_5"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_6"], LineType.Y])
        ordered.append([self.Group_gears.children["GEAR_Backlight"], LineType.Y])

        # Rev
        for i in range(REVMETER_COUNT, 0, -1):
            ordered.append([self.Group_REV.children["REV_" + str(i)], LineType.XY])

        # Turbo X
        for i in range(TURBOMETER_COUNT, 0, -1):
            ordered.append([self.Group_turbo.children["TURBO_" + str(i)], LineType.X])

        # Turbo Y
        for i in range(TURBOMETER_COUNT, 0, -1):
            ordered.append([self.Group_turbo.children["TURBO_" + str(i)], LineType.Y])

        # Live values
        ordered.append([self.Group_numbers.children["Speedo"], LineType.XY])
        ordered.append([self.Group_numbers.children["Dist1"], LineType.XY])
        ordered.append([self.Group_numbers.children["Dist2"], LineType.XY])
        ordered.append(
            [self.Group_numbers.children["EngineTemp"], LineType.XY])

        # Engine Lights
        ordered.append([self.Group_lights.children["LIGHT_1"], LineType.XY])
        ordered.append([self.Group_lights.children["LIGHT_2"], LineType.XY])
        ordered.append([self.Group_lights.children["LIGHT_3"], LineType.XY])
        ordered.append([self.Group_lights.children["LIGHT_4"], LineType.XY])
        ordered.append([self.Group_lights.children["LIGHT_5"], LineType.XY])
        ordered.append([self.Group_lights.children["LIGHT_6"], LineType.XY])

        # Labels
        ordered.append([self.Group_labels.children["Speed"], LineType.XY])
        ordered.append([self.Group_labels.children["Turbo"], LineType.XY])
        ordered.append([self.Group_labels.children["Temp"], LineType.XY])
        ordered.append([self.Group_labels.children["Dist1"], LineType.XY])
        ordered.append([self.Group_labels.children["Dist2"], LineType.XY])
        ordered.append([self.Group_labels.children["Dist3"], LineType.XY])
        ordered.append([self.Group_labels.children["RPM"], LineType.XY])

        # RPM labels
        for i in range(RPM_COUNT, 0, -1):
            ordered.append(
                [self.Group_labels_RPM.children["RPM_LABEL_" + str(i)], LineType.XY])

        # Shift lights
        ordered.append([self.Group_shift_lights.children["SHIFT_1"], LineType.XY])
        ordered.append([self.Group_shift_lights.children["SHIFT_2"], LineType.XY])

        # Alpha values
        ordered.append(
            [self.Group_alphas.children["Background"], LineType.ALPHA])
        ordered.append([self.Group_alphas.children["Unlit"], LineType.ALPHA])
        ordered.append([self.Group_alphas.children["Lit"], LineType.ALPHA])

        ordered.append([self.Group_labels.children["X1000"], LineType.XY])

        return ordered

    def Build_Array(self):
        return
    def __init__(self):
        return
    def read_file(self, file):
        self.filename=file
        f = open(file, "r")
        self.obj_array_ordered = self.Build_Ordered_Array()
        index = 0
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if line.startswith(";") or line.startswith("$") or not line:
                continue

            dbg("Line: " + line)

            match self.obj_array_ordered[index][1]:
                case LineType.X:
                    self.obj_array_ordered[index][0].Position.x = self.Read_X(
                        line)
                    dbg("Position: ")
                    dbg(self.obj_array_ordered[index][0].Position.x)
                    dbg(self.obj_array_ordered[index][0].Position.y)
                case LineType.Y:
                    self.obj_array_ordered[index][0].Position.y = self.Read_Y(
                        line)
                    dbg("Position: ")
                    dbg(self.obj_array_ordered[index][0].Position.x)
                    dbg(self.obj_array_ordered[index][0].Position.y)
                case LineType.XY:
                    self.obj_array_ordered[index][0].Position = self.Read_XY(
                        line)
                    dbg("Position: ")
                    dbg(self.obj_array_ordered[index][0].Position.x)
                    dbg(self.obj_array_ordered[index][0].Position.y)
                case LineType.ALPHA:
                    self.obj_array_ordered[index][0].Alpha = self.Read_Alpha(
                        line)
                    dbg("Alpha: ")
                    dbg(self.obj_array_ordered[index][0].Alpha)
                case _:
                    print("Unknown line type")
                    exit(1)
            index += 1

        if (index != ORDERED_OBJ_COUNT):
            print("ERROR: malformed cfg file?")
            print("index: " + str(index) +
                  " expected: " + str(ORDERED_OBJ_COUNT))
            exit(1)

    def Read_XY(self, line):
        if line[0] == 'x':
            line = line[1:]
        # Remove comment
        if ';' in line:
            line = line.split(';', 1)[0].strip()
        # Extract numbers
        numbers = line.split()
        x_number = float(numbers[0])
        y_number = float(numbers[1])
        return Point2D(x_number, y_number)

    def Read_X(self, line):
        if line[0] == 'x':
            line = line[1:]
        if ';' in line:
            # split on the first ';' and take the first part, then remove leading/trailing whitespace
            line = line.split(';', 1)[0].strip()
        number = float(line)
        return number

    def Read_Y(self, line):
        if line[0] == 'y':
            line = line[1:]
        if ';' in line:
            # split on the first ';' and take the first part, then remove leading/trailing whitespace
            line = line.split(';', 1)[0].strip()
        number = float(line)
        return number

    def Read_Alpha(self, line):
        if ';' in line:
            # split on the first ';' and take the first part, then remove leading/trailing whitespace
            line = line.split(';', 1)[0].strip()
        number = float(line)
        return number
    
    def ScaleX(self, value):
        for obj in self.obj_array_ordered:
            if type(obj[0]) is Alpha:
                continue
            obj[0].Position.x = obj[0].Position.x * value
    
    def ScaleY(self, value):
        for obj in self.obj_array_ordered:
            if type(obj[0]) is Alpha:
                continue
            obj[0].Position.y = obj[0].Position.y * value    
    
    def ScaleXY(self, value):
            self.ScaleX(value)
            self.ScaleY(value)

    def Output_Dash(self, file):
        if file == "":
            return False
        print("Writing to file: " + file)
        f = open(file, "w+")
        f.write("; RBR dash editor by Towerbrah\n")

        for obj in self.obj_array_ordered:
            match obj[1]:
                case LineType.X:
                    if DEBUG:
                        f.write("; " + obj[0].name + " X" + "\n")
                    f.write(str(obj[0].Position.x) + "\n")
                case LineType.Y:
                    if DEBUG:
                        f.write("; " + obj[0].name + " Y" + "\n")
                    f.write(str(obj[0].Position.y) + "\n")
                case LineType.XY:
                    if DEBUG:
                        f.write("; " + obj[0].name + " XY" + "\n")
                    f.write(str(obj[0].Position.x) + " " +
                            str(obj[0].Position.y) + "\n")
                case LineType.ALPHA:
                    if DEBUG:
                        f.write("; " + obj[0].name + " Alpha" + "\n")
                    f.write(str(obj[0].Alpha) + "\n")
                case _:
                    print("Unknown line type")
                    exit(1)
        f.write("$")
        f.close()
        return True
 