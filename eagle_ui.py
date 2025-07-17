import tkinter as tk
from PIL import Image, ImageTk
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
        self.title_font = ("DejaVu Sans", 48)
        self.small_font = ("DejaVu Sans", 16)

        self.title_label = tk.Label(self.root, text="System Mode", font=self.title_font, fg="black", bg="white")
        self.title_label.pack(pady=40)

        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.pack(pady=40)

        # Load and process icons with background for visibility
        def load_icon(filename):
            try:
                path = os.path.join("icons", filename)
                if os.path.exists(path):
                    img = Image.open(path).convert("RGBA").resize((160, 160))
                    background = Image.new("RGBA", img.size, (220, 220, 220, 255))
                    combined = Image.alpha_composite(background, img)
                    return ImageTk.PhotoImage(combined)
                else:
                    raise FileNotFoundError(f"File not found: {path}")
            except Exception as e:
                print(f"[Warning] Could not load {filename}: {e}")
                return None

        self.calib_icon = load_icon("calibration.png")
        self.sentry_icon = load_icon("sentry.png")
        self.update_icon = load_icon("update.png")

        def create_icon_label(parent, icon, text, command):
            frame = tk.Frame(parent, bg="white")
            btn = tk.Button(frame, image=icon, command=command, bg="white", relief="flat",
                            bd=0, highlightthickness=0, width=160, height=160)
            btn.pack()
            label = tk.Label(frame, text=text, font=self.small_font, bg="white", fg="black")
            label.pack(pady=(10, 0))
            return frame

        self.calib_widget = create_icon_label(self.button_frame, self.calib_icon, "Calibration", self.start_calibration)
        self.calib_widget.pack(side="left", padx=60)

        self.sentry_widget = create_icon_label(self.button_frame, self.sentry_icon, "Sentry", self.start_sentry)
        self.sentry_widget.pack(side="left", padx=60)

        self.update_widget = create_icon_label(self.button_frame, self.update_icon, "Update", self.update_mode)
        self.update_widget.pack(side="left", padx=60)

        self.status_label = tk.Label(self.root, text="Idle", font=self.font, fg="green", bg="white")
        self.status_label.pack(pady=50)

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
