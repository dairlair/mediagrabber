import face_recognition
import cv2

# Open the input movie file
input_movie = cv2.VideoCapture("workdir/1f9108b10e771890eeec0d0fa1a67fd2/source.mp4")

length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'Frames count: {length}')

seconds = 5
fps = int(round(input_movie.get(cv2.CAP_PROP_FPS)))  # Gets the frames per second
multiplier = fps * seconds
print(f'FPS: {fps}')

# Initialize some variables
face_locations = []
face_encodings = []
frame_number = 0

while input_movie.isOpened():
    ret, frame = input_movie.read()

    if ret:
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings):
            # cv2.imshow('Frame with faces', frame)
            cv2.imwrite(f'workdir/face-{frame_number}.png', frame)
            print(f"Faces found in the frame #{frame_number}")

        frame_number += fps * 2  # i.e. at 30 fps, this advances one second
        frame_number = int(round(frame_number))
        input_movie.set(1, frame_number)
    else:
        input_movie.release()
        break
