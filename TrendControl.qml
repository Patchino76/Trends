import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts
import Qt5Compat.GraphicalEffects

Item {
    id: root
    // property SplineSeries spSeries
    property var spSeries: SplineSeries
    property string chartTitle: "Chart Title"
    property string line_color: "yellow"
    property int y_axis_min: 0
    property int y_axis_max: 300

        Rectangle{
        id: rectBackground
        implicitWidth: rectBackground.width
        implicitHeight: rectBackground.height
        radius: 10
        anchors.fill: parent
        anchors.margins: 10
        clip: true
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#131414" }
            GradientStop { position: 1.0; color: "#434447" }
        }

        ChartView{
            id: chart
            anchors.fill: parent
            antialiasing: true
            theme: ChartView.ChartThemeDark
            backgroundColor: "transparent"
            title: chartTitle
            legend.visible: false

            SplineSeries{
                id: splineSeries
                axisX: axisX
                axisY: axisY
                color: line_color
                useOpenGL: true

            }
            ValueAxis {
                id: axisX
                min: 0
                max: 100
                visible: false
                gridVisible: false
                labelsVisible: false
            }

            ValueAxis {
                id: axisY
                min: y_axis_min
                max: y_axis_max
                labelsVisible: true
                visible: true
            }
            Component.onCompleted: {
                spSeries.forEach(element => 
                                    { splineSeries.append(element.x,element.y)});
            }
        }
    }

}

