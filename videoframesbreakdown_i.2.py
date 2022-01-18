import cv2
import mediapipe

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

capture = cv2.VideoCapture('C://Users/srite/OneDrive/Desktop/Html/video.avi')

frameNr = 0

landmarks_x = []
length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
length_seconds = length/30
print(length)
print(length_seconds)


with handsModule.Hands() as hands:

    while (True):

        success, frame = capture.read()

        if not success:
            break

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmarks_x.append(handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].x)
            cv2.imwrite(f'C://Users/srite/OneDrive/Desktop/Html/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmarks_x.append(handLandmarks.landmark[handsModule.HandLandmark.PINKY_TIP].x)
            cv2.imwrite(f'C://Users/srite/OneDrive/Desktop/Html/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmarks_x.append(handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].x)
            cv2.imwrite(f'C://Users/srite/OneDrive/Desktop/Html/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmarks_x.append(handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].x)
            cv2.imwrite(f'C://Users/srite/OneDrive/Desktop/Html/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmarks_x.append(handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].x)
            cv2.imwrite(f'C://Users/srite/OneDrive/Desktop/Html/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1


tremor_count = 0
len_minutes = 1
tremor_threshold = 0.04
print(landmarks_x)
for i in range(1, len(landmarks_x)-1):
    if abs(landmarks_x[i] - landmarks_x[i-1]) > tremor_threshold:
        tremor_count = tremor_count + 1
print("Tremor count - {}".format(tremor_count))
print("")
frequency = tremor_count/length_seconds
capture.release()
print (frequency)

# Compare other fingers: Done
# Try out a combination of all fingers
# Draw the coordinates on the frame and compile a video to see how coordinates vary
