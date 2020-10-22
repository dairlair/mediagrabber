import subprocess


url = "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"
# Wrong URL exampl
# url = "https://abcnews.go.com/Technology/video/california-judge-"

command = ["youtube-dl", url]

process = subprocess.Popen(
    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
)

(output, err) = process.communicate()

# Wait for date to terminate. Get return returncode ##
p_status = process.wait()
print("Command output : ", output)
print("Command error : ", err)
print("Command exit status/return code : ", p_status)