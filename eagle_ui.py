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
        self.root.configure(bg="white")

        self.font = ("DejaVu Sans", 20)
        self.title_font = ("DejaVu Sans", 36)

        self.title_label = tk.Label(self.root, text="System Mode", font=self.title_font, fg="black", bg="white")
        self.title_label.pack(pady=30)

        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.pack(pady=20)

        def load_icon(filename):
            try:
                return PhotoImage(file=os.path.join("icons", filename))
            except Exception as e:
                print(f"[Warning] Could not load {filename}: {e}")
                return None

        self.calib_icon = load_icon("icons/calibration.png")
        self.sentry_icon = load_icon("icons/sentry.png")
        self.update_icon = load_icon("icons/update.png")

        # Helper to create buttons with or without icons
        def create_button(parent, text, command, icon):
            return tk.Button(parent, text=f" {text} ", font=self.font, command=command,
                             width=10, height=2, image=icon, compound="top", relief="flat",
                             bg="white", fg="black", bd=0, highlightthickness=0, padx=20, pady=10)

        self.calib_btn = create_button(self.button_frame, "Calibration", self.start_calibration, self.calib_icon)
        self.calib_btn.pack(side="left", padx=20)

        self.sentry_btn = create_button(self.button_frame, "Sentry", self.start_sentry, self.sentry_icon)
        self.sentry_btn.pack(side="left", padx=20)

        self.update_btn = create_button(self.button_frame, "Update", self.update_mode, self.update_icon)
        self.update_btn.pack(side="left", padx=20)

        self.status_label = tk.Label(self.root, text="Idle", font=self.font, fg="green", bg="white")
        self.status_label.pack(pady=30)

    def start_calibration(self):
        self.status_label.config(text="Calibrating...", fg="orange")
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