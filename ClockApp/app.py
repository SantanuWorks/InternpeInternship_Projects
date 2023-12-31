# Required modules
from tkinter import * # GUI interface
from time import strftime # Time utility
import math # Calculate point on circle

# Defining some colors 
LIME = "Lime"
PURPLE = "Purple"

# Defining height and width of clock body
HEIGHT = 400
WIDTH = 400

# Creating main window of clock application
ClockApp = Tk()

# Set name of the window
ClockApp.title("Hybrid Clock")

# Defining the minimum and maximum window size
ClockApp.minsize(460, 470)
ClockApp.maxsize(460, 470)

# Defiing clock body
ClockBody = Frame(ClockApp)
ClockBody.pack()

# Defining clock dial - circular base
ClockDial = Canvas(ClockBody, height = HEIGHT, width = WIDTH)
ClockDial.pack(side = TOP)

# Defining digital display - digital interface
ClockDigitalDisplay = Label(ClockBody, font = ("ds-digital", 35), foreground = PURPLE)
ClockDigitalDisplay.pack(side = BOTTOM)

# Defining clock controller class
# Provides contraints and logic working of clock
class ClockController:
    # Center of the clock
    h = HEIGHT/2
    k = WIDTH/2

    # Length of hands
    sec_rad = 170
    min_rad = 140
    hr_rad = 100

    # Angle of rotation
    sec_theta = 0 
    min_theta = 0 
    hr_theta = 0
    
    # Draw the clock disc dial
    def DrawClockDial(self):
        # Draw main dial
        ClockDial.create_oval(10, 10, HEIGHT-10, WIDTH-10, fill = LIME, outline = PURPLE)
        # Draw center dial - small - enhance beauty
        ClockDial.create_oval(ClockController.h-5, ClockController.k-5, ClockController.h+5, ClockController.k+5, fill = PURPLE, outline = LIME)
    
    def DrawClockAdditionals(self):
        # Draw hour time stamps
        times = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        for a in range(0, 12):
            x = 170 * math.cos(math.radians(a * 30) - math.radians(90)) + ClockController.h
            y = 170 * math.sin(math.radians(a * 30) - math.radians(90)) + ClockController.k
            ClockDial.create_text(x, y, text = str(times[a]), fill = PURPLE, font = ('Helvetica 13 bold'))

        # Draw minute bullets
        for a in range(0, 60):
            if a%5 == 0:
                continue
            x = 172 * math.cos(math.radians(a * 6) - math.radians(90)) + ClockController.h
            y = 172 * math.sin(math.radians(a * 6) - math.radians(90)) + ClockController.k
            ClockDial.create_text(x, y, text = str("."), fill = PURPLE, font = ('Helvetica 10 bold'))

    # Get current time values 
    def GetCurrTimeVals(self):
        return int(strftime("%S")), int(strftime("%M")), int(strftime("%H"))
    
    # Calculate angle of rotations for all hands 
    def CalRotationAngles(self, sec_val, min_val, hr_val):
        sec_rot_angle = math.radians(sec_val * 6) - math.radians(90)
        min_rot_angle = math.radians(min_val * 6) - math.radians(90)
        hr_rot_angle = math.radians(hr_val * 30) - math.radians(90)
        return sec_rot_angle, min_rot_angle, hr_rot_angle

    # Find the point on circle
    def CalXYOnCircle(self, radius, angle):
        x = radius * math.cos(angle) + ClockController.h
        y = radius * math.sin(angle) + ClockController.k
        return x, y

    # Draw the clock hands
    def DrawClockHands(self):
        # Get the time values
        second, minute, hour = self.GetCurrTimeVals()

        # Calculate angle of rotations for respective hands
        ClockController.sec_theta, ClockController.min_theta, ClockController.hr_theta = self.CalRotationAngles(second, minute, hour)
        
        # Determine the corresponding (x, y) on circle for hands
        sec_x, sec_y = self.CalXYOnCircle(ClockController.sec_rad, ClockController.sec_theta)
        min_x, min_y = self.CalXYOnCircle(ClockController.min_rad, ClockController.min_theta)
        hr_x, hr_y = self.CalXYOnCircle(ClockController.hr_rad, ClockController.hr_theta)

        # Plot coordinates and display
        ClockDial.create_line(ClockController.h, ClockController.k, sec_x, sec_y, fill = PURPLE, smooth = 1)
        ClockDial.create_line(ClockController.h, ClockController.k, min_x, min_y, fill = PURPLE, smooth = True, width = 3)
        ClockDial.create_line(ClockController.h, ClockController.k, hr_x, hr_y, fill = PURPLE, smooth = True, width = 5)

    # Draw the physical clock design - base method
    def DrawPhysicalClock(self):
        # Draw the clock dial
        self.DrawClockDial()
        
        # Draw minute bullets and hour time stamps
        self.DrawClockAdditionals()

        # Draw clock hands
        self.DrawClockHands()

    def Run(self):
        # Draw physical clock
        self.DrawPhysicalClock()
        
        # Get clock time for digital display
        # String formated time
        timestr = strftime("%H : %M : %S %p")
        
        # Set time on display
        ClockDigitalDisplay.config(text = timestr)

        # Update time each second
        ClockBody.after(1000, self.Run)

# Initalizing the clock controller object
Clock = ClockController()

# Start the clock
Clock.Run()

# Keep running the window
ClockApp.mainloop()