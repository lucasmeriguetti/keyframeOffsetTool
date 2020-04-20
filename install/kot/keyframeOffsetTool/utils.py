import maya.cmds as cmds
import maya.mel as mel

def get_timeline_range():
    start_timeline = cmds.playbackOptions(query = True, min = True)
    end_timeline = cmds.playbackOptions(query = True, max = True)
    return [start_timeline, end_timeline]

def get_channelbox_attributes():
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')    #fetch maya's main channelbox
    attrs = cmds.channelBox(channelBox, q=True, sma=True)

    return attrs

def get_timeline_slider_range():
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')

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
        print get_channelbox_attributes()
        try:
            cmds.keyframe(obj, relative = True, at = get_channelbox_attributes(),
             time = ((slider_range[0]), (slider_range[1])), timeChange = obj_index * value)
        except:
            cmds.keyframe(obj, relative = True, time = ((slider_range[0]), (slider_range[1])), timeChange = obj_index * value)

