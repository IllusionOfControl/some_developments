import cv2


filename = "video.avi"
frames_per_second = 24
dimensions = (1280, 720)
video_type = cv2.VideoWriter_fourcc(*'XVID')

cap = cv2.VideoCapture(0)
cap.set(3, dimensions[0])   # w
cap.set(4, dimensions[1])   # h

out = cv2.VideoWriter(filename, video_type, frames_per_second, dimensions)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    out.write(frame)
    cv2.imshow('frame_1', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
