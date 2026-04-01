"""
PowerPoint Controller
Sends keyboard commands to control PowerPoint slideshow.
"""

import time

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    print("WARNING: pyautogui not found. Keyboard control disabled.")

KEY_DELAY = 0.05


def next_slide():
    """Send Right Arrow key to advance one slide."""
    if HAS_PYAUTOGUI:
        pyautogui.press('right')
    else:
        print("[SIMULATE] Next slide")


def prev_slide():
    """Send Left Arrow key to go back one slide."""
    if HAS_PYAUTOGUI:
        pyautogui.press('left')
    else:
        print("[SIMULATE] Previous slide")


def goto_slide(slide_number):
    """
    Jump to specific slide number in PowerPoint slideshow.
    Type the number then press Enter.
    """
    if HAS_PYAUTOGUI:
        slide_str = str(int(slide_number))
        for char in slide_str:
            pyautogui.press(char)
            time.sleep(KEY_DELAY)
        pyautogui.press('enter')
    else:
        print("[SIMULATE] Go to slide {}".format(slide_number))


def start_slideshow():
    """Press F5 to start slideshow from beginning."""
    if HAS_PYAUTOGUI:
        pyautogui.press('f5')
    else:
        print("[SIMULATE] Start slideshow")


def end_slideshow():
    """Press Escape to exit slideshow."""
    if HAS_PYAUTOGUI:
        pyautogui.press('escape')
    else:
        print("[SIMULATE] End slideshow")