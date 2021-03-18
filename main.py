import os
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets, QtPositioning, QtGui
from PyQt5.QtGui import QImage 
from PyQt5 import QtQuick
from MarkerModel import MarkerModel
from ExtMapPolyLine import LineModel
import sqlite3


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent,
            resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        #Defining markers
        model = MarkerModel(self)
        linemodel = LineModel(self)

        positions = [(60.016472, 30.258407), (59.868882, 30.299815)]
        urls = ["to_first_pilots.svg", "park_aviatorov.svg"]
        con = sqlite3.connect("info.sqlite")
        cur = con.cursor()
        id_es = [1, 5]
        #Adding markers
        for c, u, id_ in zip(positions, urls, id_es):
            text = cur.execute(f"""Select text from avia_info where id = {id_}""").fetchone()[0]
            pic = cur.execute(f"""Select picture from avia_info where id = {id_}""").fetchone()[0]
            im = QImage()
            im.loadFromData(pic)
            im.save(str(id_) + '.png')
            coord = QtPositioning.QGeoCoordinate(*c)
            source = QtCore.QUrl(u)
            model.appendMarker({"position": coord , "source": source, "text": text, "image": str(id_) + '.png'})

        #Adding Line Coordinates
        pos_lines = [((59.825644, 30.140200), (59.845182, 30.140338)), 
                     ((59.858245, 30.337773), (59.858100, 30.325728), (59.857764, 30.325779), (59.857615, 30.325723), (59.857538, 30.325599), (59.857516, 30.325201)),
                     ((59.855076, 30.337443), (59.854910, 30.324600), (59.854897, 30.324411), (59.854904, 30.324057), (59.854863, 30.321554))]
        id_es = [2, 3, 4]
        for c_, id_, in zip(pos_lines, id_es):
            text = cur.execute(f"""Select text from avia_info where id = {id_}""").fetchone()[0]
            pic = cur.execute(f"""Select picture from avia_info where id = {id_}""").fetchone()[0]
            im = QImage()
            im.loadFromData(pic)
            im.save(str(id_) + '.png')
            geopath = QtPositioning.QGeoPath()
            for j in c_:
                geopath.addCoordinate(QtPositioning.QGeoCoordinate(*j))
            linemodel.appendMarker({"geopath": geopath, "text": text, "image": str(id_) + '.png'})

        #Exchanging with main.qml
        self.rootContext().setContextProperty("markermodel", model)
        self.rootContext().setContextProperty("linemodel", linemodel)

        qml_path = os.path.join(os.path.dirname(__file__), "main.qml")
        self.setSource(QtCore.QUrl.fromLocalFile(qml_path))
        
        #Closing base
        con.close()

    def closeEvent(self, event):
        for i in range(1, 6, 1):
            try:
                os.remove(str(i) + ".png")
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MapWidget()
    w.show()
    sys.exit(app.exec_())