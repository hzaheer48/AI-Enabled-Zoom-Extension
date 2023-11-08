from tkinter import *
from tkinter.ttk import Combobox
from pathlib import Path
from threading import Thread
import datetime
import webbrowser
from tkinter import messagebox as mb
from classes.NetworkPredictor import NetworkPredictor
from classes.Bandwidth import Bandwidth
from classes.Threshold import Threshold
from classes.FPS import FPS
from classes.Video import Video
from classes.User import User
from functools import partial

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def combo_box_changed(fps, combo_box, fps_rate, canvas, event):
    selected_value = combo_box.get()
    fps.rate = int(selected_value)
    User.set_fps(canvas,fps_rate,fps)


def toggle_combo_box(
    threshold, fps, auto_var, combo_box, similarity_rate, fps_rate, canvas
):
    if auto_var.get() == 1:
        combo_box.config(state=DISABLED)
        threshold.rate = 1
        canvas.itemconfig(similarity_rate, text=str(threshold.rate))
        fps.rate = 30
        canvas.itemconfig(fps_rate, text=str(fps.rate))
    else:
        threshold.rate = 0.95
        canvas.itemconfig(similarity_rate, text=str(threshold.rate))
        combo_box.config(state=NORMAL)
        combo_box_changed(fps, combo_box, fps_rate, canvas, None)


def check_network_conditions(
    threshold,
    download_rate_item,
    upload_rate_item,
    timestamp,
    button_2,
    similarity_rate,
    canvas,
):
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    current_time = str(current_time)
    canvas.itemconfig(timestamp, text=current_time)
    canvas.itemconfig(download_rate_item, text="Checking")
    canvas.itemconfig(upload_rate_item, text="Checking")
    recieve_rate, send_rate = User.check_bw()
    canvas.itemconfig(download_rate_item, text=str(recieve_rate) + "Mbps")
    canvas.itemconfig(upload_rate_item, text=str(send_rate) + "Mbps")
    button_2.config(state=NORMAL)
    predictor = NetworkPredictor()
    current_bw = recieve_rate + send_rate
    future_bw = predictor.predict_network_traffic()
    future_bw = round(future_bw, 2)
    print(future_bw)
    bandwidth = Bandwidth(current_bw, future_bw)
    if bandwidth.current_bw < bandwidth.future_bw:
        threshold.rate = 0.825
        message = f"Network Condition Warning\nNetwork condition is poor.\nCurrent Bandwidth: {bandwidth.current_bw} Mbps\nPredicted Bandwidth: {bandwidth.future_bw} Mbps"
        mb.showwarning("Network Condition Warning", message)
    else:
        threshold.rate = 0.95
    canvas.itemconfig(similarity_rate, text=str(threshold.rate))


def frames_transfering(
    threshold,
    fps,
    stop_frame_transfer,
    similarity_rate_b_frame,
    button_1,
    input,
    canvas,
):
    webbrowser.open(input.get())
    video = Video(
        threshold,
        fps,
        stop_frame_transfer,
        similarity_rate_b_frame,
        button_1,
        canvas,
    )
    User.perform_video_call(video)


def handle_button_1_click(
    threshold,
    fps,
    stop_frame_transfer,
    frames_similarity,
    similarity_rate_b_frame,
    button_1,
    input,
    canvas,
):
    button_1.config(state=DISABLED)
    stop_frame_transfer = False
    frame_transfer_thread = Thread(
        target=frames_transfering,
        args=(
            threshold,
            fps,
            stop_frame_transfer,
            similarity_rate_b_frame,
            button_1,
            input,
            canvas,
        ),
    )
    frame_transfer_thread.start()


def handle_button_2_click(
    threshold,
    download_rate_item,
    upload_rate_item,
    timestamp,
    button_2,
    similarity_rate,
    canvas,
):
    button_2.config(state=DISABLED)
    network_thread = Thread(
        target=check_network_conditions,
        args=(
            threshold,
            download_rate_item,
            upload_rate_item,
            timestamp,
            button_2,
            similarity_rate,
            canvas,
        ),
    )
    network_thread.start()




def create_gui(threshold, fps):
    (
        download_rate_item,
        upload_rate_item,
        canvas,
        timestamp,
        button_1,
        button_2,
        similarity_rate,
        frames_similarity,
        similarity_rate_b_frame,
        fps_rate,
        combo_box,
        auto_var,
        stop_frame_transfer,
        input,
    ) = [None] * 14
    window = Tk()
    window.geometry("1150x494")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=494,
        width=1150,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )

    canvas.place(x=0, y=0)

    canvas.create_rectangle(18.0, 24.0, 611.0, 250.0, fill="#06285B", outline="")

    canvas.create_rectangle(18.0, 255.0, 611.0, 448.0, fill="#06285B", outline="")

    canvas.create_text(
        104.0,
        144.0,
        anchor="nw",
        text="Select FPS:",
        fill="#FBFBFB",
        font=("Inter Bold", 12 * -1),
    )
    input = Entry(
        canvas,
        font=("Inter Bold", 12 * -1),
    )
    input.insert(0, "Enter zoom meeting link")
    input.place(x=104.0, y=200.0, width=300, height=24)

    combo_values = ["30", "25", "20", "15", "10", "5", "1"]
    combo_box = Combobox(canvas, values=combo_values)
    combo_box.set("30")
    combo_box.place(x=194.0, y=144.0, width=70)

    auto_var = IntVar()
    check_button = Checkbutton(
        canvas,
        text="Auto",
        variable=auto_var,
        onvalue=1,
        offvalue=0,
        font=("Inter Bold", 12 * -1),
    )
    check_button.place(x=321.0, y=144.0, anchor="nw")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
    )
    button_1.place(x=398.0, y=138.0, width=161.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
    )
    button_2.place(x=398.0, y=333.0, width=161.0, height=37.0)

    canvas.create_rectangle(96.0, 285.0, 364.0, 419.0, fill="#FAFAFA", outline="")

    canvas.create_rectangle(95.0, 320.0, 364.0, 322.0, fill="#000000", outline="")

    canvas.create_rectangle(95.0, 350.5, 364.0, 351.5, fill="#000000", outline="")

    canvas.create_rectangle(95.0, 375.0, 364.0, 376.0, fill="#000000", outline="")

    canvas.create_rectangle(227.0, 351.0, 229.0, 419.0, fill="#000000", outline="")

    canvas.create_text(
        170.0,
        293.0,
        anchor="nw",
        text="Internet Connection",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    timestamp = canvas.create_text(
        170.0,
        325.0,
        anchor="nw",
        text="Time Stamp",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    canvas.create_text(
        106.0,
        355.0,
        anchor="nw",
        text="Download",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    download_rate_item = canvas.create_text(
        104.0,
        386.0,
        anchor="nw",
        text="None",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    upload_rate_item = canvas.create_text(
        239.0,
        386.0,
        anchor="nw",
        text="None",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    canvas.create_text(
        236.0,
        355.0,
        anchor="nw",
        text="Upload",
        fill="#126DF4",
        font=("Inter Bold", 12 * -1),
    )

    canvas.create_text(
        147.0,
        39.0,
        anchor="nw",
        text="Similarity between frames:",
        fill="#F6F6F6",
        font=("Inter Bold", 12 * -1),
    )

    canvas.create_text(
        147.0,
        78.0,
        anchor="nw",
        text="FPS",
        fill="#FDFDFD",
        font=("Inter Bold", 12 * -1),
    )

    fps_rate = canvas.create_text(
        186.0,
        78.0,
        anchor="nw",
        text=str(fps.rate),
        fill="#FAFAFA",
        font=("Inter", 12 * -1),
    )

    similarity_rate = canvas.create_text(
        244.0,
        59.0,
        anchor="nw",
        text=str(threshold.rate),
        fill="#FFFFFF",
        font=("Inter", 12 * -1),
    )

    similarity_rate_b_frame = canvas.create_text(
        314.0,
        39.0,
        anchor="nw",
        text=str(frames_similarity),
        fill="#FFFFFF",
        font=("Inter", 12 * -1),
    )

    canvas.create_text(
        147.0,
        59.0,
        anchor="nw",
        text="Similarity Rate:",
        fill="#FFFDFD",
        font=("Inter Bold", 12 * -1),
    )

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(889.0, 247.0, image=image_image_1)

    combo_box.bind(
        "<<ComboboxSelected>>",
        partial(combo_box_changed, fps, combo_box, fps_rate, canvas),
    )
    check_button.config(
        command=partial(
            toggle_combo_box,
            threshold,
            fps,
            auto_var,
            combo_box,
            similarity_rate,
            fps_rate,
            canvas,
        ),
    )

    button_1.config(
        command=partial(
            handle_button_1_click,
            threshold,
            fps,
            stop_frame_transfer,
            frames_similarity,
            similarity_rate_b_frame,
            button_1,
            input,
            canvas,
        )
    )
    button_2.config(
        command=partial(
            handle_button_2_click,
            threshold,
            download_rate_item,
            upload_rate_item,
            timestamp,
            button_2,
            similarity_rate,
            canvas,
        )
    )
    window.resizable(False, False)
    window.mainloop()


def run_gui_in_thread(threshold, fps):
    gui_thread = Thread(
        target=create_gui,
        args=(
            threshold,
            fps,
        ),
    )
    gui_thread.start()


if __name__ == "__main__":
    threshold = Threshold(1)
    fps = FPS(30)
    run_gui_in_thread(threshold, fps)
