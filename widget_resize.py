from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WidgetResize(QWidget):
    def __init__(self, signal):
        super().__init__()

        self.signal = signal
        self.ratio = 1
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        int_validator = QIntValidator()
        int_validator.setRange(1, 1024)
        
        self.le_width = QLineEdit('40')
        self.le_width.setValidator(int_validator)
        self.le_width.textEdited.connect(lambda: self.text_edited('w'))
        hbox_width = QHBoxLayout()
        hbox_width.addWidget(QLabel('目标宽度'))
        hbox_width.addWidget(self.le_width)

        self.le_height = QLineEdit('40')
        self.le_height.setValidator(int_validator)
        self.le_height.textEdited.connect(lambda: self.text_edited('h'))
        hbox_height = QHBoxLayout()
        hbox_height.addWidget(QLabel('目标高度'))
        hbox_height.addWidget(self.le_height)

        self.cb_keep_ratio = QCheckBox()
        self.cb_keep_ratio.setChecked(False)
        self.cb_keep_ratio.stateChanged.connect(self.state_changed)
        hbox_keep_ratio = QHBoxLayout()
        hbox_keep_ratio.addWidget(QLabel('保持比例'))
        hbox_keep_ratio.addWidget(self.cb_keep_ratio)
        hbox_keep_ratio.addStretch()

        btn_ok = QPushButton('确定')
        btn_ok.clicked.connect(lambda: self.btn_clicked('ok'))
        btn_cancel = QPushButton('取消')
        btn_cancel.clicked.connect(lambda: self.btn_clicked('cancel'))
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_ok)
        hbox_btn.addWidget(btn_cancel)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_width)
        vbox.addLayout(hbox_height)
        vbox.addLayout(hbox_keep_ratio)
        vbox.addLayout(hbox_btn)

        self.setLayout(vbox)
        self.resize(200, 100)

    def zx_show(self, w, h):
        self.le_width.setText(f'{w}')
        self.le_height.setText(f'{h}')
        self.ratio = w / h
        self.show()

    def btn_clicked(self, arg):
        if arg == 'ok':
            width = int(self.le_width.text())
            height = int(self.le_height.text())
            self.signal.emit('resize', (width, height))
        self.hide()

    # def text_changed(self, arg):

    def text_edited(self, arg):
        if not self.cb_keep_ratio.isChecked():
            return
        if arg == 'w':
            try:
                new_width = int(self.le_width.text())
            except Exception as e:
                new_width = 0
            new_height = int(new_width / self.ratio + 0.5)
            self.le_height.setText(f'{new_height}')
        elif arg == 'h':
            try:
                new_height = int(self.le_height.text())
            except Exception as e:
                new_height = 0
            new_width = int(new_height * self.ratio + 0.5)
            self.le_width.setText(f'{new_width}')

    def state_changed(self):
        if not self.cb_keep_ratio.isChecked():
            return
        try:
            new_width = int(self.le_width.text())
        except Exception as e:
            new_width = 0
        new_height = int(new_width / self.ratio + 0.5)
        self.le_height.setText(f'{new_height}')

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = WidgetResize(None)
    widget.show()
    sys.exit(app.exec_())