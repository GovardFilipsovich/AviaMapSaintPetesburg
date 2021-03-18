import os
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtGui
from PyQt5.QtGui import QImage 
from PyQt5 import QtQuick
class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole, TextDescr, ImageRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 4)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []
        

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._markers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.SourceRole:
                return self._markers[index.row()]["source"]
            elif role == MarkerModel.TextDescr:
                return self._markers[index.row()]["text"]
            elif role == MarkerModel.ImageRole:
                return self._markers[index.row()]["image"]
        return QtCore.QVariant()

    def roleNames(self):
        return {MarkerModel.PositionRole: b"position_marker", MarkerModel.SourceRole: b"source_marker",
                MarkerModel.TextDescr: b"text_descr", MarkerModel.ImageRole: b"image"}

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()