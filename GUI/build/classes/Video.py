import cv2, pyvirtualcam
from classes.ImageSimilarity import ImageSimilarityCalculator


class Video:
    def __init__(
        self,
        threshold,
        fps,
        stop_frame_transfer,
        similarity_rate_b_frame,
        button_1,
        canvas,
    ):
        self._fps = fps
        self._canvas = canvas
        self._threshold = threshold
        self._similarity_rate_b_frame = similarity_rate_b_frame
        self._button_1 = button_1
        self._stop_frame_transfer = stop_frame_transfer

    def transmit_video(self):
        while True:
            cap = cv2.VideoCapture(0)
            _, old_frame = cap.read()
            old_fps = self._fps.rate
            with pyvirtualcam.Camera(
                width=old_frame.shape[1], height=old_frame.shape[0], fps=self._fps.rate
            ) as cam:
                my_old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2RGB)
                cam.send(my_old_frame)
                while not self._stop_frame_transfer:
                    if old_fps != self._fps.rate:
                        break
                    ret, new_frame = cap.read()
                    # cv2.imshow('Original', new_frame)
                    similarity_calculator = ImageSimilarityCalculator()
                    s = similarity_calculator.struct_similarity(old_frame, new_frame)
                    new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
                    frames_similarity = s
                    self._canvas.itemconfig(
                        self._similarity_rate_b_frame, text=str(frames_similarity)
                    )
                    if s < self._threshold.rate:
                        cam.send(new_frame)
                        cam.sleep_until_next_frame()
                    old_frame = new_frame
                    k = cv2.waitKey(30) & 0xFF
                    if k == 27:
                        frames_similarity = "None"
                        self._canvas.itemconfig(
                            self._similarity_rate_b_frame, text=str(frames_similarity)
                        )
                        stop_frame_transfer = True
                        self._button_1.config(state="NORMAL")
            cap.release()
            cv2.destroyAllWindows()
