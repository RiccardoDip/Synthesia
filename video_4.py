import cv2
import socket
from chainer import cuda, Variable, serializers
from net import *
import numpy as np
from PIL import Image, ImageFilter
import time
import binascii
import io

RUN_ON_GPU = False
CAMERA_ID = 0 # 0 for integrated cam, 1 for first external can ....
WIDTH=1
HEIGHT=1
PADDING = 50
MEDIAN_FILTER = 1
KEEP_COLORS = False

model = FastStyleNet()
# from 6o6o's fork. https://github.com/6o6o/chainer-fast-neuralstyle/blob/master/generate.py
def original_colors(original, stylized):
    h, s, v = original.convert('HSV').split()
    hs, ss, vs = stylized.convert('HSV').split()
    return Image.merge('HSV', (h, s, vs)).convert('RGB')

def _transform(in_image,loaded,m_path):
    if m_path == 'none':
        return in_image
    if not loaded:
        serializers.load_npz(m_path, model)
        if RUN_ON_GPU:
            cuda.get_device(0).use() #assuming only one core
            model.to_gpu()
        print ("loaded")

    xp = np if not RUN_ON_GPU else cuda.cupy
    
    image = np.asarray(in_image, dtype=np.float32).transpose(2, 0, 1)
    image = image.reshape((1,) + image.shape)
    if PADDING > 0:
        image = np.pad(image, [[0, 0], [0, 0], [PADDING, PADDING], [PADDING, PADDING]], 'symmetric')
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

if __name__ == '__main__':

    '''
    cv2.namedWindow("style")
    vc = cv2.VideoCapture(CAMERA_ID)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
    '''
    address = ("127.0.0.1", 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1000)

    print("Waiting for the client...")

    client, addr = s.accept()

    print('got connected from', addr)



    '''
    if vc.isOpened():
        rval, frame = vc.read()
        loaded = False
        mpath = 'models/edtaonisl.model'
    else:
        rval = False
    '''
    loaded = False

    mpath = 'models/edtaonisl.model'
    
    def on_change(value):
            print(value) 
            
    cv2.namedWindow('style')
    cv2.createTrackbar('slider', "style", 0, 100, on_change)

    time.sleep(2)
    

    while True:
        #cv2.imshow("style", frame)
        #rval, frame = vc.read()



        print("reading from socket")
        print("sending")
        client.send(b"go")
        strng = client.recv(32768)
        interpolation = client.recv(1024).decode("utf8")
        #print(interpolation.decode("utf8"))

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

        img = cv2.imdecode(np.frombuffer(strng, dtype=np.uint8), 1)

        img_shape = img.shape

        print(img_shape)

            

        #print(strng)

        #cv2.imshow("style", img) 
            
        #start = time.time()
        img = cv2.resize( _transform(img,loaded,mpath), (0,0), fx=1.0, fy=1.0)

        cv2.imshow("style", img)
        
            
        print("immagine mostrata")
        #print(time.time() - start, 'sec')
        
        loaded=True

        key = cv2.waitKey(1)

    
        key = cv2.waitKey(1)
        if key == 49: # 1
            mpath='models/edtaonisl.model'
            loaded=False
            print("Pressed 1")
        if key == 50: # 2
            mpath='models/natasha-russu.model'
            loaded=False
            print("Pressed 2")
        if key == 51: # 3
            mpath='models/kandinsky_e2_crop512.model'
            loaded=False
            print("Pressed 3")
        if key == 52: # 4
            mpath='models/composition.model'
            loaded=False
            print("Pressed 4")
        if key == 53: # 5
            mpath='models/scream-style.model'
            loaded=False
            print("Pressed 5")
        if key == 54: # 6
            mpath='models/candy.model'
            loaded=False
            print("Pressed 6")
        if key == 55: # 7
            mpath='models/kanagawa.model'
            loaded=False
            print("Pressed 7")
        if key == 56: # 8
            mpath='models/fur.model'
            loaded=False
            print("Pressed 8")
        if key == 57: # 9
            mpath='none'
            loaded=False
            print("Pressed 9")

        if 'c' == chr(key & 0xFF):
            KEEP_COLORS = not KEEP_COLORS
        if 'q' == chr(key & 0xFF):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break            
    cv2.destroyWindow("preview")