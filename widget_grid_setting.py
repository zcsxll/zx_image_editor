from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WidgetGridSetting(QWidget):
    def __init__(self, signal):
        super().__init__()

        self.signal = signal
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.le_grid_size = QLineEdit('1')
        self.le_grid_size.setFixedWidth(40)
        hbox_grid_size = QHBoxLayout()
        hbox_grid_size.addWidget(QLabel('栅格尺寸'))
        hbox_grid_size.addWidget(self.le_grid_size)
        hbox_grid_size.addStretch()

        self.cb_on = QCheckBox()
        self.cb_on.setChecked(False)
        hbox_grid_on = QHBoxLayout()
        hbox_grid_on.addWidget(QLabel('显示栅格'))
        hbox_grid_on.addWidget(self.cb_on)
        hbox_grid_on.addStretch()

        self.le_r = QLineEdit('255')
        self.le_g = QLineEdit('0')
        self.le_b = QLineEdit('0')
        self.le_r.setFixedWidth(40)
        self.le_g.setFixedWidth(40)
        self.le_b.setFixedWidth(40)
        hbox_grid_color = QHBoxLayout()
        hbox_grid_color.addWidget(QLabel('栅格颜色'))
        hbox_grid_color.addWidget(QLabel('R'))
        hbox_grid_color.addWidget(self.le_r)
        hbox_grid_color.addWidget(QLabel('G'))
        hbox_grid_color.addWidget(self.le_g)
        hbox_grid_color.addWidget(QLabel('B'))
        hbox_grid_color.addWidget(self.le_b)
        hbox_grid_color.addStretch()

        btn_ok = QPushButton('确定')
        btn_ok.clicked.connect(lambda: self.btn_clicked('ok'))
        btn_cancel = QPushButton('取消')
        btn_cancel.clicked.connect(lambda: self.btn_clicked('cancel'))
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_ok)
        hbox_btn.addWidget(btn_cancel)
        hbox_btn.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_grid_size)
        vbox.addLayout(hbox_grid_on)
        vbox.addLayout(hbox_grid_color)
        vbox.addLayout(hbox_btn)

        self.setLayout(vbox)
        self.resize(200, 100)

    def btn_clicked(self, arg):
        if arg == 'ok':
            grid_size = int(self.le_grid_size.text())
            grid_on = self.cb_on.isChecked()
            r, g, b = int(self.le_r.text()), int(self.le_g.text()), int(self.le_b.text())
            grid_color = (r << 16) + (g << 8) + b
            self.signal.emit('grid_setting', (grid_size, grid_on, grid_color))
        self.hide()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = WidgetGridSetting(None)
    widget.show()
    sys.exit(app.exec_())