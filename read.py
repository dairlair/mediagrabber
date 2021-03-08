import cv2
from console_progressbar import ProgressBar

cap = cv2.VideoCapture("workdir2/Constantine.2005.HD-DVDRip.1080p.HEVC.10bit.mkv")

print(cv2.version.__dict__)

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'Frames count: {length}')

fps = int(round(cap.get(cv2.CAP_PROP_FPS)))  # Gets the frames per second
print(f'FPS: {fps}')

sample_rate = int(fps * 5)

pb = ProgressBar(total=length, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')


# for fno in range(0, length, fps * 5):
#     cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
#     _, image = cap.read()
#     pb.print_progress_bar(fno)

counter = 0
success = cap.grab()  # get the next frame
while success is not None:
    if counter % sample_rate == 0:
        _, img = cap.retrieve()

    counter += 1
    pb.print_progress_bar(counter)
    success = cap.grab()
