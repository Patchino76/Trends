import QtQuick
import QtQuick.Controls
import QtCharts
import Qt.labs.qmlmodels
import QtQuick.Layouts 
// import "SliderControl.qml" as SliderControl

ApplicationWindow {
    width: 1920 
    height: 1000
    visible: true
    property int index : 0

    Rectangle{
        id: rectBackground
        anchors.fill: parent
        color: "white"
      
        GridView  {
                id: grid_tags
                width: 1900
                height: 600
                x: 10
                y: 10

                clip: true
                focus: true
                cellWidth: 470
                cellHeight: 300

                model: trends_ui
                delegate: chooser

                DelegateChooser {
                    id: chooser
                    role: "tag_name"
                    DelegateChoice { delegate: trendGaugeDelegate }
                }
        }

        Component {
            id: trendGaugeDelegate
   
            Rectangle {
                id: backgroundRect
                color: "lightgray"
                border.color: "black"
                border.width: 2
                radius: 10

                width: grid_tags.cellWidth - 5
                height: grid_tags.cellHeight - 5

                Rectangle{
                    id: roundRect
                    color: "grey"
                    width: backgroundRect.width
                    height: 30
                    anchors.top: backgroundRect.top
                    radius: backgroundRect.radius
                }
                Rectangle {
                    id: squareRect
                    color: "grey"   
                    height: roundRect.radius
                    anchors.bottom:  roundRect.bottom
                    anchors.left: roundRect.left
                    anchors.right: roundRect.right
                }
                Text{
                    anchors.left: backgroundRect.left
                    anchors.leftMargin: 15
                    anchors.top: backgroundRect.top
                    anchors.topMargin: 0
                    text: "Тренд " + tag_name
                    font.pixelSize: 18
                    color: "white"
                }
                Text{
                    anchors.right: backgroundRect.right
                    anchors.rightMargin: 20
                    anchors.top: backgroundRect.top
                    anchors.topMargin: 0
                    text: "PV            SP "
                    font.pixelSize: 20
                    color: "white"
                }

                Trend2Control {
                    id: trend_control
                    width: 290
                    height: 260
                    anchors.left: backgroundRect.left
                    anchors.leftMargin: 0
                    anchors.top: backgroundRect.top
                    anchors.topMargin: 30

                    chartTitle: tag_name
                    spSeriesProc: trend_proc
                    spSeriesSim: trend_sim
                    scSeriesOut: trend_out

                    line_color: tag_color
                    y_axis_min : axis_min
                    y_axis_max : axis_max
                }

                VerticalGauge{
                    anchors.left: trend_control.right
                    anchors.leftMargin: 35
                    anchors.top: trend_control.top
                    anchors.topMargin: 40

                    value: cur_val_proc
                    minValue: axis_min
                    maxValue: axis_max
                    progressColor: tag_color
                    progressOpacity: 1
                }

                VerticalGauge{
                    anchors.left: trend_control.right
                    anchors.leftMargin: 120
                    anchors.top: trend_control.top
                    anchors.topMargin: 40

                    value: cur_val_sim
                    minValue: axis_min
                    maxValue: axis_max
                    progressColor: "black"
                    // progressOpacity: 0.5
                }
            }     
        }
        Rectangle {
            id: slidersRect
            color: "lightgray"
            border.color: "black"
            border.width: 2
            radius: 10
            opacity: 0.8
            x: 10
            y: 800
            width: 1500
            height: 210


            SliderControl{
                id: slider_cidra
                anchors.left: slidersRect.left
                anchors.leftMargin: 50
                anchors.top: slidersRect.top
                anchors.topMargin: 20
                sliderWidth: 50
                sliderHeight: 180
                setpoint: data_gen.sp_cidra_sim
                onSliderValueChanged: data_gen.sp_cidra_sim = value
            }

                Switch  {
                    anchors.left: slidersRect.left
                    anchors.leftMargin: 110
                    anchors.top: slidersRect.top
                    anchors.topMargin: 20
                    checked: false
                    text: "OFF"

                    onCheckedChanged: {
                        if (checked) {
                            data_gen.save_sp_cidra_sim_to_proc(true)
                            text = "ON"
                        } else {
                            data_gen.save_sp_cidra_sim_to_proc(false)
                            text = "OFF"
                        }
                    }
            }
        }
    }

}