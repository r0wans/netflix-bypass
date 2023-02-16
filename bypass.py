import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import psutil
import keyboard
import os
text = """
███╗   ██╗███████╗████████╗███████╗██╗     ██╗██╗  ██╗    ██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║     ██║╚██╗██╔╝    ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝
██╔██╗ ██║█████╗     ██║   █████╗  ██║     ██║ ╚███╔╝     ██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗ Press q to exit recording.
██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║     ██║ ██╔██╗     ██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║
██║ ╚████║███████╗   ██║   ██║     ███████╗██║██╔╝ ██╗    ██████╔╝   ██║   ██║     ██║  ██║███████║███████║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝    ╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝

                                                                                                        """#
print(text)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 25
record_seconds = 15



browser_process_names = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe', 'opera.exe']
browser_processes = set(p.info['name'] for p in psutil.process_iter(['name']) if p.info['name'] in browser_process_names)


print("Available browser processes:")
for i, process in enumerate(browser_processes):
    print(f"{i+1}. {process}")

selection = None
while selection is None:
    try:
        selection = int(input("\nEnter the number of the process to record: "))
        if selection < 1 or selection > len(browser_processes):
            raise ValueError()
    except:
        print("Invalid selection. Please try again.")
        selection = None


process_name = list(browser_processes)[selection-1]
process_name = os.path.splitext(os.path.basename(process_name))[0]
process_name = process_name.capitalize()

w = gw.getWindowsWithTitle(process_name)[0]
if w != []:
    try:
        w.activate()
    except:
        w.minimize()
        w.maximize()
out = cv2.VideoWriter("output.avi", fourcc, fps, tuple(w.size))


for i in range(int(record_seconds * fps)):
    img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    if keyboard.is_pressed('q'):
        break


os.startfile("output.avi")
cv2.destroyAllWindows()
out.release()
