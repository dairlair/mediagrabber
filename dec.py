from decord import VideoReader, cpu
from console_progressbar import ProgressBar
from PIL import Image, ImageDraw
import face_recognition

workdir = 'workdir/1f9108b10e771890eeec0d0fa1a67fd2/'
vr = VideoReader(workdir + '/source.mp4', ctx=cpu(0))
length = len(vr)
fps = int(vr.get_avg_fps())
print(f'video length: {length}, FPS: {fps}')

pb = ProgressBar(total=length, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')

for pos in range(0, length, fps * 5):
    # vr.seek(pos)
    frame = vr[pos].asnumpy()
    face_locations = face_recognition.face_locations(frame, 1, "fog")
    if face_locations:
        face_encodings = face_recognition.face_encodings(frame, face_locations)

    # if face_locations:
    #     pil_image = Image.fromarray(frame)
    #     draw = ImageDraw.Draw(pil_image)
    #     # for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    #     #     draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    #     # pil_image.save(workdir + f'/frame-{pos}.png')

    pb.print_progress_bar(pos)



# frames_numbers = range(0, length, 150)
# frames = vr.get_batch(frames_numbers)

# # a file like object works as well, for in-memory decoding
# with open('workdir2/Constantine.2005.HD-DVDRip.1080p.HEVC.10bit.mkv', 'rb') as f:
#     print('opened')
#     vr = VideoReader(f, ctx=cpu(0), num_threads=1)
#     print('video frames:', len(vr))
#     # pb = ProgressBar(total=vr, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')
#     # # frames = range(0, len(vr), 150)
#     # # 1. the simplest way is to directly access frames
#     # for i in range(len(vr)):
#     #     # the video reader will handle seeking and skipping in the most efficient manner
#     #     frame = vr[i]
#     #     pb.print_progress_bar(i)
#     #     # print(frame.shape)

# # To get multiple frames at once, use get_batch
# # this is the efficient way to obtain a long list of frames
# frames = vr.get_batch([1, 3, 5, 7, 9])
# print(frames.shape)
# # (5, 240, 320, 3)
# # duplicate frame indices will be accepted and handled internally to avoid duplicate decoding
# frames2 = vr.get_batch([1, 2, 3, 2, 3, 4, 3, 4, 5]).asnumpy()
# print(frames2.shape)
# # (9, 240, 320, 3)

# # 2. you can do cv2 style reading as well
# # skip 100 frames
# vr.skip_frames(100)
# # seek to start
# vr.seek(0)
# batch = vr.next()
# print('frame shape:', batch.shape)
# print('numpy frames:', batch.asnumpy())