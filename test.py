import face_recognition
import cv2
from PIL import Image, ImageDraw
from console_progressbar import ProgressBar
from time import time_ns


# Download video for test
# youtube-dl -f "bestvideo[height<=480]+bestaudio/best[height<=480]" https://www.youtube.com/watch?v=ozqhwa9K0gk -o "./workdir/source.%(ext)s"

# Open the input movie file
# input_movie = cv2.VideoCapture("workdir/source.mp4")
input_movie = cv2.VideoCapture("workdir2/Constantine.2005.HD-DVDRip.1080p.HEVC.10bit.mkv")


length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'Frames count: {length}')

fps = int(round(input_movie.get(cv2.CAP_PROP_FPS)))  # Gets the frames per second
print(f'FPS: {fps}')

pb = ProgressBar(total=length, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')


# Initialize some variables
face_locations = []
face_encodings = []
frame_number = 0

known_face_encodings = []

def is_known(face_encoding) -> bool:
    global known_face_encodings
    results = face_recognition.compare_faces(known_face_encodings, face_encoding)
    if True in results:
        return True

    known_face_encodings.append(face_encoding)
    return False


while input_movie.isOpened():
    ret, frame = input_movie.read()

    if ret:
        pb.print_progress_bar(frame_number)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame, 1, "fog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings):
            pil_image = Image.fromarray(rgb_frame)
            draw = ImageDraw.Draw(pil_image)

            # Loop through each face found in the unknown image
            face_number = 0
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                # name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # # if True in matches:
                # #     first_match_index = matches.index(True)
                # #     name = known_face_names[first_match_index]

                # # Or instead, use the known face with the smallest distance to the new face
                # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #     name = known_face_names[best_match_index]

                # Draw a box around the face using the Pillow module
                start = time_ns()
                if is_known(face_encoding):
                    outline = (255, 0, 0)
                else:
                    outline = (0, 0, 255)
                    face = pil_image.crop(box=(left, top, right, bottom))
                    face.save(f'workdir2/faces/face-{frame_number}-{face_number}.png')
                    face_number += 1
                    draw.rectangle(((left, top), (right, bottom)), outline=outline)
                    pil_image.save(f'workdir2/frame-{frame_number}.png')
                finish = time_ns()

                print("Matching duration: " + str(finish - start) + " nanosecods")

            # if len(face_encodings):
            #     pil_image = Image.fromarray(rgb_frame)
            #     print(f"Faces found in the frame #{frame_number}")
            #     for j, face_encoding in enumerate(face_encodings):
            #         if (is_known(face_encoding)):
            #             print("This is a new face!")
            #             # cv2.imshow('Frame with faces', frame)
            #             cv2.imwrite(f'workdir/face-{frame_number}-{j}.png', frame)

        frame_number += fps * 10  # i.e. at 30 fps, this advances two secods
        frame_number = int(round(frame_number))
        input_movie.set(1, frame_number)
    else:
        input_movie.release()
        break
