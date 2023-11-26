import pyperclip
from PySide6 import QtCore, QtGui, QtWidgets

from solie.recipe import outsource


class LongTextView(QtWidgets.QWidget):
    def __init__(self, done_event, payload):
        # ■■■■■ the basic ■■■■■

        super().__init__()

        long_text = payload[0]

        # ■■■■■ full layout ■■■■■

        full_layout = QtWidgets.QVBoxLayout(self)
        cards_layout = QtWidgets.QVBoxLayout()
        full_layout.addLayout(cards_layout)

        label = QtWidgets.QLabel(long_text)
        fixed_width_font = QtGui.QFont("Source Code Pro", 9)
        label.setFont(fixed_width_font)
        label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        cards_layout.addWidget(label)

        # Copy to clipboard button

        async def job_cc(*args):
            pyperclip.copy(long_text)

        button = QtWidgets.QPushButton("Copy to clipboard")
        outsource.do(button.clicked, job_cc)
        button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        full_layout.addWidget(button)
