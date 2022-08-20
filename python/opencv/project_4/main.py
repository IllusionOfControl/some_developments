import numpy as np
import cv2


def verify_alpha_channel(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame


def apply_invert(frame):
    return cv2.bitwise_not(frame)


def apply_sepia(frame, intensity=0.7):
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, _ = frame.shape
    sepia_bgra = (20, 66, 112, 1)
    overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame


def alpha_blend(frame_1, frame_2, mask):
    alpha = mask / 255
    blended = cv2.convertScaleAbs(frame_1 * (1 - alpha) + frame_2 * alpha)
    return blended


def apply_cucle_focus_blur(frame):
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, _ = frame.shape
    x, y = int(frame_w / 2), int(frame_h / 2)
    center = (x, y)
    radius = int(y / 4)
    mask = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    cv2.circle(mask, center, radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask, (21, 21), 11)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, 255-mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


def apply_portrait(frame):
    frame = verify_alpha_channel(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow('mask', mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    invert_frame = apply_invert(frame)
    sepia = apply_sepia(frame.copy())
    blur = apply_cucle_focus_blur(frame.copy())
    portrait = apply_portrait(frame.copy())

    cv2.imshow('frame', frame)
    cv2.imshow('invert', invert_frame)
    cv2.imshow('sepia', sepia)
    cv2.imshow('blur', blur)
    cv2.imshow('portrait', portrait)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
