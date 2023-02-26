import imghdr
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np

from widget_resize import WidgetResize
from widget_grid_setting import WidgetGridSetting
from widget_export_font_lib import WidgetExportFontLib
from widget_import_font_lib import WidgetImportFontLib

class ZWidget(QWidget):
    signal = pyqtSignal(str, tuple)

    def __init__(self):
        super().__init__(None)
        self.init_menu()

        self.images = []
        self.cur_image = None
        self.cur_format = 'BGR'
        self.grid_size = 1
        self.grid_on = False
        self.grid_color = 0xff0000

        self.signal.connect(self.slot)
        self.widget_resize = WidgetResize(self.signal)
        self.widget_grid_setting = WidgetGridSetting(self.signal)
        self.widget_export_font_lib = WidgetExportFontLib(self.signal)
        self.widget_import_font_lib = WidgetImportFontLib(self.signal)

        # self.label_image = QLabel()
        # self.label_image.setScaledContents(True)

        # self.scroll_area = QScrollArea()
        # self.scroll_area.setWidget(self.label_image)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # hbox = QHBoxLayout()
        # hbox.addWidget(self.scroll_area)
        # hbox.addWidget(self.label_image)
        # self.setLayout(hbox)

        self.resize(400, 300)
        self.move(300, 50)
        self.show()

        # for debug
        # self.cur_image = QImage('/Users/cszhao/project/python/zx_image_editor/images/一键三连3.png')
        # self.cur_image = QImage('/Users/cszhao/project/python/zx_image_editor/images/red.png')
        self.cur_image = cv2.imread('/Users/cszhao/project/python/zx_image_editor/images/一键三连3.png') #[W, H, 3]
        # self.cur_image = cv2.imread('/Users/cszhao/project/python/zx_image_editor/images/test.png') #[W, H, 3]
        # self.cur_image = cv2.resize(self.cur_image, (40, 40))
        # self.cur_image = cv2.cvtColor(self.cur_image, cv2.COLOR_BGR2GRAY)
        # ret, self.cur_image = cv2.threshold(self.cur_image, 0, 255, cv2.THRESH_OTSU)
        # self.cur_format = 'BIN'
        # self.grid_size = 15
        # self.grid_on = True
        # self.cur_image = self.floyd_dteinberg_dithering()
        # self.cur_format = 'GRAY'

    def init_menu(self):
        self.menu = QMenu(self)
        action_open_img = QAction('打开图片', self.menu)
        action_resize = QAction('调整大小', self.menu)
        action_grid_setting = QAction('栅格设置', self.menu)
        action_trans2gray = QAction('灰度化', self.menu)
        action_trans2bin = QAction('二值化', self.menu)
        action_trans2bin_dither = QAction('二值化(dither)', self.menu)
        action_symmetrize_lr = QAction('左右对称', self.menu)
        action_symmetrize_ud = QAction('上下对称', self.menu)
        self.menu.addAction(action_open_img)
        self.menu.addSeparator()
        self.menu.addAction(action_resize)
        self.menu.addAction(action_grid_setting)
        self.menu.addSeparator()
        self.menu.addAction(action_trans2gray)
        self.menu.addAction(action_trans2bin)
        self.menu.addAction(action_trans2bin_dither)
        self.menu.addSeparator()
        self.menu.addAction(action_symmetrize_lr)
        self.menu.addAction(action_symmetrize_ud)
        self.menu.addSeparator()
        self.menu.addAction(QAction('导出字库', self.menu))
        self.menu.addAction(QAction('导入字库', self.menu))
        self.menu.triggered.connect(self.menu_slot)

    # def paintEvent(self, e):
    #     image = self.cur_image if self.grid_size == 1 else self.zoom_in(self.cur_image, self.grid_size)
    #     w, h = image.shape[1], image.shape[0]
    #     # painter = QPainter(self)
    #     if self.cur_format == 'BGR':
    #         qimage = QImage(image.data, w, h, w*3, QImage.Format_BGR888)
    #         self.label_image.setPixmap(QPixmap(qimage))
    #     elif self.cur_format == 'GRAY' or self.cur_format == 'BIN':
    #         qimage = QImage(image.data, w, h, w*1, QImage.Format_Grayscale8)
    #         self.label_image.setPixmap(QPixmap(qimage))
            
    def paintEvent(self, e):
        rect = e.region().rects()[0] #may contains more rect
        sx, sy, ex, ey = rect.left(), rect.top(), rect.right(), rect.bottom()

        if self.cur_image is None:
            return

        image = self.cur_image if self.grid_size == 1 else self.zoom_in(self.cur_image, self.grid_size)
        w, h = image.shape[1], image.shape[0]
        painter = QPainter(self)
        if self.cur_format == 'BGR':
            qimage = QImage(image.data, w, h, w*3, QImage.Format_BGR888)
            painter.drawImage(0, 0, qimage)
        elif self.cur_format == 'GRAY' or self.cur_format == 'BIN':
            qimage = QImage(image.data, w, h, w*1, QImage.Format_Grayscale8)
            painter.drawImage(0, 0, qimage)

        if self.grid_on and self.grid_size > 1:
            pen = QPen(QColor(self.grid_color))
            painter.setPen(pen)
            for y in range(sy, ey, self.grid_size):
                painter.drawLine(0, y, ex, y)
            for x in range(sx, ex, self.grid_size):
                painter.drawLine(x, 0, x, ey)

    def contextMenuEvent(self, e):
        self.menu.exec_(e.globalPos())

    def mousePressEvent(self, e):
        if self.cur_image is None:
            return 
        if self.grid_size <= 1:
            return
        if self.cur_format != 'BIN':
            return
        if e.buttons() != Qt.LeftButton:
            return
        x = e.pos().x() // self.grid_size
        y = e.pos().y() // self.grid_size
        if x < 0 or x >= self.cur_image.shape[1]:
            return
        if y < 0 or y >= self.cur_image.shape[0]:
            return
        # print(self.cur_image[y, x])
        self.cur_image[y, x] = 255 - self.cur_image[y, x]
        self.update()

    # def mouseMoveEvent(self, e):
    #     print('m', e)

    def menu_slot(self, action):
        if self.cur_image is None and action.text() != '打开图片' and action.text() != '导入字库':
            QMessageBox.warning(self, 'Warning', '未加载图片')
            return

        if action.text() == '打开图片':
            file_name, _ = QFileDialog.getOpenFileName(self, '打开图片', filter='Image(*.png *.jpg *.jpeg)')
            # self.cur_image = QImage(file_name)
            self.cur_image = cv2.imread(file_name)
            self.cur_format = 'BGR'
            self.grid_size = 1
            self.grid_on = False
            self.update()
        elif action.text() == '调整大小':
            self.widget_resize.zx_show(self.cur_image.shape[1], self.cur_image.shape[0])
        elif action.text() == '栅格设置':
            self.widget_grid_setting.show()
        elif action.text() == '灰度化':
            if self.cur_format != 'BGR':
                QMessageBox.warning(self, 'Warning', '只能对彩色图片进行灰度化')
                return
            self.cur_image = cv2.cvtColor(self.cur_image, cv2.COLOR_BGR2GRAY)
            self.cur_format = 'GRAY'
            self.update()
        elif action.text() == '二值化':
            if self.cur_format != 'GRAY' and self.cur_format != 'BIN':
                QMessageBox.warning(self, 'Warning', '只能对灰度图片进行二值化')
                return
            ret, self.cur_image = cv2.threshold(self.cur_image, 0, 255, cv2.THRESH_OTSU)
            self.cur_format = 'BIN'
            self.update()
        elif action.text() == '二值化(dither)':
            if self.cur_format != 'GRAY' and self.cur_format != 'BIN':
                QMessageBox.warning(self, 'Warning', '只能对灰度图片进行二值化')
                return
            self.cur_image = self.floyd_dteinberg_dithering()
            self.cur_format = 'BIN'
            self.update()
        elif action.text() == '左右对称':
            self.action_symmetrize('lr')
        elif action.text() == '上下对称':
            self.action_symmetrize('ud')
        elif action.text() == '导出字库':
            self.widget_export_font_lib.show()
        elif action.text() == '导入字库':
            self.widget_import_font_lib.show()

    def slot(self, cmd, args):
        if cmd == 'resize':
            self.cur_image = cv2.resize(self.cur_image, args)
            self.update()
        elif cmd == 'grid_setting':
            if self.cur_image.shape[0] >= 200 or self.cur_image.shape[1] >= 200:
                QMessageBox.warning(self, 'Warning', '图片过大，暂不支持，否则卡顿')
                return
            self.grid_size, self.grid_on, self.grid_color = args[0], args[1], args[2]
            self.update()
        elif cmd == 'export':
            self.export_font_lib(*args)
        elif cmd == 'import':
            self.import_font_lib(*args)

    def zoom_in(self, image, grid_size):
        w, h = image.shape[1], image.shape[0]
        shape = [int(h*grid_size), int(w*grid_size)]
        if len(image.shape) > 2:
            shape.append(image.shape[2])
        image_out = np.zeros(shape, dtype=image.dtype)
        for y in range(h):
            y2 = int(y * grid_size)
            for x in range(w):
                x2 = int(x * grid_size)
                image_out[y2:y2+grid_size, x2:x2+grid_size, ...] = image[y, x, ...]
        return image_out

    def action_symmetrize(self, arg):
        w, h = self.cur_image.shape[1], self.cur_image.shape[0]
        if arg == 'lr':
            for x in range(0, w//2):
                self.cur_image[:, w-x-1, ...] = self.cur_image[:, x, ...]
        elif arg == 'ud':
            for y in range(0, h//2):
                self.cur_image[h-y-1, :, ...] = self.cur_image[y, :, ...]
        self.update()

    def floyd_dteinberg_dithering(self):
        w, h = self.cur_image.shape[1], self.cur_image.shape[0]
        image_dither = np.zeros((h+1, w+1))
        image_dither[:h, 0:w] = self.cur_image
        threshold = 128

        for i in range(h):
            for j in range(w):
                old_pix = image_dither[i, j]
                new_pix = 255 if (image_dither[i, j] > threshold) else 0

                image_dither[i, j] = new_pix
                quant_err = old_pix - new_pix

                if j > 0:
                    image_dither[i+1, j-1] = image_dither[i+1, j-1] + quant_err * 3 / 16
                image_dither[i+1, j] = image_dither[i+1, j] + quant_err * 5 / 16
                image_dither[i, j+1] = image_dither[i, j+1] + quant_err * 7 / 16
                image_dither[i+1, j+1] = image_dither[i+1, j+1] + quant_err * 1 / 16

        image_dither = image_dither.astype(np.uint8)
        image_dither = image_dither[0:h, 0:w].copy() #call copy make it continues???, otherwise cursh
        return image_dither

    def export_font_lib(self, bits, bit_order, scan_mode, file_name, append):
        if self.cur_format != 'BIN':
            QMessageBox.warning(self, 'Warning', '目前只支持二值化图像导出')
            return
        # print(bits, bit_order, scan_mode)
        self.font = []
        if scan_mode == '列行':
            for sy in range(0, self.cur_image.shape[0], bits):
                tmp = []
                for x in range(0, self.cur_image.shape[1]):
                    data = 0x00
                    for y in range(sy, sy+bits):
                        if y >= self.cur_image.shape[0]:
                            break
                        if bit_order == '高位在前':
                            data += ((1 << (bits-(y-sy)-1)) if self.cur_image[y, x] == 0 else 0)
                        else:
                            data += ((1 << (y-sy)) if self.cur_image[y, x] == 0 else 0)
                    tmp.append(data)
                    # print('%02x' % data, end=' ')
                self.font.append(tmp)
            # print('%x' % self.font[0][0])
        else:
            QMessageBox.warning(self, 'Warning', f'not implemented for {scan_mode} yet')
            return

        fp = open(file_name, 'a' if append else 'w')
        ret = ''
        for i, line in enumerate(self.font):
            for data in line:
                if bits == 8:
                    ret += '0x%02x, ' % data
                elif bits == 8:
                    ret += '0x%04x, ' % data
                elif bits == 8:
                    ret += '0x%06x, ' % data
                elif bits == 8:
                    ret += '0x%08x, ' % data
            if i == len(self.font) - 1:
                ret = ret[:-2] #delete the last space and ,
            else:
                ret = ret[:-1] #delete the last space
                ret += '\r\n'
        ret = '{' + ret + '},\r\n\r\n'
        # print(ret)
        fp.write(ret)
        fp.close()

    def import_font_lib(self, bits, bit_order, scan_mode, file_name):
        # def ztrans(s):
        #     s = s.strip()
        #     n = int(s.strip()[2:], 16)
        #     return n

        if bits != 8 or bit_order != '高位在前' or scan_mode != '列行':
            QMessageBox(self, '警告', 'not implemented')
            return

        with open(file_name, 'r') as fp:
            lines = fp.read().splitlines()
        
        state = 0
        libs = []
        for line in lines:
            if line.startswith('{'):
                libs = [line]
                state = 1
            elif state == 1:
                libs.append(line)
                if line.endswith('},'):
                    state = 2
                    break
        if state != 2:
            QMessageBox.warning(self, '格式错误', '字库格式：\r\n//注释\r\n#注释\r\n{0x11, 0x22, 0x33, ..., 0xaa,\r\n0x22, 0x33, 0x44, ..., 0x11\r\n...\r\n0x66, 0x77, 0x88, ..., 0x66},')
            return
        libs[0] = libs[0][1:]
        libs[-1] = libs[-1][:-2]
        # print(libs)

        lines = []
        for lib in libs:
            # nums = list(map(ztrans, lib.split(',')))
            # print(nums)
            ss = lib.split(',')
            line = []
            for s in ss:
                s = s.strip()
                if s != '':
                    line.append(int(s[2:], 16))
            lines.append(line)

        print(len(lines), len(lines[0]))
        img = np.ones((len(lines) * 8, len(lines[0])), dtype=np.uint8) * 255
        for y, line in enumerate(lines):
            for x, num in enumerate(line):
                for i in range(8):
                    if num & (1 << (7 - i)):
                        img[y * bits + i, x] = 0
        self.cur_image = img
        self.cur_format = 'BIN'
        self.update()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = ZWidget()
    sys.exit(app.exec_())