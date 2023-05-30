import cv2, Queue, threading, time
from GrabParams import grabParams

class FastVideoCapture(object):

    def __init__(self, num):
      print("FastVideoCapture __init__:")
      self.done = False
      self.cap = cv2.VideoCapture(num)
      self.q = Queue.Queue()
      self.t = threading.Thread(target=self._reader)
      self.t.daemon = True
      self.t.start()
      self.__init_flag = True
      

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
      while not self.done:
        ret, frame = self.cap.read()
        if not ret:
          break
        if not self.q.empty():
          try:
            self.q.get_nowait()   # discard previous (unprocessed) frame
          except Queue.Empty:
            pass
        self.q.put(frame)

    def read(self):
      return self.q.get()

    def getHeight(self):
      return self.cap.get(4)

    def getWidth(self):
      return self.cap.get(3)

    def close(self):
      self.done = True


# fastVideoCapture = FastVideoCapture(grabParams.cap_num)

