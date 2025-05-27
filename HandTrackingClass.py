"""
Hand Tracking Class
"""
import cv2 as cv
import mediapipe as mp


class HandTracker:
    """
    Hand Tracking Class
    """
    def __init__(self, mode=False, maxHands=2, detect_confi=0.5, track_confi=0.5):
        """
        Constructor for hands
        :param mode: Whether to treat the input images all only detection or detection and track with confidence.
        :param maxHands: Num of hands followed on the screen
        :param detect_confi:
        :param track_confi:
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detect_confi = detect_confi
        self.track_confi = track_confi

        # init the hands class. mp.solutions.hands -> Solutions/models in media pipe for the hands
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        model_complexity=1,
                                        min_detection_confidence=self.detect_confi,
                                        min_tracking_confidence=self.track_confi)
        self.mpDraw = mp.solutions.drawing_utils  # draws landmarks + connections

    def hand_processor(self, frame, draw=True):
        """
        This fxn is a visualizer (based on draw) and the major hand detector
        :param frame:
        :param draw:
        :return:frame:
        """
        # convert frame to RGB
        self.result = self.hands.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))  #
        lndmarks = self.result.multi_hand_landmarks
        if lndmarks:  # .multi_hand_landmarks is the collection of detected/tracked hand landmarks
            for handlmk in lndmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handlmk, self.mphands.HAND_CONNECTIONS)

        return frame

    def get_postion(self, frame, num_hands=0, draw=True):
        """
        Fxn returns list of data with landmark, and it's respetive (x,y) cords
        :param frame:
        :param num_hands:
        :param draw:
        :return: lm_list: List contians landmark id [0], x-cord of landmark [1], y-cord of landmark [2], as an ele in
        list.
        """
        lm_list = []
        lndmarks = self.result.multi_hand_landmarks
        if lndmarks:
            if num_hands < len(lndmarks):
                curr_hand = lndmarks[num_hands]
                for i, lm in enumerate(curr_hand.landmark):
                    h, w, c = frame.shape
                    # cx,cy tracks the x,y of the various lankmarks based on the index
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([i, cx, cy])

                    if draw and i == 0:
                        # shows hand that is in use/curr tracked
                        cv.circle(frame, (cx, cy), 15, (0, 0, 255), cv.FILLED)

        return lm_list


def main():
    """
    Webcam set up for hand detection.
    """
    cap = cv.VideoCapture(0)  # Open default camera
    if not cap.isOpened():
        print("Camera cannot be opened at this time.")
        exit()

    # create handtracker obj
    detector = HandTracker()
    while True:
        ret, frame = cap.read()

        frame = detector.hand_processor(frame, True)  # detectes hands
        lst_hand_data = detector.get_postion(frame, 0, True)  # gets postion

        frame = cv.flip(frame, 1)  # flip the frame so it's properly mirrored
        cv.imshow("WebCam", frame)

        if cv.waitKey(1) == ord("q"):  # press q to quit
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
