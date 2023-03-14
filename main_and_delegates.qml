import QtQuick
import QtQuick.Controls
import QtCharts
import Qt.labs.qmlmodels
import QtQuick.Layouts 

ApplicationWindow {
    width: 1600 
    height: 1024
    visible: true
    property int index : 0
    // property var mainSeries: SplineSeries

    Rectangle{
        id: rectBackground
        anchors.fill: parent
        color: "white"

       
        GridView  {
                id: grid_tags
                width: 1500
                height: 600

                clip: true
                focus: true
                cellWidth: 500
                cellHeight: 300

                model: trends_ui
                delegate: chooser

                DelegateChooser {
                    id: chooser
                    role: "tag_name"
                    // DelegateChoice { roleValue: "Руда"; delegate: trendgaugeDelegate }
                    // DelegateChoice { roleValue: "Вода в мелницата"; delegate: trendDelegate }
                    DelegateChoice { delegate: trendgaugeDelegate }
                }
        }

        // Component {
        //     id: trendDelegate

        //     TrendControl {
        //         width: 300
        //         height: 300

        //         chartTitle: tag_name
        //         spSeries: trend_series
        //         line_color: tag_color
        //         y_axis_min: axis_min
        //         y_axis_max: axis_max
        //     }
        // }
        // Component {
        //     id: gaugeDelegate

        //     VerticalGauge{
        //         x:300
        //         y:200
        //         value: 225
        //         minValue: 200
        //         maxValue: 230
        //     }
        // }

        Component {
            id: trendgaugeDelegate
   
            Rectangle {
                id: backgroundRect
                color: "lightgray"
                border.color: "black"
                border.width: 2
                radius: 10
                opacity: 0.8

                width: grid_tags.cellWidth - 10
                height: grid_tags.cellHeight - 10

                TrendControl {
                    id: trend_control
                    width: 300
                    height: 300
                    anchors.left: backgroundRect.left
                    anchors.leftMargin: 10

                    chartTitle: tag_name
                    spSeries: trend_series
                    line_color: tag_color
                    y_axis_min : axis_min
                    y_axis_max : axis_max
                }

                VerticalGauge{
                    anchors.left: trend_control.right
                    anchors.leftMargin: 30

                    anchors.horizontalCenter: trend_control.horizontalCenter
                    anchors.verticalCenter: trend_control.verticalCenter

                    value: cur_val
                    minValue: axis_min
                    maxValue: axis_max
                    progressColor: tag_color
                }
            }     
        }

        // SliderControl{
        //     x: 10
        //     y: 800
        //     width: 100
        //     height: 200
        //     // value: cur_val
        //     minValue: axis_min
        //     maxValue: axis_max
        // }
    }

}