import os
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtGui
from PyQt5.QtGui import QImage 
from PyQt5 import QtQuick
class LineModel(QtCore.QAbstractListModel):
    TextDescr, ImageRole, Geopath = range(QtCore.Qt.UserRole + 4, QtCore.Qt.UserRole + 7)

    def __init__(self, parent=None):
        super(LineModel, self).__init__(parent)
        self._lines = []
        

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._lines)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == LineModel.Geopath:
                return self._lines[index.row()]["geopath"]
            elif role == LineModel.TextDescr:
                return self._lines[index.row()]["text"]
            elif role == LineModel.ImageRole:
                return self._lines[index.row()]["image"]
        return QtCore.QVariant()

    def roleNames(self):
        return {LineModel.Geopath: b"geopath", LineModel.TextDescr: b"text_descr", 
                LineModel.ImageRole: b"image"}

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._lines.append(marker)
        self.endInsertRows()