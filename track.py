import cv2
import mediapipe as mp
import os
import numpy as np

# --- CONFIGURATION ---
# Folder path where images are stored ('.' means current folder)
IMAGE_FOLDER = "." 
# Size to resize the overlay images to (width, height)
OVERLAY_SIZE = (150, 150) 

class HandTracker:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.images = self.load_images()
        
        # New check: Exit if no images were loaded at all
        if not self.images:
            print("🛑 CRITICAL ERROR: No valid gesture images were loaded. Please check your image files.")
            exit()


    def load_images(self):
        """Loads images into a dictionary with robust error checking."""
        img_dict = {}
        filenames = {
            "close": "close.png",
            "open": "open.png",
            "one": "one.png",
            "two": "two.png"
        }
        
        for key, filename in filenames.items():
            path = os.path.join(IMAGE_FOLDER, filename)
            # cv2.IMREAD_UNCHANGED loads the image including the alpha channel
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED) 
            
            if img is None:
                print(f"🛑 WARNING: Could not load {filename}. File is missing or corrupted.")
            
            elif img.shape[2] != 4:
                # The image was found, but it lacks the 4th (Alpha/Transparency) channel, 
                # causing the original IndexError.
                print(f"⚠️ WARNING: {filename} has {img.shape[2]} channels (expected 4). Skipping this gesture image.")
                
            else:
                # Image found and has 4 channels (BGRA), proceed.
                img = cv2.resize(img, OVERLAY_SIZE)
                img_dict[key] = img
                print(f"✅ Loaded {filename} successfully.")
                
        return img_dict

    def overlay_image(self, background, overlay, x, y):
        """Overlays a PNG with transparency onto the video frame."""
        h, w = overlay.shape[:2]
        bh, bw = background.shape[:2]

        # Check bounds to ensure we don't draw outside the screen
        if y < 0 or y + h > bh or x < 0 or x + w > bw:
            return background

        # Separate Alpha channel and BGR channels
        # Accessing index 3 is now SAFE because load_images ensures shape[2] == 4
        alpha_channel = overlay[:, :, 3] / 255.0
        overlay_colors = overlay[:, :, :3]
        
        # Region of Interest (ROI) on the background
        roi = background[y:y+h, x:x+w]

        # Blend the images
        for c in range(0, 3):
            roi[:, :, c] = roi[:, :, c] * (1 - alpha_channel) + overlay_colors[:, :, c] * alpha_channel

        background[y:y+h, x:x+w] = roi
        return background

    def count_fingers(self, lm_list):
        """Counts fingers and returns the gesture name."""
        if not lm_list:
            return None

        fingers = []
        
        # Thumb (Check if tip is to the left/right of knuckle depending on hand)
        # Note: This logic assumes right hand for simplicity. 
        # For left hand, the logic flips. MediaPipe detects handedness if needed.
        if lm_list[4][1] < lm_list[3][1]: # Adjust logic based on hand facing
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers (Index, Middle, Ring, Pinky)
        # Check if tip (id 8,12,16,20) is higher (lower y value) than PIP joint (id 6,10,14,18)
        tip_ids = [8, 12, 16, 20]
        for id in tip_ids:
            if lm_list[id][2] < lm_list[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)
        
        # Determine Gesture
        if total_fingers == 0:
            return "close"
        elif total_fingers == 1: # Usually just index
            return "one"
        elif total_fingers == 2: # Usually index + middle
            return "two"
        elif total_fingers >= 4: # Open hand
            return "open"
        else:
            return None

    def run(self):
        cap = cv2.VideoCapture(0) 

        while True:
            success, img = cap.read()
            if not success:
 
                print("Error reading frame from webcam.")
                break


            img = cv2.flip(img, 1)
            

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:



                    lm_list = []
                    h, w, c = img.shape
                    for id, lm in enumerate(hand_lms.landmark):
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append([id, cx, cy])


                    gesture = self.count_fingers(lm_list)
                    

                    if gesture and gesture in self.images:
                        wrist_x = lm_list[0][1]
                        wrist_y = lm_list[0][2]

                        img_x = wrist_x - 50
                        img_y = wrist_y - 200
                        
                        img = self.overlay_image(img, self.images[gesture], img_x, img_y)

            cv2.imshow("Hand Tracker Custom", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()