import QtQuick 2.11
import QtPositioning 5.12
import QtLocation 5.12
import QtQuick.Controls 2.15

Rectangle {
    id:rectangle
    width: 1300
    height: 800
    Plugin {
        id: osmPlugin
        name: "osm"
    }
    objectName: "MainRect"
    property variant locationTC: QtPositioning.coordinate(59.938, 30.314)
    property var description: "Объект"
    
    Map {
        objectName: "map"
        id: map
        width: 900
        height: 800
        plugin: osmPlugin
        center: locationTC
        zoomLevel: 10
         
        MapItemView{
            model: linemodel
            delegate: MapPolyline{
                id: polyLine
                line.width: 5
                line.color: 'red'
                path: {                
                    var lines = []
                    for(var i=0; i < model.geopath.size(); i++){
                        lines[i] = model.geopath.coordinateAt(i)
                    }
                polyLine.path = lines
                }

                MouseArea{
                    anchors.fill: parent
                    hoverEnabled: true

                    onClicked: {
                        picture.source = model.image
                        descr.text = model.text_descr
                    }

                    onEntered: {
                        polyLine.line.width = polyLine.line.width * 2
                    }

                    onExited: {
                        polyLine.line.width = polyLine.line.width / 2
                    }
                }
            }      
        } 

        MapItemView{
            model: markermodel
            delegate: MapQuickItem {
                coordinate: model.position_marker
                anchorPoint.x: image.width / 2
                anchorPoint.y: image.height / 2
                sourceItem: 
                    Image { id: image; source: model.source_marker }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        descr.text = model.text_descr
                        picture.source = model.image
                    }

                    onEntered: {
                        image.width = image.width * 2
                        image.height = image.height * 2
                    }
                    onExited:{
                        image.height = image.height / 2
                        image.width = image.width / 2
                    }
                }
            } 
        }
    }

    Rectangle {
        id:info
        x: 900
        width: 400
        height: 800

        ScrollView {
            id: view
            y: 100
            width: 400
            height: 200

            TextArea {
                id: descr
                text: "Объект"
            }
        }

        Image {
            id: picture
            y: 300
            width: 400
            height: 300
            source: "-"
        }
        
    }
}