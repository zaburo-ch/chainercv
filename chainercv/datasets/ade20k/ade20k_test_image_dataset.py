import glob
import os

import numpy as np

from chainer import dataset
from chainer.dataset import download
from chainercv import utils
from chainercv.utils import read_image

root = 'pfnet/chainercv/ade20k'
test_url = 'http://data.csail.mit.edu/places/ADEchallenge/release_test.zip'


def get_ade20k():
    data_root = download.get_dataset_directory(root)
    cache_fn = utils.cached_download(test_url)
    utils.extractall(cache_fn, data_root, os.path.splitext(test_url)[1])
    return data_root


class ADE20KTestImageDataset(dataset.DatasetMixin):

    """Image dataset for test split of `ADE20K`_.

    This is an image dataset of test split in ADE20K dataset distributed at
    MIT Scene Parsing Benchmark website. It has 3,352 test images.

    .. _`MIT Scene Parsing Benchmark`: http://sceneparsing.csail.mit.edu/

    Args:
        data_dir (string): Path to the dataset directory. The directory should
            contain the :obj:`release_test` dir. If :obj:`auto` is given, the
            dataset is automatically downloaded into
            :obj:`$CHAINER_DATASET_ROOT/pfnet/chainercv/ade20k`.

    """

    def __init__(self, data_dir='auto'):
        if data_dir is 'auto':
            data_dir = get_ade20k()
        img_dir = os.path.join(data_dir, 'release_test', 'testing')
        self.img_paths = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))

    def __len__(self):
        return len(self.img_paths)

    def get_example(self, i):
        """Returns the i-th example.

        Args:
            i (int): The index of the example.

        Returns:
            Returns a color image whose shape is (3, H, W). H and W are height
            and width of the image. The dtype of the image is
            :obj:`numpy.float32`.

        """
        return read_image(self.img_paths[i])
