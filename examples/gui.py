
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from growcut import automata, growcut
from PyQt4 import QtCore, QtGui


def ndarrayToQtImage(array):
    r"""Converts a numpy array to a Qt Qimage.

    Parameters
    ----------
        array: nd-array (uint8)
            A user defined array.

    Returns
    -------
        qimage: QtImage
            A newly constructed QtImage, with a reference to the original `gray`
            nd-array.
    """

    # Map to 0-255 colorspace.
    array = np.array(
        np.interp(
            array,
            [array.min(), array.max()],
            [0, 255]
            ),
        dtype=np.uint8
        )

    h, w = array.shape

    # pad to a division of a byte boundary
    padd = np.zeros((h + (h % 2), w + (w % 2)), dtype=np.uint8)
    padd[0:h, 0:w] = array

    qimage = QtGui.QImage(padd.data, w, h,  QtGui.QImage.Format_Indexed8)
    # Attach a reference to the nd-array to the Qimage, otherwise it could be
    # garbage collected - QImage is a reference not a copy to the numpy data.
    qimage.ndarray = array

    # Update the color table, which is associated with the luminance image.
    for i in xrange(256):
        qimage.setColor(i, QtGui.QColor(i, i, i).rgb())
    return qimage


class GrowCutImageView(QtGui.QGraphicsView):

    mouseDragEvent = QtCore.pyqtSignal(int, int, name='mouseDragEvent')

    def __init__(self, parent=None):
        super(GrowCutImageView, self).__init__(parent)
        self.setMouseTracking(True)

    def wheelEvent(self, event):
        scale = math.pow(2.0, -event.delta() / 240.0)
        self.scale(scale, scale)

    def mouseMoveEvent(self, event):
        point = self.mapToScene(event.pos())
        if event.buttons() & QtCore.Qt.LeftButton:
            self.mouseDragEvent.emit(point.x(), point.y())


class GrowCutWidget(QtGui.QWidget):

    def __init__(self, image, label, strength, parent=None):
        super(GrowCutWidget, self).__init__(parent)

        self.image = image
        self.strength = strength
        self.label = label
        self.coordinates = automata.formSamples(
             self.image.shape,
             neighbours=automata.CONNECT_4
             )

        # Itterating?
        self.paused = True
        self.editLabel = 1

        self.resize(640, 480)
        self.layout = QtGui.QHBoxLayout(self)
        self.setMouseTracking(True)

        # Place a visualization of the image.
        self.imageScene = QtGui.QGraphicsScene(self)
        self.imageView = GrowCutImageView(self.imageScene)
        self.imageView.fitInView(QtCore.QRectF(0, 0, image.shape[1], image.shape[0]), QtCore.Qt.KeepAspectRatio)
        self.layout.addWidget(self.imageView)

        self.displayedImage = QtGui.QGraphicsPixmapItem()
        self.imageScene.addItem(self.displayedImage)
        self.imageView.centerOn(self.displayedImage)

        self.displayedImage.setPixmap(
            QtGui.QPixmap.fromImage(ndarrayToQtImage(image))
            )

        # Place a visualization of the label.
        self.labelScene = QtGui.QGraphicsScene(self)
        self.labelView = GrowCutImageView(self.labelScene)
        self.labelView.fitInView(QtCore.QRectF(0, 0, image.shape[1], image.shape[0]), QtCore.Qt.KeepAspectRatio)

        self.layout.addWidget(self.labelView)

        self.displayedLabel = QtGui.QGraphicsPixmapItem()
        self.labelScene.addItem(self.displayedLabel)
        self.labelView.centerOn(self.displayedLabel)

        self.displayedLabel.setPixmap(
            QtGui.QPixmap.fromImage(ndarrayToQtImage(self.label))
            )

        self.labelView.mouseDragEvent.connect(self.labelUpdate)

        # self.labelView.wheelEvent.connect(self.wheelEvent)

        # Form a timer for growcut automations
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timedUpdate)

    def labelUpdate(self, x, y):
        """
        Update the label/strength map based on user input
        """

        if (((y > 0) & (y < self.image.shape[0])) &
            ((x > 0) & (x < self.image.shape[1]))):

            self.label[y, x] = self.editLabel
            self.strength[y, x] = 1.0

    def pause(self):

        if not self.paused:
            self.timer.stop()
            self.paused = True
        else:
            self.timer.start(50)
            self.paused = False

    def editForeground(self):
        self.editLabel = 1

    def editBackground(self):
        self.editLabel = 2

    def timedUpdate(self):
        """
        slot for constant timer timeout
        """

        self.strength[:], self.label[:] = growcut.numpyAutomate(
            self.coordinates,
            self.image,
            self.strength,
            self.label
            )

        self.displayedLabel.setPixmap(
            QtGui.QPixmap.fromImage(ndarrayToQtImage(self.label * self.image))
            )


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # Glue in the grow-cut widget

        # Load an image of a particular type
        image = plt.imread('./examples/flower.png')
        lum = np.average(image, 2)

        # Form a label grid (0: no label, 1: foreground, 2: background)
        label = np.zeros_like(lum, dtype=np.int)
        label[:] = 0
        label[75:90, 100:110] = 1
        label[110:120, 150:160] = 1
        label[50:55, 160:165] = 1
        label[50:55, 180:185] = 2
        label[0:10, 0:10] = 2
        label[75:90, 0:10] = 2
        label[0:10, 200:210] = 2
        label[75:90, 200:210] = 2

        # Form a strength grid.
        strength = np.zeros_like(lum, dtype=np.float64)
        strength[label > 0] = 1.

        self.widget = GrowCutWidget(lum, label, strength)

        self.setCentralWidget(self.widget)

        self.segmentAction = QtGui.QAction(QtGui.QIcon('examples/play.png'), 'Pause', self)
        self.segmentAction.setShortcut('Ctrl+P')
        self.segmentAction.setStatusTip('Start/Stop segmentation')

        self.foregroundAction = QtGui.QAction(QtGui.QIcon('examples/pen.png'), 'Fill foreground', self)
        self.foregroundAction.setShortcut('Ctrl+F')
        self.foregroundAction.setStatusTip('Fill foreground pixels')

        self.backgroundAction = QtGui.QAction(QtGui.QIcon('examples/pen_alt.png'), 'Fill background', self)
        self.backgroundAction.setShortcut('Ctrl+F')
        self.backgroundAction.setStatusTip('Fill background pixels')

        self.segmentAction.triggered.connect(self.widget.pause)
        self.segmentAction.triggered.connect(self.toggleSegmentActionIcon)

        self.foregroundAction.triggered.connect(self.widget.editForeground)
        self.backgroundAction.triggered.connect(self.widget.editBackground)

        self.backgroundAction.setCheckable(False)

        self.statusBar()

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(self.segmentAction)
        toolbar.addSeparator()
        toolbar.addAction(self.foregroundAction)
        toolbar.addAction(self.backgroundAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('GrowCut Segmentation')
        self.show()

    def toggleSegmentActionIcon(self, event):
        if self.widget.paused:
            self.segmentAction.setIcon(QtGui.QIcon('examples/play.png'))
        else:
            self.segmentAction.setIcon(QtGui.QIcon('examples/pause.png'))

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


