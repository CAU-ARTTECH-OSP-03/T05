import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles # 미디어 파이프 내 모든 그리기를 담당, 우리의 포즈를 시각화하기 위해서 필요
mp_pose = mp.solutions.pose # 미디어 파이프 내 모든 포즈 추정 모델 불러옴. 
# Curl counter variables
counter = 0 
stage = 'Down'
exercise_name = ''
cnt = 0

# arctan2를 활용한 각도 계산 코드(0 ~ 파이) 
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return int(angle)


def input_workout():
    print("1 : Squats, 2 : Deadlift, 3 : Bench Press")
    type_of_exercise = int(input("Please input the type of exercise number : "))
    return type_of_exercise
    
    
# 실시간 비디오 불러오기
cap = cv2.VideoCapture(0)

type_exercise = input_workout()

## Setup mediapipe instance
### confidence 값 높아지면 감지도가 더 높아짐.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB(openCV 기본형식이 bgr이라 우리가 활용하기 위해서 rgb로 변환)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection(이미지를 detection한 결과값을 저장)
        results = pose.process(image)
    
        # Recolor back to BGR(rgb 데이터를 다시 bgr 데이터로 변환)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates(필요한 점 설정)
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            left_heel  = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
            
            
            # Classification of pose
            if type_exercise == 1:
                exercise_name = 'Squats'
                
                # calculate knee angle
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                
                # Visalize angle
                cv2.putText(image, str(left_knee_angle), 
                           tuple(np.multiply(left_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
                cv2.putText(image, str(right_knee_angle), 
                           tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                
                # Curl counter logic
                if left_knee_angle > 160 and right_knee_angle > 160:
                    stage = "down"
                if left_knee_angle < 90 and left_knee_angle > 70 and right_knee_angle < 90 and right_knee_angle > 70 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
            
            
            ################################################################################################################################
            elif type_exercise == 2:
                
                exercise_name = 'Deadlift'
                
                # calculate hip & knee angle
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                
                left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                
                # Visalize angle                
                cv2.putText(image, str(left_hip_angle), 
                           tuple(np.multiply(left_hip, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                cv2.putText(image, str(right_hip_angle), 
                           tuple(np.multiply(right_hip, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                
                cv2.putText(image, str(left_knee_angle), 
                           tuple(np.multiply(left_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
                cv2.putText(image, str(right_knee_angle), 
                           tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                
                # Curl counter logic
                if left_hip_angle < 100 and right_hip_angle < 100 and cnt == 0:
                    print('success_step_1')
                    stage = "down"
                    cnt = 1
                
                if stage == 'down' and cnt == 1:
                    if left_hip_angle > 160 and right_hip_angle > 160:
                        stage = "up"
                        counter += 1
                        print(counter)
                        
                if stage == 'up' and cnt == 1:
                    if left_hip_angle < 100 and right_hip_angle < 100:
                        stage = "down"
                    
                    
############################################################################################################################################
            elif type_exercise == 3:
                exercise_name = 'Bench Press'
                
                # calculate hip & knee angle
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                
                # Visalize angle
                cv2.putText(image, str(left_elbow_angle), 
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
                cv2.putText(image, str(right_elbow_angle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                
                 #Curl counter logic
                if left_elbow_angle < 95 and right_elbow_angle < 95:
                    stage = "up"
                if left_elbow_angle > 120 and right_elbow_angle > 120 and stage =='up':
                    stage="down"
                    counter +=1
                    print(counter)
                    
            else :
                exercise_name = 'Out_of_range'


        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (255,90), (245,117,16), -1)
        
        # Exercise_name data
        cv2.putText(image, exercise_name, (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        # Rep data
        cv2.putText(image, 'REPS', (15,30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,83), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,83), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections(라인 그리기)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        
        # 화면 닫기 단축키 설정
        key = cv2.waitKey(33) & 0xFF #q
        if key == ord('q'):
            type_exercise = input_workout()
            counter = 0
            
        elif cv2.waitKey(5) & 0xFF == 27: #esc
            break
            
cap.release()
cv2.destroyAllWindows()