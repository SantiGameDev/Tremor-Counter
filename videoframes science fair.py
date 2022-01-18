# Ensure you have created the directory C:/Users/srite/tremor_videos and C:/Users/srite/tremor_videos/output

import cv2
import math
import mediapipe

# Editable parameters
tremor_threshold = 0.0305  # Threshold value for displacement
skip_frame = 1  # Number of frames to skip when processing

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# Read the stored video
capture = cv2.VideoCapture('C:/Users/srite/Desktop/Tremor/video.avi')
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))

size = (frame_width, frame_height)
# Create a new output video with hand tracked
result = cv2.VideoWriter('C:/Users/srite/Desktop/Tremor/Output/video.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

frameNr = 0
landmark_ring_x = []
landmark_thumb_x = []
landmark_pinky_x = []
landmark_middle_x = []
landmark_index_x = []

landmark_ring_y = []
landmark_thumb_y = []
landmark_pinky_y = []
landmark_middle_y = []
landmark_index_y = []

with handsModule.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7) as hands:
    while (True):
        success, frame = capture.read()
        if not success:
            break

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                landmark_ring_x.append(handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].x)
                landmark_thumb_x.append(handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].x)
                landmark_pinky_x.append(handLandmarks.landmark[handsModule.HandLandmark.PINKY_TIP].x)
                landmark_middle_x.append(handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].x)
                landmark_index_x.append(handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].x)

                landmark_ring_y.append(handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].y)
                landmark_thumb_y.append(handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].x)
                landmark_pinky_y.append(handLandmarks.landmark[handsModule.HandLandmark.PINKY_TIP].x)
                landmark_middle_y.append(handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].x)
                landmark_index_y.append(handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].x)
            result.write(frame)
            cv2.imshow("video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            # cv2.imwrite(f'C://Users/srite/tremor_videos/frames/frame_{frameNr}.jpg', frame) #Enable above if frames need to be saved
        frameNr = frameNr + 1
tremor_count = 0

# Computing the displacements for all fingers (sqrt((x2-x1)^2 + (y2-y1)^2) and comparing with threshold. We increase tremor count even if the displacement exceeds threshold for one finger.
for i in range(skip_frame, len(landmark_ring_x) - skip_frame, skip_frame):
    dist_between_frames_ring = math.sqrt(math.pow((landmark_ring_x[i] - landmark_ring_x[i - skip_frame]), 2) + math.pow(
        (landmark_ring_y[i] - landmark_ring_y[i - skip_frame]), 2))
    dist_between_frames_thumb = math.sqrt(
        math.pow((landmark_thumb_x[i] - landmark_thumb_x[i - skip_frame]), 2) + math.pow(
            (landmark_thumb_y[i] - landmark_thumb_y[i - skip_frame]), 2))
    dist_between_frames_pinky = math.sqrt(
        math.pow((landmark_pinky_x[i] - landmark_pinky_x[i - skip_frame]), 2) + math.pow(
            (landmark_pinky_y[i] - landmark_pinky_y[i - skip_frame]), 2))
    dist_between_frames_middle = math.sqrt(
        math.pow((landmark_middle_x[i] - landmark_middle_x[i - skip_frame]), 2) + math.pow(
            (landmark_middle_y[i] - landmark_middle_y[i - skip_frame]), 2))
    dist_between_frames_index = math.sqrt(
        math.pow((landmark_index_x[i] - landmark_index_x[i - skip_frame]), 2) + math.pow(
            (landmark_index_y[i] - landmark_index_y[i - skip_frame]), 2))

    if (
            dist_between_frames_ring >= tremor_threshold or dist_between_frames_thumb >= tremor_threshold or dist_between_frames_pinky >= tremor_threshold or dist_between_frames_middle >= tremor_threshold or dist_between_frames_index >= tremor_threshold):
        tremor_count = tremor_count + 1

print("Tremor count - {}".format(tremor_count))
print("")
length_seconds = frameNr / 30
frequency = tremor_count / length_seconds
print("Frequency - {} hz".format(frequency))
capture.release()