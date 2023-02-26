from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WidgetExportFontLib(QWidget):
    def __init__(self, signal):
        super().__init__()

        self.signal = signal
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.combo_box_bits = QComboBox()
        self.combo_box_bits.setEditable(False)
        self.combo_box_bits.addItems(('8', '16', '24', '32'))
        hbox_bites = QHBoxLayout()
        hbox_bites.addWidget(QLabel('位数'))
        hbox_bites.addWidget(self.combo_box_bits)
        hbox_bites.addStretch()

        self.combo_box_bit_order = QComboBox()
        self.combo_box_bit_order.setEditable(False)
        self.combo_box_bit_order.addItems(('高位在前', '低位在前'))
        hbox_bite_order = QHBoxLayout()
        hbox_bite_order.addWidget(QLabel('位顺序'))
        hbox_bite_order.addWidget(self.combo_box_bit_order)
        hbox_bite_order.addStretch()

        self.combo_box_scan_mode = QComboBox()
        self.combo_box_scan_mode.setEditable(False)
        self.combo_box_scan_mode.addItems(('列行', '列列', '行列', '行行'))
        hbox_scan_mode = QHBoxLayout()
        hbox_scan_mode.addWidget(QLabel('扫描模式'))
        hbox_scan_mode.addWidget(self.combo_box_scan_mode)
        hbox_scan_mode.addStretch()

        self.le_file_name = QLineEdit('./font.c')
        self.cb_append = QCheckBox('追加')
        self.cb_append.setChecked(True)
        hbox_out = QHBoxLayout()
        hbox_out.addWidget(QLabel('输出文件'))
        hbox_out.addWidget(self.le_file_name)
        hbox_out.addWidget(self.cb_append)
        hbox_out.addStretch()

        btn_ok = QPushButton('确定')
        btn_ok.clicked.connect(lambda: self.btn_clicked('ok'))
        btn_cancel = QPushButton('取消')
        btn_cancel.clicked.connect(lambda: self.btn_clicked('cancel'))
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_ok)
        hbox_btn.addWidget(btn_cancel)
        hbox_btn.addStretch()

        # self.text = QTextEdit()
        # self.text.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_bites)
        vbox.addLayout(hbox_bite_order)
        vbox.addLayout(hbox_scan_mode)
        vbox.addLayout(hbox_out)
        vbox.addLayout(hbox_btn)
        # vbox.addWidget(self.text)
        self.setLayout(vbox)
        self.resize(300, 100)

    def btn_clicked(self, arg):
        if arg == 'ok':
            bits = int(self.combo_box_bits.currentText())
            bit_order = self.combo_box_bit_order.currentText()
            scan_mode = self.combo_box_scan_mode.currentText()
            file_name = self.le_file_name.text()
            append = self.cb_append.isChecked()
            self.signal.emit('export', (bits, bit_order, scan_mode, file_name, append))
        self.hide()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = WidgetExportFontLib(None)
    widget.show()
    sys.exit(app.exec_())