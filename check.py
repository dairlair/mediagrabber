# from mediagrabber.downloader.youtubedl import YoutubedlVideoDownloader
import subprocess
import sys

url = "https://video.aktualne.cz/dvtv/prouza-tisice-firem-jsou-v-ohrozeni-kompenzace-stacit-nebudo/r~9536aaca13be11ebb408ac1f6b220ee8/"

# downloader = YoutubedlVideoDownloader()
# response = downloader.download("./workdir", url)
# print('Video downloaded successfully')
# print(response.__dict__)


def subcall_stream(cmd: list):
    # Run a shell command, streaming output to STDOUT in real time
    # Expects a list style command, e.g. `["docker", "pull", "ubuntu"]`
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    )

    output: str = ''
    for line in p.stdout:
        print("Line:")
        output += line
        sys.stdout.write(line)

    p.wait()
    return (p.returncode, output)


command = [
    "youtube-dl",
    "-f",
    "bestvideo[height<=480]+bestaudio/best[height<=480]",
    url,
]

code = subcall_stream(command)
print('Result:')
print(code)
