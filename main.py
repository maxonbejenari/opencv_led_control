import cv2
import mediapipe as mp
import serial
import time

###################### INIT pyserial connection
try:
    board = serial.Serial(port='PORT_NAME', timeout=0.1) #CHANGE ME
    print("CONNECTED")
    time.sleep(2)
except Exception as e:
    print(f"COULD NOT CONNECT THE ARDUINO BOARD {e}")
    board = None
######################

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

def count_raised_fingers(hand_landmarks) -> int:
    tip_index = [8, 12, 16, 20]
    fingers_raised = []
    
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        fingers_raised.append(1)
    else:
        fingers_raised.append(0)   
    
    for tip_id in tip_index:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers_raised.append(1)
        else:
            fingers_raised.append(0)
    
    return sum(fingers_raised)

def send_data(total_fingers, previous_fingers) -> int:
    if board is not None and total_fingers != previous_fingers:
        command_string = f"{total_fingers}\n"
        
        board.write(command_string.encode('utf-8'))
        print(f"Sent to the Board: {command_string.strip()}")
        
        return total_fingers
    
    return previous_fingers

def draw_landmarks(results, frame):
    previous_fingers = -1 # we sent this to remeber what we sent last time, to not spam Arduino
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
            )
            total_fingers = count_raised_fingers(hand_landmarks)
            previous_fingers = send_data(total_fingers, previous_fingers)
                
            cv2.putText(frame, f"Count: {total_fingers}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
            
    elif previous_fingers != 0:
        previous_fingers = send_data(0, previous_fingers)
        
def main():
    with mp_hands.Hands(
        max_num_hands = 1,
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7,
    ) as hands:
        while True:
            success, frame = cap.read()
            if not success and frame is None:
                print("Could not get image frame")
                break
                
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            
            draw_landmarks(results, frame)
            
            cv2.imshow("Image", frame)

            if cv2.waitKey(1) and 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()
    if board is not None:
        board.write("0\n".encode('utf-8'))
        board.close()

if __name__ == "__main__":
    main()

