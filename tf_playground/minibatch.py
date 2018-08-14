import tensorflow as tf
import itertools
import tables
import matplotlib.pyplot as plt

DEFAULT_FILE = '/home/qinglong/node3share/analytical_phantom_sinogram.h5'
file = tables.open_file(DEFAULT_FILE)

# TODO replace with parser

class gen:
    """
    g = gen(file)

    with tf.Session() as sess:
        sess.run(g.next_sino_batch)
    """
    def __init__(self, file, batch_size=32):
        self.file = file
        self.next_sino = (tf.data.Dataset
                         .from_generator(self._sino_gen, tf.float32, tf.TensorShape([320,320]))
                         .make_one_shot_iterator()
                         .get_next())

        self.next_img = (tf.data.Dataset
                        .from_generator(self._img_gen, tf.float32, tf.TensorShape([256,256]))
                        .make_one_shot_iterator()
                        .get_next())

        self.next_sino_batch = (tf.data.Dataset
                              .from_generator(self._sino_gen, tf.float32, tf.TensorShape([320,320]))
                              .batch(batch_size)
                              .make_one_shot_iterator()
                              .get_next())

        self.next_img_batch = (tf.data.Dataset
                             .from_generator(self._img_gen, tf.float32, tf.TensorShape([256,256]))
                             .batch(batch_size)
                             .make_one_shot_iterator()
                             .get_next())

    def _sino_gen(self):
        for i in itertools.count(1):
            # TODO uncoupling path
            yield self.file.root.data[i][2]

    def _img_gen(self):
        for i in itertools.count(1):
            yield self.file.root.data[i][0]