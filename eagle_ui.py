import tkinter as tk
from tkinter import PhotoImage
from threading import Thread
import time
import os

class JetsonGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jetson Anomaly Detector")
        self.root.geometry("1920x1080")
        self.root.configure(bg="black")

        self.font = ("DejaVu Sans", 20)
        self.title_font = ("DejaVu Sans", 36)

        self.title_label = tk.Label(self.root, text="System Mode", font=self.title_font, fg="white", bg="black")
        self.title_label.pack(pady=30)

        #Frame to hold buttons horizontally
        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.pack(pady=20)

        self.calib_icon = PhotoImage(file=os.path.join("icons", "calibration.png"))
        self.sentry_icon = PhotoImage(file=os.path.join("icons", "sentry.png"))
        self.update_icon = PhotoImage(file=os.path.join("icons", "update.png"))

        #Rounded buttons with icons
        self.calib_btn = tk.Button(self.button_frame, text=" Calibration ", font=self.font, command=self.start_calibration,
                                   width=10, height=2, image=self.calib_icon, compound="top", relief="flat",
                                   bg="#1f1f1f", fg="white", bd=0, highlightthickness=0, padx=20, pady=10)
        self.calib_btn.pack(side="left", padx=20)

        self.sentry_btn = tk.Button(self.button_frame, text=" Sentry ", font=self.font, command=self.start_sentry,
                                    width=10, height=2, image=self.sentry_icon, compound="top", relief="flat",
                                    bg="#1f1f1f", fg="white", bd=0, highlightthickness=0, padx=20, pady=10)
        self.sentry_btn.pack(side="left", padx=20)

        self.update_btn = tk.Button(self.button_frame, text=" Update ", font=self.font, command=self.update_mode,
                                    width=10, height=2, image=self.update_icon, compound="top", relief="flat",
                                    bg="#1f1f1f", fg="white", bd=0, highlightthickness=0, padx=20, pady=10)
        self.update_btn.pack(side="left", padx=20)

        self.status_label = tk.Label(self.root, text="Idle", font=self.font, fg="green", bg="black")
        self.status_label.pack(pady=30)

    def start_calibration(self):
        self.status_label.config(text="Calibrating...", fg="yellow")
        Thread(target=self.calibration_loop, daemon=True).start()

    def calibration_loop(self):
        for zone in range(9):
            print(f"[Calibration] Scanning zone {zone}...")
            time.sleep(0.5)
        print("[Calibration] Complete.")
        self.status_label.config(text="Calibration Complete", fg="green")

    def start_sentry(self):
        self.status_label.config(text="Sentry Mode Active", fg="red")
        Thread(target=self.sentry_loop, daemon=True).start()

    def sentry_loop(self):
        for _ in range(9):
            print("[Sentry] Scanning...")
            time.sleep(1)
        self.status_label.config(text="Sentry Complete", fg="green")

    def update_mode(self):
        self.status_label.config(text="Update Mode (Not Implemented)", fg="gray")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = JetsonGUI()
    app.run()
