#!/usr/bin/env python
import roslib; roslib.load_manifest('beetree')
import rospy 
from std_msgs.msg import *
import beetree
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class NamedField(QWidget):
  def __init__(self,name,text, parent=None):
    QWidget.__init__(self, parent)
    self.l = QHBoxLayout()
    self.setLayout(self.l)
    self.t = QLabel(name)
    # self.setStyleSheet('background-color:#dedede')
    self.t.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
    self.l.addWidget(self.t)
    self.f = QLineEdit(text)
    self.l.addWidget(self.f)
  def interface(self):
    return self.f.textChanged
  def clear_field(self):
    self.f.clear()
  def set_field(self,text):
    self.f.setText(text)

#-------------------------------------------------------------------------------

class NodeRootGUI(QWidget):
    def __init__(self):
        super(NodeRootGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','root')
        self.name = 'root'
        # self.name_field.interface().connect(self.set_name)
        self.layout_.addWidget(self.name_field)

    def generate(self):
        return beetree.NodeRoot('root','root')


