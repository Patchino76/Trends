import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts
import Qt5Compat.GraphicalEffects

Item {
    id: root
    property var spSeriesProc: SplineSeries
    property var spSeriesSim: SplineSeries
    property var scSeriesOut: ScatterSeries
    property string chartTitle: "Chart Title"
    property string line_color: "yellow"
    property real y_axis_min: 0
    property real y_axis_max: 300

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
                id: splineSeriesProc
                name: "Spline of Process"
                axisX: axisX
                axisY: axisY
                color: line_color
                useOpenGL: true
            }
            SplineSeries{
                id: splineSeriesSim
                name: "Spline of Simulation"
                axisX: axisX
                axisY: axisY
                color: "white"
                useOpenGL: true 
                style: {
                   penStyle: Qt.DashLine     
                }                            
            }

            ScatterSeries {
                id: scatSeriesOut
                markerShape: ScatterSeries.MarkerShapeCircle
                markerSize: 5
                color: "red"
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
                spSeriesProc.forEach(element => 
                                    { splineSeriesProc.append(element.x,element.y)});
                spSeriesSim.forEach(element => 
                                    { splineSeriesSim.append(element.x,element.y)});
                scSeriesOut.forEach(element => 
                                    { scatSeriesOut.append(element.x,element.y)});
            }
        }
    }

}

