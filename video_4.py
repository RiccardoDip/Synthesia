import cv2
import socket
from chainer import cuda, Variable, serializers
from net import *
import numpy as np
from PIL import Image, ImageFilter
import time
import binascii
import io

RUN_ON_GPU = True
CAMERA_ID = 0  # 0 for integrated cam, 1 for first external can ....
WIDTH = 1
HEIGHT = 1
PADDING = 50
MEDIAN_FILTER = 1
KEEP_COLORS = False

model = FastStyleNet()
# from 6o6o's fork. https://github.com/6o6o/chainer-fast-neuralstyle/blob/master/generate.py


def original_colors(original, stylized):
    h, s, v = original.convert('HSV').split()
    hs, ss, vs = stylized.convert('HSV').split()
    return Image.merge('HSV', (h, s, vs)).convert('RGB')


def _transform(in_image, loaded, m_path):
    if m_path == 'none':
        return in_image
    if not loaded:
        print(f'loading {m_path}')
        serializers.load_npz(m_path, model)
        if RUN_ON_GPU:
            cuda.get_device(0).use()  # assuming only one core
            model.to_gpu()
        print('loaded')

    xp = np if not RUN_ON_GPU else cuda.cupy

    image = np.asarray(in_image, dtype=np.float32).transpose(2, 0, 1)
    image = image.reshape((1,) + image.shape)
    if PADDING > 0:
        image = np.pad(image, [[0, 0], [0, 0], [PADDING, PADDING], [
                       PADDING, PADDING]], 'symmetric')
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
    print(value)


if __name__ == '__main__':
    path_to_presets = '/home/dargendanico/Scrivania/real-time-style-transfer/chainer-fast-neuralstyle/models/presets/'
    path_to_user_models = '/home/dargendanico/Scrivania/real-time-style-transfer/chainer-fast-neuralstyle/models/'

    address = ('127.0.0.1', 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1000)

    print('Waiting for the client...')

    client, addr = s.accept()

    print('got connected from', addr)

    loaded = False
    closed = False

    cv2.namedWindow('style')
    cv2.createTrackbar('slider', 'style', 0, 8, on_change)

    mpath = 'none'

    while True:

        try:
            # print('sending')
            client.send(b'f')
            # print('reading from socket')
            strng = client.recv(32768)
            client.send(b'i')
            interpolation = client.recv(1024).decode('utf8')
            print(interpolation)
        except:
            # recreate the socket and reconnect
            print("socket disconnected from server")
            break

        '''
        # Open plaintext file with hex
        #picture_hex = open(strng).read()

        # Convert hex to binary data
        #picture_bytes = binascii.unhexlify(picture_hex)

        # Convert bytes to stream (file-like object in memory)
        picture_stream = io.BytesIO(strng)

        # Create Image object
        picture = Image.open(picture_stream)

        #display image
        picture.show()

        # print whether JPEG, PNG, etc.
        print(picture.format)
        '''

        print('undecoded')
        img = cv2.imdecode(np.frombuffer(strng, dtype=np.uint8), 1)

        img_shape = img.shape

        print(img_shape)

        # print(strng)

        # cv2.imshow('style', img)

        # start = time.time()
        img = cv2.resize(_transform(img, loaded, mpath),
                         (0, 0), fx=1.0, fy=1.0)

        cv2.imshow('style', img)

        # print('immagine mostrata')
        # print(time.time() - start, 'sec')

        loaded = True

        key = cv2.waitKey(1)
        if interpolation == '0.0':
            mpath = f'{path_to_presets}starrynight.model'
            loaded = False
        if interpolation == '1.0':
            mpath = f'{path_to_presets}picasso.model'
            loaded = False
        if interpolation == '2.0':
            mpath = f'{path_to_presets}kandinsky_e2_crop512.model'
            loaded = False
        if interpolation == '3.0':
            mpath = f'{path_to_presets}composition.model'
            loaded = False
        if interpolation == '4.0':
            mpath = f'{path_to_presets}scream-style.model'
            loaded = False
        if interpolation == '5.0':
            mpath = f'{path_to_presets}candy.model'
            loaded = False
        if interpolation == '6.0':
            mpath = f'{path_to_presets}kanagawa.model'
            loaded = False
        if interpolation == '7.0':
            mpath = f'{path_to_presets}fur.model'
            loaded = False
        if interpolation == '8.0':
            mpath = 'none'
            loaded = False

        if 'c' == chr(key & 0xFF):
            KEEP_COLORS = not KEEP_COLORS
        if 'q' == chr(key & 0xFF):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        # close with X
        if cv2.getWindowProperty('style', cv2.WND_PROP_VISIBLE) < 1:
            closed = True
            break

    print("disconnecting socket from client")
    # TODO

    if not closed:
        cv2.destroyWindow('style')