
from image_backend.image_processing_main import VideoReader
from image_analysis.image_analysis_main import ImageAnalysisMain

import config
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2, sys
import numpy as np
import threading
import _thread

class DivingVisualTracker:
    def __init__(self):
        self.id = 0
        self.videoReading = VideoReader("")
        self.videoAnalysis = ImageAnalysisMain()
        self.frames = None
        self.currentframe = None
        self.current_frame_index = 0  # Replace this with the appropriate initialization


        self.currentPicture = None
        #@TODO Make GUI

    def start_shape_detetion(self, first_frame: np.array) -> None:
        self.id = 1
        self.videoAnalysis.read_frame(first_frame)
        if 0 == self.videoAnalysis.start_RGB_shape_detection(False, [], 5, 5, 3):
            self.frames = self.videoAnalysis.frames_processed
            return True
        else:
            return False

         
    
    def __str__(self) -> str:
        
        pass
    
    def process_video(self, path: str) -> list:
        print("Loading... Processing Video File...")
        self.frames = self.videoReading.read_all_video_frames_source
        self.frameCounter = 0
        print("Done")
        return self.frames
    
    def process_picture(self, path: str):
        i = self.videoReading.get_picture__feed_source(path)
        self.currentframe = i
        self.currentPicture = i
        return i
    
    def get_previous_frame(self):
        # Replace this with your actual logic to get the previous frame
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            return self.frames[self.current_frame_index]
        else:
            return None

    def get_next_frame(self):
        # Replace this with your actual logic to get the next frame
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            return self.frames[self.current_frame_index]
        else:
            return None

    def __del__(self):
        print("Destoryed visual tracker")

    

class SportsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.divingBackend = DivingVisualTracker()

        self.initUI()

    def initUI(self):
        # Create a tab widget
        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.createTab1(), "Image Processing")  # Renamed the tab
        tab_widget.addTab(self.createTab2(), "Graph Tab")

        # Set up the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # Set the background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_color = QColor(Qt.cyan).lighter(150)  # Mild opaque industrial cyan blue
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        # Set up the main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Sports Visualization App')
        self.show()

    def createTab1(self):
        widget = QWidget()

        self.button_open_file = QPushButton('Open File', self)
        self.textbox_file_path = QLineEdit(self)
        self.label_image = QLabel(self)
        self.button_process_image = QPushButton('Process Image', self)
        self.button_back = QPushButton('Back', self)
        self.button_forward = QPushButton('Forward', self)

        # Connect button click events to functions
        self.button_open_file.clicked.connect(self.openFile)
        self.button_process_image.clicked.connect(self.processImage)
        self.button_back.clicked.connect(self.showPreviousFrame)
        self.button_forward.clicked.connect(self.showNextFrame)

        # Initially hide the buttons
        self.button_process_image.hide()
        self.button_back.hide()
        self.button_forward.hide()

        # Set up the layout for the first tab
        layout_tab1 = QVBoxLayout(widget)
        layout_tab1.addWidget(self.button_open_file)
        layout_tab1.addWidget(self.textbox_file_path)
        layout_tab1.addWidget(self.label_image)  # Placeholder for loaded image
        layout_tab1.addWidget(self.button_process_image)
        layout_tab1.addLayout(self.createNavigationLayout())
        layout_tab1.addStretch(1)

        return widget

    def createTab2(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # Add your graph-related widgets or components here
        # For example, you might use Matplotlib or another plotting library
        layout.addWidget(QLabel("Graph Tab Content"))
        layout.addStretch(1)
        return widget

    def createNavigationLayout(self):
        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.button_back)
        navigation_layout.addWidget(self.button_forward)
        return navigation_layout

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video or Image File", "", "All Files (*)", options=options)

        if file_path:
            # Display the file path in the text box
            self.textbox_file_path.setText(file_path)

            # Check if the file is an image and display it
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.divingBackend.process_picture(file_path)
                self.showImage(self.divingBackend.currentPicture)

                # Show the buttons after an image is loaded
                self.button_process_image.show()
                self.button_back.show()
                self.button_forward.show()
            else:
                self.label_image.clear()
                # Hide the buttons if no image is loaded
                self.button_process_image.hide()
                self.button_back.hide()
                self.button_forward.hide()

    def processImage(self):
        # Replace this with your actual logic to process the image
        # Update self.divingBackend.currentPicture with the processed image
        self.divingBackend.start_shape_detetion(self.divingBackend.currentframe)
        self.updateNavigationButtons()
        pass

    def showImage(self, image_data):
        # Load and display an image in the QLabel
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_BGR888)

        # Convert the QImage to a QPixmap and display it in the QLabel
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaledToWidth(400)  # Adjust the width as needed
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignCenter)

    def showPreviousFrame(self):
        previous_frame = self.divingBackend.get_previous_frame()
        if previous_frame is not None:
            self.showImage(previous_frame)

        # Update the button label and state
        self.updateNavigationButtons()

    def showNextFrame(self):
        next_frame = self.divingBackend.get_next_frame()
        if next_frame is not None:
            self.showImage(next_frame)

        # Update the button label and state
        self.updateNavigationButtons()

    def updateNavigationButtons(self):
        # Update the button labels with the number of available frames
        self.button_back.setText(f'Back ({self.divingBackend.current_frame_index} frames)')
        self.button_forward.setText(f'Forward ({len(self.divingBackend.frames) - 1 - self.divingBackend.current_frame_index} frames)')

        # Enable or disable the buttons based on the availability of frames
        self.button_back.setEnabled(self.divingBackend.current_frame_index > 0)
        self.button_forward.setEnabled(self.divingBackend.current_frame_index < len(self.divingBackend.frames) - 1)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SportsApp()
    sys.exit(app.exec_())