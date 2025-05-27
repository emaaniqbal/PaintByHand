"""
PAINT GAME

Guide / Instructions
===============================
This module contains the code for the paint game. Make sure all the files are in the same location.
To interact with the interface, use a raised pointer finger on either hand.
Hover over UI elements to make a selection.

Functionalities:
    - Changing Colours
    - Clear Canvas
    - Increase Brush Size
    - Decrease Brush Size
    - Save Painting (It will save .jpg images into the PaintbyHand file)
    - Quit

Libraries used: mediapipe, OpenCV, pygame
https://github.com/emaaniqbal
===============================
"""
import pygame
import cv2 as cv
import HandTrackingClass as ht
import UIShapeClass
import tkinter.simpledialog
import tkinter.messagebox


def drawUI():
    """
    Fxn contains all the drawing shape methods for the toolbar
    :return:None
    """
    for c in clr_collection:
        pygame.draw.rect(window, c.clr, c.rect)
    for t in tool_collection:
        pygame.draw.rect(window, t.clr, t.rect)
        text_des = font.render(f"{t.des}", True, (255, 255, 255))
        window.blit(text_des, (t.x + 20, t.y + 10))


# CV/hand detector set up
cap = cv.VideoCapture(0)  # Open default camera
if not cap.isOpened():
    print("Camera cannot be opened at this time.")
    exit()

# pygame set up
pygame.init()
window = pygame.display.set_mode((560, 500))
window.fill((255, 255, 255))
pygame.display.set_caption("Paint")
running = True

# create handtracker obj
detector = ht.HandTracker(False, 1, 0.7, 0.7)

side_bar_region = UIShapeClass.UIshape((128, 128, 128), 400, 0, 200, 520)
# paint clrs-> define our shapes, which gives clrs +ui parameters
clr_collection = [
    UIShapeClass.UIshape((255, 0, 0), 410, 20, 30, 30, "Red"),  # red -> 0
    UIShapeClass.UIshape((255, 165, 0), 460, 20, 30, 30, "Orange"),  # orange -> 1
    UIShapeClass.UIshape((255, 255, 0), 410, 80, 30, 30, "Yellow"),  # yellow -> 2
    UIShapeClass.UIshape((0, 255, 0), 460, 80, 30, 30, "Green"),  # green -> 3
    UIShapeClass.UIshape((0, 0, 255), 410, 140, 30, 30, "Blue"),  # blue -> 4
    UIShapeClass.UIshape((128, 0, 125), 460, 140, 30, 30, "Purple"),  # purple -> 5
    UIShapeClass.UIshape((255, 192, 203), 410, 200, 30, 30, "Pink"),  # pink -> 6
    UIShapeClass.UIshape((0, 0, 0), 460, 200, 30, 30, "Black"),  # blk -> 7
    UIShapeClass.UIshape((255, 255, 255), 510, 20, 30, 30, "White")  # white -> 8
]

# tool_collection, def clrs for tool ui + regions/zones
tool_collection = [
    UIShapeClass.UIshape((90, 90, 90), 420, 260, 120, 30, "Clear"),  # clear canvas -> 0
    UIShapeClass.UIshape((90, 90, 90), 420, 300, 120, 30, "Inc. Size"),  # change size -> 1
    UIShapeClass.UIshape((90, 90, 90), 420, 340, 120, 30, "Dec. Size"),  # change size -> 2
    UIShapeClass.UIshape((90, 90, 90), 420, 380, 120, 30, "Save"),  # save-> 3
    UIShapeClass.UIshape((90, 90, 90), 420, 420, 120, 30, "Quit")  # quit-> 4
]

# canvas base
paint_canvas = pygame.Surface((400, 500))
paint_canvas.fill((255, 255, 255))

# font data
font = pygame.font.SysFont("", 24, 2)

# brush data
base_clr = (0, 0, 0)
base_brush = 5

# time settings
cd_time = 500
hover_time = 0

while running:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)  # flip the frame so it's propelry mirrored
    frame = detector.hand_processor(frame, True)
    lst_hand_data = detector.get_postion(frame, 0, False)

    # draw in the ui
    pygame.draw.rect(window, side_bar_region.clr, side_bar_region.rect)
    drawUI()

    # set up landmarks
    x1, y1 = None, None  # rep lndmark 8
    x2, y2 = None, None  # rep lndmark 6

    if len(lst_hand_data) != 0:
        x1, y1 = lst_hand_data[8][1], lst_hand_data[8][2]
        x2, y2 = lst_hand_data[6][1], lst_hand_data[6][2]
        cv.circle(frame, (x1, y1), 10, (0, 0, 255), 2)
        cv.putText(frame, f"Location: {x1, y1}", (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

    # finding collisions -> https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
    # to have a valid point on the screen, make sure our (x,y) values aren't none
    if (x1 is not None and y1 is not None) and (x2 is not None and y2 is not None):
        if y1 < y2:
            # cycle tru the color boxes, seee if there is a collidepoint, if so, save that clr
            for c in clr_collection:
                if c.rect.collidepoint((x1, y1)):
                    base_clr = c.clr
                    clr_des = font.render(f"{c.des}", True, c.clr)
                    window.blit(clr_des, (420, 460))
            # cycle thru tool collection, check name of tool collection, and cause event
            curr_time = pygame.time.get_ticks()
            if (curr_time - hover_time) >= cd_time:
                hover_time = curr_time
                for t in tool_collection:
                    if t.rect.collidepoint((x1, y1)):
                        if t.des == "Clear":
                            paint_canvas.fill((255, 255, 255))

                        if t.des == "Inc. Size":  # inc brush size
                            if base_brush < 100:
                                base_brush += 10

                        if t.des == "Dec. Size":
                            if base_brush > 5:
                                base_brush -= 5

                        if t.des == "Quit":
                            pygame.quit()
                            cap.release()
                            cv.destroyAllWindows()

                        if t.des == "Save":
                            my_painnting = tkinter.simpledialog.askstring("Save", "Save as:")

                            if my_painnting is None:
                                pass
                            elif my_painnting.strip() == "":
                                tkinter.messagebox.showwarning("Error", "Cannot save without a file name!")
                            else:
                                pygame.image.save(paint_canvas, f"{my_painnting}.jpg")

            # render draiwing
            if (0 <= x1 <= 400) and (0 <= y1 <= 520):
                pygame.draw.circle(paint_canvas, base_clr, (x1, y1), base_brush)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    cv.imshow("WebCam", frame)
    if cv.waitKey(1) == ord("q"):  # press q to quit
        break

    # ui update
    brush_des = font.render(f"Brush size: {base_brush}", True, (0, 0, 0))
    window.blit(brush_des, (420, 480))

    # UPDATE CANVAS
    window.blit(paint_canvas, (0, 0))

    # cursor after update canvas
    r = 255 - base_clr[0]
    g = 255 - base_clr[1]
    b = 255 - base_clr[2]
    # center argument must be a pair of numbers -> check x1, y1 again
    if (x1 is not None and y1 is not None) and (x2 is not None and y2 is not None):
        if r == 255 and g == 255 and b == 255:
            pygame.draw.circle(window, (255, 209, 223), (x1, y1), 5)
        else:
            pygame.draw.circle(window, (r, g, b), (x1, y1), 5)

    pygame.display.flip()

pygame.quit()
cap.release()
cv.destroyAllWindows()
