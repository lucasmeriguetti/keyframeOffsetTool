from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Slot, Qt
from maya import cmds


def get_timeline_range():
    start_timeline = cmds.playbackOptions(query = True, min = True)
    end_timeline = cmds.playbackOptions(query = True, max = True)
    return [start_timeline, end_timeline]

def get_channelbox_attributes():
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')    #fetch maya's main channelbox
    attrs = cmds.channelBox(channelBox, q=True, sma=True)

    return attrs

def get_timeline_slider_range():
    aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')

    if cmds.timeControl(aPlayBackSliderPython, query = True, rangeVisible = True):
        time_slider_range = cmds.timeControl(aPlayBackSliderPython, query = True, rangeArray = True)
        timeline_range =  list(time_slider_range)
        return timeline_range
        
    return None


def get_selection():
    selection = cmds.ls(sl = True)

    #return the list of objects
    return selection

def keyframe_offset(value, timeline_range):
    #get timeline range
    slider_range = timeline_range
    selection = get_selection()
    size = len(selection) or 0
    
    for obj in selection:
        obj_index = selection.index(obj) + 1
        try:
            cmds.keyframe(obj, relative = True, at = get_channelbox_attributes(),
             time = ((slider_range[0]), (slider_range[1])), timeChange = obj_index * value)
        except:
            cmds.keyframe(obj, relative = True, time = ((slider_range[0]), (slider_range[1])), timeChange = obj_index * value)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(315, 150)
        Form.setMinimumSize(QtCore.QSize(50, 50))
        Form.setMaximumSize(QtCore.QSize(315, 150))
        Form.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.sld_keyframe = QtWidgets.QSlider(Form)
        self.sld_keyframe.setGeometry(QtCore.QRect(20, 100, 271, 30))
        self.sld_keyframe.setMinimum(-20)
        self.sld_keyframe.setMaximum(20)
        self.sld_keyframe.setOrientation(QtCore.Qt.Horizontal)
        self.sld_keyframe.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sld_keyframe.setTickInterval(1)
        self.sld_keyframe.setObjectName("sld_keyframe")
        self.btn_in = QtWidgets.QPushButton(Form)
        self.btn_in.setGeometry(QtCore.QRect(20, 40, 40, 23))
        self.btn_in.setObjectName("btn_in")
        self.btn_out = QtWidgets.QPushButton(Form)
        self.btn_out.setGeometry(QtCore.QRect(250, 40, 40, 23))
        self.btn_out.setObjectName("btn_out")
        self.spin_in = QtWidgets.QDoubleSpinBox(Form)
        self.spin_in.setGeometry(QtCore.QRect(70, 40, 62, 22))
        self.spin_in.setDecimals(1)
        self.spin_in.setMinimum(-10000.0)
        self.spin_in.setMaximum(10000.0)
        self.spin_in.setSingleStep(5.0)
        self.spin_in.setObjectName("spin_in")
        self.spin_out = QtWidgets.QDoubleSpinBox(Form)
        self.spin_out.setGeometry(QtCore.QRect(180, 40, 62, 22))
        self.spin_out.setMinimum(-10000.0)
        self.spin_out.setMaximum(10000.0)
        self.spin_out.setSingleStep(5.0)
        self.spin_out.setObjectName("spin_out")
        self.lb_timeline = QtWidgets.QLabel(Form)
        self.lb_timeline.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.lb_timeline.setObjectName("lb_timeline")
        self.lb_offset = QtWidgets.QLabel(Form)
        self.lb_offset.setGeometry(QtCore.QRect(20, 80, 47, 13))
        self.lb_offset.setObjectName("lb_offset")

        
        
        self.retranslateUi(Form)

        self.interact()
        self.is_get_time_slider_range = False
        self.timeline_range = self.get_timeline();

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Keyframe Offset"))
        self.btn_in.setText(_translate("Form", "In"))
        self.btn_out.setText(_translate("Form", "Out"))
        self.lb_timeline.setText(_translate("Form", "Timeline"))
        self.lb_offset.setText(_translate("Form", "Offset"))

    def keyframe_offset(self):

        if self.get_timeline_slider() != None:
            self.is_get_time_slider_range = True
            self.timeline_range = self.get_timeline_slider()  

        if not self.is_get_time_slider_range:
            self.timeline_range = [self.spin_in.value(), self.spin_out.value()]

        self.new_value = (float(self.sld_keyframe.value() - self.oldvalue )/10.0)

        keyframe_offset(self.new_value,  self.timeline_range)
        
        self.oldvalue  = self.sld_keyframe.value()

    def reset_value(self):
        self.is_get_time_slider_range = False
        self.globalvalue = self.sld_keyframe.value()
        self.sld_keyframe.setValue(0)

    def slider_pressed(self):
        self.oldvalue = self.sld_keyframe.value()

    
    def get_timeline_slider(self):
        return get_timeline_slider_range()

    def get_timeline(self):
        timeline = self.get_timeline_slider()
        
        if timeline == None:
            timeline = get_timeline_range()

        return timeline 

    def update_spinners(self):
        self.spin_in.setValue(self.get_timeline()[0])
        self.spin_out.setValue(self.get_timeline()[1])

    def btn_in_clicked(self):
        self.spin_in.setValue(self.get_timeline()[0])

    def btn_out_clicked(self):
        self.spin_out.setValue(self.get_timeline()[1])

    def interact(self):
        self.oldvalue = 0
        self.globalvalue = 0

        self.sld_keyframe.sliderPressed.connect(self.slider_pressed)
        self.sld_keyframe.sliderMoved.connect(self.keyframe_offset)
        self.sld_keyframe.sliderReleased.connect(self.reset_value)
        self.update_spinners()

        self.btn_in.clicked.connect(self.btn_in_clicked)
        self.btn_out.clicked.connect(self.btn_out_clicked)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    app.exec_()


