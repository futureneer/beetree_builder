#!/usr/bin/env python
import roslib; roslib.load_manifest('beetree_builder')
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

    def generate(self,parent = None):
        return beetree.NodeRoot('root','root')


class NodeParallelGUI(QWidget):
    def __init__(self):
        super(NodeParallelGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','')
        self.name_field.interface().connect(self.set_name)
        self.name = ''
        self.layout_.addWidget(self.name_field)

    def set_name(self,t):
        self.name = str(t)

    def generate(self,parent=None):
        if self.name != '':
            return beetree.NodeParallel(parent,self.name,'')
        else:
            return 'ERROR: node name not defined'


class NodeSequenceGUI(QWidget):
    def __init__(self):
        super(NodeSequenceGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','')
        self.name_field.interface().connect(self.set_name)
        self.name = ''
        self.layout_.addWidget(self.name_field)

    def set_name(self,t):
        self.name = str(t)

    def generate(self,parent=None):
        if self.name != '':
            return beetree.NodeSequence(parent,self.name,'')
        else:
            return 'ERROR: node name not defined'

class NodeActionSampleGUI(QWidget):
    def __init__(self):
        super(NodeActionSampleGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','')
        self.name_field.interface().connect(self.set_name)
        self.name = ''
        self.layout_.addWidget(self.name_field)

        self.label_field = NamedField('Label','')
        self.label_field.interface().connect(self.set_label)
        self.label = ''
        self.layout_.addWidget(self.label_field)

    def set_name(self,t):
        self.name = str(t)

    def set_label(self,t):
        self.label = str(t)

    def generate(self,parent=None):
        if self.name != '':
            if self.label !='':
                return beetree.NodeAction(parent,self.name,self.label)
            else:
                return 'ERROR: node label not defined'
        else:
            return 'ERROR: node name not defined'

class NodeServiceSampleGUI(QWidget):
    def __init__(self):
        super(NodeServiceSampleGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','')
        self.name_field.interface().connect(self.set_name)
        self.name = ''
        self.layout_.addWidget(self.name_field)

        self.label_field = NamedField('Label','')
        self.label_field.interface().connect(self.set_label)
        self.label = ''
        self.layout_.addWidget(self.label_field)

    def set_name(self,t):
        self.name = str(t)

    def set_label(self,t):
        self.label = str(t)

    def generate(self,parent=None):
        if self.name != '':
            if self.label !='':
                return beetree.NodeAction(parent,self.name,self.label)
            else:
                return 'ERROR: node label not defined'
        else:
            return 'ERROR: node name not defined'

class NodeConditionSampleGUI(QWidget):
    def __init__(self):
        super(NodeConditionSampleGUI,self).__init__()
        ### Setup Widget Structure ###
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        #####################
        self.name_field = NamedField('Name','')
        self.name_field.interface().connect(self.set_name)
        self.name = ''
        self.layout_.addWidget(self.name_field)

        self.label_field = NamedField('Label','')
        self.label_field.interface().connect(self.set_label)
        self.label = ''
        self.layout_.addWidget(self.label_field)

    def set_name(self,t):
        self.name = str(t)

    def set_label(self,t):
        self.label = str(t)

    def generate(self,parent=None):
        if self.name != '':
            if self.label !='':
                return beetree.NodeParamCondition(parent,self.name,self.label)
            else:
                return 'ERROR: node label not defined'
        else:
            return 'ERROR: node name not defined'


