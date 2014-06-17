#!/usr/bin/env python
import roslib; roslib.load_manifest('beetree_builder')
import rospy
import os,sys
from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget
from python_qt_binding.QtGui import QPalette
from python_qt_binding.QtCore import Qt
from xdot.xdot_qt import DotWidget
import std_msgs.msg
import rospkg

class Builder(Plugin):

    def __init__(self, context):
        super(Builder, self).__init__(context)

        self.setObjectName('BeetreeBuilder')
        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which is a sibling of this file
        rospack = rospkg.RosPack()
        ui_path = rospack.get_path('beetree_builder') + '/ui/main.ui'
        # Load the ui attributes into the main widget
        loadUi(ui_path, self._widget)
        self._widget.setObjectName('BeetreeBuilderPluginUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        # Add widget to the user interface
        context.add_widget(self._widget)
        palette = QPalette ()
        palette.setColor(QPalette.Background, Qt.white)
        self._widget.setPalette(palette)

        # Add custom options
        self._widget.node_type_list.addItems(['test1','test2'])

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass
