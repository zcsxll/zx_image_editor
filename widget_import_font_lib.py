from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WidgetImportFontLib(QWidget):
    def __init__(self, signal):
        super().__init__()

        self.signal = signal
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        label_format = QLabel('//注释\r\n#注释\r\n{0x11, 0x22, 0x33, ..., 0xaa,\r\n0x22, 0x33, 0x44, ..., 0x11\r\n...\r\n0x66, 0x77, 0x88, ..., 0x66},')
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        label_format.setPalette(pe)
        hbox_format = QHBoxLayout()
        hbox_format.addWidget(QLabel('字库格式'))
        hbox_format.addWidget(label_format)
        hbox_format.addStretch()

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
        btn_select = QPushButton('...')
        btn_select.clicked.connect(lambda: self.btn_clicked('select'))
        hbox_out = QHBoxLayout()
        hbox_out.addWidget(QLabel('输入文件'))
        hbox_out.addWidget(self.le_file_name)
        hbox_out.addWidget(btn_select)
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
        vbox.addLayout(hbox_format)
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
            self.signal.emit('import', (bits, bit_order, scan_mode, file_name))
            self.hide()
        elif arg == 'cancel':
            self.hide()
        elif arg == 'select':
            lib_name, _ = QFileDialog.getOpenFileName(self, '打开字库', filter='Lib(*.c *.txt)')
            self.le_file_name.setText(lib_name)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = WidgetImportFontLib(None)
    widget.show()
    sys.exit(app.exec_())