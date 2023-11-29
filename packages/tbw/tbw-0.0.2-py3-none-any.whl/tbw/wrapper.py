from torch.utils.tensorboard import SummaryWriter
from tbw.functionals import checkdir
from enum import Enum

class TBType(Enum):
    r"""The data type of the writer"""

    SCALAR = 'scalar'
    r"""Scalar data type"""

    SCALARS = 'scalars'
    r"""Scalars data type, provided as a dictionary"""

    IMAGE = 'image'
    r"""Image data type, provided as a tensor"""

    VIDEO = 'video'
    r"""Video data type"""

    FIGURE = 'figure'
    r"""Figure data type"""

    TEXT = 'text'
    r"""Text data type"""

    HISTOGRAM = 'histogram'
    r"""Histogram data type"""

    EMBEDDING = 'embedding'
    r"""Embedding data type"""

    @staticmethod
    def from_str(data_type: str) -> 'TBType':
        r"""
        This method returns a :py:class:`TBType` object given a valid type string.

        :param str data_type: The type of the data to be logged. Supported values: ``scalar``,
            ``scalars``, ``image``, ``video``, ``figure``, ``text``, ``histogram``,
            and ``embedding`` (case insensitive).

        :returns TBType: :py:class:`TBType` corresponds to the data type
            string.
        
        :raises ValueError: Raises an error if the string is invalid.
        """

        match data_type.lower():
            case 'scalar': return TBType.SCALAR
            case 'scalars': return TBType.SCALARS
            case 'image': return TBType.IMAGE
            case 'video': return TBType.VIDEO
            case 'figure': return TBType.FIGURE
            case 'text': return TBType.TEXT
            case 'histogram': return TBType.HISTOGRAM
            case 'embedding': return TBType.EMBEDDING
            case _: raise ValueError("Invalid data type specified.")


class TBWriter(object):
    r"""
    A class that creates a tensorboard writer for a single data stream (e.g., scalar).

    :param SummaryWriter writer: A tensorboard writer
    :param TBType data_type: The data type to be logged from :py:class:`TBType`
    :param str tag: The tag for tensorboard logging
    """

    def __init__(self, writer, data_type, tag):

        self.step = 0
        self.writer = writer
        self.type = data_type
        self.tag = tag

    def __call__(self, data, step = None, flush = False, metadata=None, label_img=None, fps=4.0):
        r"""
        The call function of the writer.

        :param torch.Tensor data: The data to be logged.
        :param int step: The step value to override the default counter.
        :param bool flush: Flushes the logging after writing it.
        :param list metadata: metadata for the embedding writer.
        :param list label_img: labels for the embedding writer.
        :param float fps: fps for the video writer.
        """

        counter = self.step if step ==None else step

        match self.type:
            case TBType.SCALAR: 
                self.writer.add_scalar(self.tag, data, global_step = counter)

            case TBType.SCALARS: 
                self.writer.add_scalars(self.tag, data, global_step = counter)

            case TBType.IMAGE: 
                self.writer.add_image(self.tag, data, global_step = counter)

            case TBType.VIDEO: 
                self.writer.add_video(self.tag, data, global_step = counter, fps = fps)

            case TBType.FIGURE: 
                self.writer.add_figure(self.tag, data, global_step = counter)

            case TBType.TEXT: 
                self.writer.add_text(self.tag, data, global_step = counter)

            case TBType.HISTOGRAM: 
                self.writer.add_histogram(self.tag, data, global_step = counter)

            case TBType.EMBEDDING: 
                self.writer.add_embedding(mat=data, metadata=metadata, label_img=label_img, global_step=counter, tag=self.tag)

            case _: 
                raise ValueError("Invalid data type specified.")


        self.step += 1
        if flush: self.flush()

    def flush(self):
        self.writer.flush()


class TBWrapper(object):
    r"""
    The main wrapper class that initializes the SummaryWriter and creates as many writers as needed.

    :param str path: Path to save the logging files
    """

    def __init__(self, path):
        checkdir(path)
        self.writer = SummaryWriter(path)
        self.writers = {}

    def __call__(self, data_type, tag):
        r"""
        The call function creates a :py:meth:`TBWriter` and returns it

        :param TBType data_type: The type of data for logging
        :param str tag: The tag for the data stream
        """
        type_enum = data_type if isinstance(data_type, TBType) else TBType.from_str(data_type)
        writer = TBWriter(self.writer, type_enum, tag)
        self.writers[tag] = writer
        return writer

    def __len__(self):
        return len(self.writers)

    def __bool__(self):
        return len(self)>0

    def __getitem__(self, tag):
        assert (tag in self.writers), "The requested writer does not exist"
        return self.writers[tag]

    def __del__(self):
        self.writers = {}
        self.writer.close()


