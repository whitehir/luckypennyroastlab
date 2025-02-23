# Blue Bear Roast Probe Assembly (BBRPA)
#
# Author: R. Whitehill
# Version: 0.1
# Date: 28 Nov 2024
#
# Creates an interface to monitor roast metrics using a Popper coffee roaster
#

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FixedFormatter, FixedLocator
import time, datetime, os, subprocess, csv
import numpy as np
import mysql.connector

global start_time
global coffeeName
start_time = time.time()

slideFile = "./Outputs/tmpSlide.txt"
crackFile = "./Outputs/tmpCrack.txt"
if os.path.exists(crackFile):
    os.remove(crackFile)
with open(crackFile, 'w') as h:
    pass

# --------------------------------------------------
# Define Functions
# --------------------------------------------------
def plot_data(coffeeName="Generic", xTarg=[], yTarg=[]):
    # Initialize plot and variables
    plt.ion()
    global fig
    y1Old = 500
    fig, axs = plt.subplots(4, 1)
    ax2 = axs[0].twinx()
    xTime, xTime2, chamberTemp, chamberRate, ambientTemp, sliderValue = [], [], [], [], [], []
    
    line1, = axs[0].plot(xTime, chamberTemp, color='C0', label='Chamber')
    line2, = axs[3].plot(xTime, ambientTemp, color='C2', label='Ambient')
    line3, = axs[0].plot(xTarg, yTarg, color='black', linestyle="--", linewidth=0.5, label='Target')
    line4, = ax2.plot(xTime, chamberRate, color='gray', label='dT/dt')
    legLines, legLabels = axs[0].get_legend_handles_labels()
    legLines2, legLabels2 = ax2.get_legend_handles_labels()
    axs[0].legend(legLines + legLines2, legLabels + legLabels2, loc='upper right')
    axs[0].set_title(coffeeName + " - " + datetime.datetime.now().strftime("%d %b %Y"))
    step, = axs[1].step(xTime, sliderValue, color='C7')
    axs[0].set_ylabel("Chamber Temperature (degF)")
    axs[3].set_ylabel("Ambient Temperature (degF)")
    ax2.set_ylabel("dT/dt (degF/sec)")
    axs[1].set_ylabel("Power Setting (kW)")
    axs[2].set_ylabel("Bean Crack Events")
    axs[3].set_xlabel("Elapsed Time (Minutes)")
    fig.set_size_inches(6.5, 10)
    
    
    axs[0].autoscale(enable=None, axis='y')
    axs[0].set_xlim(0, 20)
    ax2.set_ylim(0, 4)
    axs[0].xaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].xaxis.set_major_locator(MultipleLocator(5))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
    
    axs[1].set_ylim(0, 8)
    axs[1].set_xlim(0, 20)
    axs[1].xaxis.set_minor_locator(AutoMinorLocator(5))
    axs[1].xaxis.set_major_locator(MultipleLocator(5))
    axs[1].yaxis.set_major_locator(MultipleLocator(8))
    axs[1].yaxis.set_major_locator(FixedLocator([1, 2, 3, 4, 5, 6, 7]))
    axs[1].yaxis.set_major_formatter(FixedFormatter(['A', 'B', 'C', 'D', 'E', 'F', 'G']))
    
    axs[2].xaxis.set_minor_locator(AutoMinorLocator(5))
    axs[2].xaxis.set_major_locator(MultipleLocator(5))
    axs[2].set_ylim(0, 2)
    axs[2].set_xlim(0, 20)
    axs[2].yaxis.set_ticks([])
    axs[2].yaxis.set_ticklabels([])
    
    axs[3].set_xlim(0, 20)
    axs[3].xaxis.set_minor_locator(AutoMinorLocator(5))
    axs[3].xaxis.set_major_locator(MultipleLocator(5))
    axs[3].yaxis.set_minor_locator(AutoMinorLocator(5))
    
    previousLinesOne = 0
    previousLinesTwo = 0
    previousLinesThree = 0
    filename = "./Outputs/" + coffeeName.replace(" ", "") + "_" + datetime.datetime.now().strftime("%d%b%Y") +".txt"
    
    while True:
        
        with open(filename, 'r') as f:

            #  Read file line
            linesOne = f.readlines()

            if len(linesOne) > previousLinesOne:
                # Read and map data points
                y1, y2 = map(float, linesOne[-1].strip().split(','))
                chamRate = y1 - y1Old
                y1Old = y1
                elapsed_time = time.time() - start_time
                xTime.append(elapsed_time/60)
                if previousLinesOne == 0:
                        axs[3].set_ylim(y2-5, y2+5)
    
                # Append read or cacluated time to data vector
                chamberTemp.append(y1)
                ambientTemp.append(y2)
                chamberRate.append(chamRate/5)
    
                # Generate plot data
                line1.set_data(xTime, chamberTemp)
                line2.set_data(xTime, ambientTemp)
                line4.set_data(xTime, chamberRate)
                y1_str = f"{y1:.1f} degF"
                chamReading = tk.Label(root, text=y1_str, font=("Arial", 10), fg="red")
                chamReading.place(x=10, y=460)
    
                # Draw and rescele plot
                axs[0].autoscale(enable=None, axis='y')
                axs[0].relim()
                
                previousLinesOne = len(linesOne)
        
        with open(slideFile, 'r') as g:
            linesTwo = g.readlines()
            if len(linesTwo) > previousLinesTwo:
                y3 = linesTwo[-1].strip()
                sliderValue.append(int(y3))
                elapsed_time = time.time() - start_time
                xTime2.append(elapsed_time/60)
                # step.set_data(xTime2, sliderValue)
                axs[1].step(xTime2, sliderValue, where='post', color='grey')
                # axs[1].relim()
                previousLinesTwo = len(linesTwo)
                
        with open(crackFile, 'r') as h:
            linesThree = h.readlines()
            if len(linesThree) > previousLinesThree:
                if previousLinesThree == 0:
                    oneStart = float(linesThree[-1].strip())
                elif previousLinesThree == 1:
                    oneDuration = float(linesThree[-1].strip()) - oneStart
                    axs[2].broken_barh([(oneStart, oneDuration)], (0.5, 1), facecolors='lightsteelblue')
                elif previousLinesThree == 2:
                    twoStart = float(linesThree[-1].strip())
                elif previousLinesThree == 3:
                    twoDuration = float(linesThree[-1].strip()) - twoStart
                    axs[2].broken_barh([(twoStart, twoDuration)], (0.5, 1), facecolors='slategray')
                    axs[2].legend(['First', 'Second'])
                    
                previousLinesThree = len(linesThree)
                
        insert_sql_data(y1, chamRate/5, y3)     
        plt.draw()
        plt.pause(1)

def calculateElapsedTime(start_time, crackSelection):
    if crackSelection == 1:      # Crack 1 Start
        crack1Start = (time.time() - start_time)/60
        labelCrack1Start.config(text=f"Elapsed Time: {crack1Start:.1f} Minutes")
        append_to_file(crackFile, crack1Start)
    elif crackSelection == 2:    # Crack 1 End
        crack1End = (time.time() - start_time)/60
        labelCrack1End.config(text=f"Elapsed Time: {crack1End:.1f} Minutes")
        append_to_file(crackFile, crack1End)
    elif crackSelection == 3:     # Crack 2 Start
        crack2Start = (time.time() - start_time)/60
        labelCrack2Start.config(text=f"Elapsed Time: {crack2Start:.1f} Minutes")
        append_to_file(crackFile, crack2Start)
    elif crackSelection == 4:     # Crack 2 End
        crack2End = (time.time() - start_time)/60
        labelCrack2End.config(text=f"Elapsed Time: {crack2End:.1f} Minutes")
        append_to_file(crackFile, crack2End)

def append_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(str(text) + '\n')

def read_csv_data(filename):
    xTarg, yTarg = [], []
    with open(filename, 'r') as h:
        reader = csv.reader(h)
        for row in reader:
            xTarg.append(float(row[0])/60)
            yTarg.append(float(row[1]))
    return xTarg, yTarg

def scale_changed(event):
    text_to_append = scale.get()
    append_to_file(slideFile, text_to_append)

def targetSelector(event):
    global targetValue
    global xTarg
    global yTarg
    targetValue = selectedTarget.get()
    if targetValue == "Ethiopia Dry Process Gerba Doku (Full City+)":
        xTarg, yTarg = read_csv_data('./Targets/EthiopiaDryProcessGerbaDoku_28Dec2024.csv')
    elif targetValue == "Ethiopia Dry Process Gerba Doku (French)":
        xTarg, yTarg = read_csv_data('./Targets/EthiopiaDryProcessGerbaDoku_29Dec2024.csv')
    elif targetValue == "Kenya Nyeri Kamoini AB (Full City)":
        xTarg, yTarg = read_csv_data('./Targets/KenyaNyeriKamoiniAB2_14Feb2025.csv')
    else:
        xTarg, yTarg = read_csv_data('./Targets/testProfile.csv')
    dropdown.config(state='disabled')
    
def get_coffee_name():
    global coffeeName
    global dataCollection
    coffeeName = entryCoffeeName.get()
    coffeeNameStrip = coffeeName.replace(" ", "")
    dataCollection = subprocess.Popen(["python3", "fileWritter_5sec.py", coffeeNameStrip])
    
def crackPlot(axis, oneStart=0.0, oneDuration=0.0, twoStart=0.0, twoDuration=0.0):
	# fig, ax = plt.subplots()
	ax.broken_barh([(oneStart, oneDuration)], (0.5, 1), facecolors='lightsteelblue')
	ax.broken_barh([(twoStart, twoDuration)], (0.5, 1), facecolors='slategray')

	ax.set_ylim(0, 2)
	ax.set_xlim(0, 20)
	ax.legend(['First', 'Second'])

	# Set y-axis limits to 0 and 1
	ax.yaxis.set_ticks([])  # Remove y-axis ticks
	ax.yaxis.set_ticklabels([])

def end_collection(fig):
    try: 
        dataCollection.terminate()
    except subprocess.TimeoutExpired:
        dataCollection.kill()
        
    figSaveFile = "./Outputs/" + coffeeName.replace(" ", "") + "_" + datetime.datetime.now().strftime("%d%b%Y") + ".png"
    fig.savefig(figSaveFile, dpi=75)
    time.sleep(3)
    exit(0)

def insert_sql_data(cham, chamChange, slider):

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="grafanaReader",
            password="spw",
            database="coach"
        )
        cursor = conn.cursor()
        current_time = datetime.datetime.now()
        
        sql = "INSERT INTO roaster (timestamp, chamber, chamberChange, sliderSetting) VALUES (%s, %s, %s, %s)" 
        cursor.execute(sql, (current_time, cham, chamChange, slider))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")
        return False

# --------------------------------------------------
# Create the main window and initialize variables
# --------------------------------------------------
root = tk.Tk()
root.title("Roast Window")
root.geometry("400x500+200+200")
title_label = tk.Label(root, text="Blue Bear Roasting", font=("Arial", 14), fg="blue")
title_label.place(x=10, y=10)

# ----------------------------------------------------------
# Create text labels
# ----------------------------------------------------------
labelCrack1Start = tk.Label(root, text="Elapsed Time:")
labelCrack1Start.place(x=200, y=215)
labelCrack1End = tk.Label(root, text="Elapsed Time:")
labelCrack1End.place(x=200, y=260)
labelCrack2Start = tk.Label(root, text="Elapsed Time:")
labelCrack2Start.place(x=200, y=305)
labelCrack2End = tk.Label(root, text="Elapsed Time:")
labelCrack2End.place(x=200, y=350)
labelRoastSetting = tk.Label(root, text="Power Setting")
labelRoastSetting.place(x=10, y=135)

# ----------------------------------------------------------
# Create buttons
# ----------------------------------------------------------
# First Crack
buttonCrack1Start = tk.Button(root, text="Start First", command=lambda: [calculateElapsedTime(start_time, 1), buttonCrack1Start.config(state=tk.DISABLED)], width=15, height=1)
buttonCrack1Start.place(x=10, y=210)
buttonCrack1End = tk.Button(root, text="End First", command=lambda: [calculateElapsedTime(start_time, 2), buttonCrack1End.config(state=tk.DISABLED)], width=15, height=1)
buttonCrack1End.place(x=10, y=255)

# Second Crack
buttonCrack2Start = tk.Button(root, text="Start Second", command=lambda: [calculateElapsedTime(start_time, 3), buttonCrack2Start.config(state=tk.DISABLED)], width=15, height=1)
buttonCrack2Start.place(x=10, y=300)
buttonCrack2End = tk.Button(root, text="End Second", command=lambda: [calculateElapsedTime(start_time, 4), buttonCrack2End.config(state=tk.DISABLED)], width=15, height=1)
buttonCrack2End.place(x=10, y=345)

# Start Collection
buttonStartCollection = tk.Button(root, text="Start Data Collection", command=lambda: [buttonStartCollection.config(state=tk.DISABLED), plot_data(coffeeName, xTarg, yTarg)], width=18, height=1)
buttonStartCollection.place(x=10, y=420)
buttonEndCollection = tk.Button(root, text="End Data Collection", command=lambda: [end_collection(fig)], width=18, height=1)
buttonEndCollection.place(x=205, y=420)

# ----------------------------------------------------------
# Other Inputs
# ----------------------------------------------------------
# Coffe Name
labelCoffeeName = tk.Label(root, text="Coffee Name: ")
labelCoffeeName.place(x=10, y=45)
entryCoffeeName = tk.Entry(root, width=23)
entryCoffeeName.place(x=110, y=45)
buttonSaveCoffeeName = tk.Button(root, text="Set", command=lambda: [get_coffee_name(), buttonSaveCoffeeName.config(state=tk.DISABLED), entryCoffeeName.config(state=tk.DISABLED)])
buttonSaveCoffeeName.place(x=330, y=40)

# Target Selector
labelTargetName = tk.Label(root, text="Target Profile: ")
labelTargetName.place(x=10, y=85)
selectedTarget = tk.StringVar(root)
selectedTarget.set("None Selected")
dropdown = tk.OptionMenu(root, selectedTarget, "Ethiopia Dry Process Gerba Doku (Full City+)", "Ethiopia Dry Process Gerba Doku (French)", "Kenya Nyeri Kamoini AB (Full City)", command=targetSelector)
dropdown.place(x=110, y=80)

# Create slider
scale = tk.Scale(root, from_=0, to=7, orient=tk.HORIZONTAL, length=375, command=scale_changed)
scale.place(x=10, y=155)


# ----------------------------------------------------------
# Other Stucture
# ----------------------------------------------------------
hSeparator1 = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
hSeparator1.place(x=10, y=125, relwidth=0.95)
hSeparator2 = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
hSeparator2.place(x=10, y=400, relwidth=0.95)

root.mainloop()

