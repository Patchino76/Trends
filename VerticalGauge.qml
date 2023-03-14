import QtQuick 2.0

Item {
    id: gauge
    property real value: 0.5
    property real minValue: 0.0
    property real maxValue: 1.0
    property color progressColor: "grey"
    property real progressOpacity: 1
    property int animationDuration: 500
    property int labelPadding: 45
    property int labelFontSize: 12

    width: 60 + labelPadding * 2 + labelFontSize * 2
    height: 200

    Rectangle {
        id: mainRect
        width: 40
        height: 200
        radius: 5
        border.color: "#333333"
        border.width: 2
        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: "#eeeeee"
            }
            GradientStop {
                position: 1.0
                color: "#333333"
            }
        }
    }

    Rectangle {
        id: progress
        width: 36
        height: 0
        radius: 5
        color: gauge.progressColor
        opacity: progressOpacity
        Behavior on height { NumberAnimation { duration: gauge.animationDuration } }
        anchors.bottom: mainRect.bottom
        anchors.horizontalCenter: mainRect.horizontalCenter
    }

    Text {
        id: valueLabel
        // text: Math.round(gauge.value * 100) + "%"
        font.bold: true
        font.pointSize: gauge.labelFontSize
        color: "#333333"
        anchors.bottom: mainRect.bottom
        anchors.bottomMargin: mainRect.height + 5
        anchors.horizontalCenter: mainRect.horizontalCenter
    }

    Text {
        id: maxLabel
        text: gauge.maxValue
        font.pointSize: gauge.labelFontSize
        color: "#333333"
        anchors.right: mainRect.right
        anchors.top: mainRect.top
        anchors.rightMargin: gauge.labelPadding
    }

    Text {
        id: minLabel
        text: gauge.minValue
        font.pointSize: gauge.labelFontSize
        color: "#333333"
        anchors.right: mainRect.right
        anchors.bottom: mainRect.bottom
        anchors.rightMargin: gauge.labelPadding
    }
    // NumberAnimation {
    //     id: heightAnimation
    //     target: progress
    //     property: "height"
    //     duration: 100
    //     easing.type: Easing.Linear
    // }

    onValueChanged: {
        value = Math.min(Math.max(value, minValue), maxValue);
        progress.height = gauge.height * (value - minValue) / (maxValue - minValue);
        valueLabel.text = (gauge.value).toFixed(2)  + "";

        // heightAnimation.to = value;
        // heightAnimation.start();
    }
}
