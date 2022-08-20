import cv2


cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    cv2.imshow('frame_1', frame)
    cv2.imshow('frame_2', frame)
    cv2.imshow('frame_3', frame)
    cv2.imshow('frame_4', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()