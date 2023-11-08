import speedtest

class User:
    @staticmethod
    def perform_video_call(video):
        video.transmit_video()

    @staticmethod
    def check_bw():
        st = speedtest.Speedtest(secure=True)
        receive_rate = st.download()
        send_rate = st.upload()
        receive_rate = round(receive_rate / 1000000, 2)
        send_rate = round(send_rate / 1000000, 2)
        return receive_rate, send_rate

    @staticmethod
    def set_fps(canvas, fps_rate, fps):
        canvas.itemconfig(fps_rate, text=str(fps.rate))

