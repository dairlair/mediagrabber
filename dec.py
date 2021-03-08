from decord import VideoReader, cpu
from console_progressbar import ProgressBar

vr = VideoReader('workdir2/Constantine.2005.HD-DVDRip.1080p.HEVC.10bit.mkv', ctx=cpu(0))
length = len(vr)
print('video frames:', length)

pb = ProgressBar(total=length, prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')

for pos in range(0, length, 150):
    batch = vr.next()
    pb.print_progress_bar(pos)
    vr.seek(pos)


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