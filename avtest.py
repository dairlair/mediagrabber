import av
from tqdm import tqdm


with av.open('/home/dairlair/Videos/Constantine.mkv') as container:
    # Signal that we only want to look at keyframes.
    stream = container.streams.video[0]
    stream.codec_context.skip_frame = 'NONKEY'

    for frame in tqdm(container.decode(stream)):
        x = frame
        # print(frame)
        # We use `frame.pts` as `frame.index` won't make must sense with the `skip_frame`.
        # frame.to_image().save('avtest/frame.{:04d}.jpg'.format(frame.pts), quality=80)
