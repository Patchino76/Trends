import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    property int minValue: 0
    property int maxValue: 100
    property int sliderWidth: 50
    property int sliderHeight: 150

    property alias setpoint: slider.value
    signal sliderValueChanged(real value)


    Rectangle {
        id: backgroundSliderRect
        color: "grey"
        border.color: "black"
        border.width: 2
        radius: 5
        opacity: 0.8
        width: sliderWidth
        height: sliderHeight

        Slider {
            id: slider
            orientation: Qt.Vertical
            anchors.fill: parent
            from: 16
            to: 28
            stepSize: 0.1

            value: setpoint
            onValueChanged: { sliderValueChanged(value); }
        }

        Label {
            text: "16" //minValue.toFixed(2)
            x: -30
            y: slider.height - height
            font.bold: true
            font.pointSize: 12
        }

        Label {
            text: "28" //maxValue.toFixed(0)
            x: -30
            y: 0
            font.bold: true
            font.pointSize: 12
        }
        Text {
            text: slider.value.toFixed(2)
            anchors.bottom: slider.top
            anchors.horizontalCenter: slider.horizontalCenter
            font.bold: true
            font.pointSize: 12
            color: "black"
        }
    }
}
