import cv2
import socket
from chainer import cuda, Variable, serializers
from net import *
import numpy as np
from PIL import Image, ImageFilter

RUN_ON_GPU = True
CAMERA_ID = 0  # 0 for integrated cam, 1 for first external can ....
WIDTH = 1
HEIGHT = 1
PADDING = 50
MEDIAN_FILTER = 1
KEEP_COLORS = False

model = FastStyleNet()
# from 6o6o's fork. https://github.com/6o6o/chainer-fast-neuralstyle/blob/master/generate.py

path_to_presets = "real-time-style-transfer/chainer-fast-neuralstyle/models/presets/"
path_to_user_models = "real-time-style-transfer/chainer-fast-neuralstyle/models/"

m_path_dict = {
    0: f"{path_to_user_models}picasso/final_ep_picasso_6.model",
    1: f"{path_to_user_models}onde-overlay-75-25/final_ep_onde-overlay-75-25_10.model",
    2: f"{path_to_user_models}onde-overlay-50-50/final_ep_onde-overlay-50-50_10.model",
    3: f"{path_to_user_models}onde-overlay-25-75/final_ep_onde-overlay-25-75_9.model",
    4: f"{path_to_presets}kanagawa.model",
}


def original_colors(original, stylized):
    h, s, v = original.convert("HSV").split()
    hs, ss, vs = stylized.convert("HSV").split()
    return Image.merge("HSV", (h, s, vs)).convert("RGB")


def _transform(in_image, loaded, m_path):
    if m_path == "none":
        return in_image
    if not loaded:
        print(f"loading {m_path}")
        serializers.load_npz(m_path, model)
        if RUN_ON_GPU:
            cuda.get_device(0).use()  # assuming only one core
            model.to_gpu()
        loaded = True
        print("loaded")

    xp = np if not RUN_ON_GPU else cuda.cupy

    image = np.asarray(in_image, dtype=np.float32).transpose(2, 0, 1)
    image = image.reshape((1,) + image.shape)
    if PADDING > 0:
        image = np.pad(
            image, [[0, 0], [0, 0], [PADDING, PADDING], [PADDING, PADDING]], "symmetric"
        )
    image = xp.asarray(image)
    x = Variable(image)
    y = model(x)
    result = cuda.to_cpu(y.data)
    if PADDING > 0:
        result = result[:, :, PADDING:-PADDING, PADDING:-PADDING]
    result = np.uint8(result[0].transpose((1, 2, 0)))
    med = Image.fromarray(result)
    if MEDIAN_FILTER > 0:
        med = med.filter(ImageFilter.MedianFilter(MEDIAN_FILTER))
    if KEEP_COLORS:
        med = original_colors(Image.fromarray(in_image), med)

    return np.asarray(med)


def on_change(value):
    # print(value)
    return


if __name__ == "__main__":
    # SOCKET CONNECTION
    # address = ('192.168.178.103', 5000)
    address = ("127.0.0.1", 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1000)

    print("Waiting for the client...")

    client, addr = s.accept()
    connected = True

    print("got connected from", addr)

    loaded = False
    closed = False

    cv2.namedWindow("style")
    cv2.createTrackbar("slider", "style", 0, 100, on_change)

    mpath = "none"

    last_interpolation = -1

    # assert cv2.getWindowProperty('style', 0) >= 0, 'non è ancora aperto cazzo'

    while True:
        try:
            # GET IMAGE AND DECODE
            client.send(b"f")
            # print('reading from socket')
            strng = client.recv(32768)
            img = cv2.imdecode(np.frombuffer(strng, dtype=np.uint8), 1)
            # GET INTERPOLATION VALUE
            client.send(b"i")
            interpolation = client.recv(1024).decode("utf8")
            interpolation = int(round(float(interpolation)))
        except:
            # couldn't send, connection is down
            connected = False
            print("socket disconnected from server")
            break

        img = cv2.resize(_transform(img, loaded, mpath), (0, 0), fx=1.0, fy=1.0)

        cv2.imshow("style", img)
        cv2.setTrackbarPos("slider", "style", interpolation * 25)

        loaded = interpolation == last_interpolation

        if not loaded:
            mpath = m_path_dict[interpolation]

        key = cv2.waitKey(1)
        if "c" == chr(key & 0xFF):
            KEEP_COLORS = not KEEP_COLORS
        if "q" == chr(key & 0xFF):
            break

        last_interpolation = interpolation

        # close with X
        if cv2.getWindowProperty("style", cv2.WND_PROP_VISIBLE) < 1:
            closed = True
            break

    if connected:
        print("disconnecting socket from client")
        try:
            client.send(b"q")
        except:
            print("disconnected already")

    if not closed:
        cv2.destroyWindow("style")
