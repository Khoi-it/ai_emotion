import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading

class AiMusicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EMOTION MUSIC")
        self.geometry("1024x600")
        self.configure(bg="#1E1E1E")  # Màu nền tối

        self.camera_on = False
        self.cap = None

        # Menu bên trái
        self.left_menu = tk.Frame(self, bg="#1E1E1E", width=180)
        self.left_menu.place(x=0, y=0, width=180, height=600)

        # Logo Zing mp3
        logo = tk.Label(self.left_menu, text="Emotion Music", font=("Arial", 16, "bold"), fg="#FFFFFF", bg="#1E1E1E")
        logo.pack(pady=20)

        # Danh sách mục menu
        menu_items = [
            ("📚 Thư Viện",),
            ("🔍 Khám Phá",),
            ("🎵 #zingchart",),
            ("📻 Radio",),
            ("🎶 BXH Nhạc Mới",),
            ("📂 Chủ Đề & Thể Loại",),
            ("⭐ Top 100",),
        ]

        for item in menu_items:
            btn = tk.Button(
                self.left_menu,
                text=item[0],
                font=("Arial", 12),
                bg="#1E1E1E",
                fg="white",
                anchor="w",
                relief="flat"
            )
            btn.pack(fill="x", padx=20, pady=5)

        # Nút đăng nhập
        login_frame = tk.Frame(self.left_menu, bg="#1E1E1E")
        login_frame.pack(fill="x", pady=20)

        login_label = tk.Label(
            login_frame,
            text="Đăng nhập để khám phá\nplaylist dành riêng cho bạn",
            font=("Arial", 10),
            bg="#1E1E1E",
            fg="white",
            justify="center"
        )
        login_label.pack(pady=5)

        login_button = tk.Button(
            login_frame,
            text="ĐĂNG NHẬP",
            font=("Arial", 10, "bold"),
            bg="#8A2BE2",
            fg="white",
            relief="flat",
            padx=20,
            pady=5
        )
        login_button.pack(pady=5)

        # Nút tạo playlist mới
        new_playlist_button = tk.Button(
            self.left_menu,
            text="+ Tạo playlist mới",
            font=("Arial", 12),
            bg="#1E1E1E",
            fg="white",
            relief="flat",
            anchor="w"
        )
        new_playlist_button.pack(fill="x", padx=20, pady=5)

        # Sidebar bên phải
        self.right_sidebar = tk.Frame(self, bg="#2C2C2C", width=300, height=500)
        self.right_sidebar.place(x=724, y=0, width=300, height=530)

        # Thanh tiêu đề của sidebar
        self.sidebar_header = tk.Frame(self.right_sidebar, bg="#2C2C2C")
        self.sidebar_header.pack(fill="x", pady=5)

        btn_playlist = tk.Button(self.sidebar_header, text="Danh sách phát", font=("Arial", 10), bg="#2C2C2C", fg="white", relief="flat")
        btn_playlist.pack(side="left", padx=10)

        btn_recent = tk.Button(self.sidebar_header, text="Nghe gần đây", font=("Arial", 10), bg="#2C2C2C", fg="white", relief="flat")
        btn_recent.pack(side="left", padx=10)

        # Camera khung hình và nút
        self.camera_section = tk.Frame(self, bg="#2C2C2C", width=544, height=530)
        self.camera_section.place(x=180, y=0, width=544, height=530)

        # Sử dụng grid layout để bố trí các widget trong camera_section
        self.camera_section.grid_rowconfigure(0, weight=1)  # Hàng đầu tiên mở rộng
        self.camera_section.grid_rowconfigure(1, weight=0)  # Hàng cho nút không mở rộng
        self.camera_section.grid_columnconfigure(0, weight=1)  # Cột mở rộng

        # Khung camera
        self.camera_frame = tk.Label(self.camera_section, bg="#2C2C2C")
        self.camera_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 50))

        # Nút bật/tắt camera
        self.toggle_camera_button = tk.Button(
            self.camera_section,
            text="Bật Camera",
            font=("Arial", 10),
            bg="#8A2BE2",
            fg="white",
            command=self.toggle_camera
        )
        self.toggle_camera_button.grid(row=1, column=0, pady=10)

        # Danh sách bài hát
        self.song_list = tk.Frame(self.right_sidebar, bg="#2C2C2C")
        self.song_list.pack(fill="both", expand=True)

        songs = [
            ("Say Yes", "Loco, Punch"),
            ("Reset", "Tiger JK"),
            ("Star (Little Prince)", "Loco, U SUNG EUN"),
            ("Be With You", "AKMU"),
            ("A Lot Like Love", "Baek A Yeon"),
            ("Can You Hear My Heart", "Epik High, LeeHi"),
            ("I Love You, I", "I.O.I")
        ]

        for song_title, artist in songs:
            song_frame = tk.Frame(self.song_list, bg="#2C2C2C")
            song_frame.pack(fill="x", padx=10, pady=5)

            cover = tk.Label(song_frame, text="🎵", font=("Arial", 14), bg="#2C2C2C", fg="white", width=3)
            cover.pack(side="left", padx=5)

            song_info = tk.Frame(song_frame, bg="#2C2C2C")
            song_info.pack(side="left", fill="both", expand=True)

            song_name = tk.Label(song_info, text=song_title, font=("Arial", 10, "bold"), bg="#2C2C2C", fg="white", anchor="w")
            song_name.pack(fill="x")

            song_artist = tk.Label(song_info, text=artist, font=("Arial", 9), bg="#2C2C2C", fg="gray", anchor="w")
            song_artist.pack(fill="x")

            add_button = tk.Button(song_frame, text="⏯", font=("Arial", 10), bg="#2C2C2C", fg="white", relief="flat")
            add_button.pack(side="right", padx=5)

        # Footer (Thanh điều khiển dưới cùng)
        self.bottom_bar = tk.Frame(self, bg="#1E1E1E", height=70)
        self.bottom_bar.place(x=0, y=530, width=1024, height=70)

        control_icons = ["🔀", "⏮", "⏯", "⏭", "🔁"]
        for icon in control_icons:
            button = tk.Button(
                self.bottom_bar,
                text=icon,
                font=("Arial", 16),
                bg="#1E1E1E",
                fg="white",
                relief="flat",
                padx=10
            )
            button.pack(side="left", padx=15)

        self.progress_frame = tk.Frame(self.bottom_bar, bg="#1E1E1E")
        self.progress_frame.pack(fill="x", pady=5)

        self.current_time = tk.Label(self.progress_frame, text="00:00", font=("Arial", 10), bg="#1E1E1E", fg="white")
        self.current_time.pack(side="left", padx=5)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate", length=400)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)
        self.progress_bar["value"] = 20

        self.total_time = tk.Label(self.progress_frame, text="03:39", font=("Arial", 10), bg="#1E1E1E", fg="white")
        self.total_time.pack(side="right", padx=5)

    def toggle_camera(self):
        if self.camera_on:
            self.camera_on = False
            self.toggle_camera_button.config(text="Bật Camera")
            if self.cap:
                self.cap.release()
                self.cap = None
            self.camera_frame.config(image="")
        else:
            self.camera_on = True
            self.cap = cv2.VideoCapture(0)
            threading.Thread(target=self.update_camera_frame, daemon=True).start()
            self.toggle_camera_button.config(text="Tắt Camera")

    def update_camera_frame(self):
        while self.camera_on and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_frame.config(image=imgtk)
                self.camera_frame.image = imgtk
            else:
                break

if __name__ == "__main__":
    app = AiMusicApp()
    app.mainloop()
