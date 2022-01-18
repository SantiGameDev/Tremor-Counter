import cv2
import processframe

capture = cv2.VideoCapture(0)

while True:

    ret, frame = capture.read()

    if ret:
        cv2.imshow('video', frame)
        ProcessFrame(frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()

cv2.destroyAllWindows()
