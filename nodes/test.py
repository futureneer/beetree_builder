#!/usr/bin/env python
import roslib; roslib.load_manifest('instruktor')
import rospy

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from xdot.xdot_qt import DotWidget
from beetree import *
import sys
from std_msgs.msg import *

class BTWidget(QWidget):
  def __init__(self,app):
    super(BTWidget,self).__init__()
    self.app_ = app
    self.setMinimumWidth(700)
    self.setMinimumHeight(500)
    
    # Setup layout
    self.layout_ = QGridLayout()
    self.setLayout(self.layout_)
    self.dot_widget = DotWidget()
    self.layout_.addWidget(self.dot_widget)
    self.setStyleSheet('background-color:#ffffff')
    self.show()

    # Set up ros_ok watchdog timer to handle termination and ctrl-c
    self.ok_timer_ = QTimer(self)
    self.connect(self.ok_timer_, QtCore.SIGNAL("timeout()"), self.check_ok)
    self.ok_timer_.start(1000)

    self.root = NodeRoot('root','start')
    para_look_and_grab = NodeParallel(self.root,'para_look_and_grab','detect_obj_move_to_bin')
    act_detect_object = NodeAction(para_look_and_grab,'act_detect_object','detect_obj')
    sec_pick_move_to_bin = NodeSequence(para_look_and_grab,'sec_pick_move_to_bin','pick_move_to_bin')
    cond_found_obj = NodeParamCondition(sec_pick_move_to_bin,'cond_found_obj','object_found','test','test')
    sec_pick_up = NodeSequence(sec_pick_move_to_bin,'sec_pick_up','pick_up')
    act_move_to_obj = NodeAction(sec_pick_up,'act_move_to_obj','move_to_object')
    act_grab = NodeAction(sec_pick_up,'act_grab','grab')
    act_lift = NodeAction(sec_pick_up,'act_lift','lift')
    act_move = NodeAction(sec_pick_move_to_bin,'act_move','move_above_bin')
    sec_place = NodeSequence(sec_pick_move_to_bin,'sec_place','place')
    act_move_to_bin = NodeAction(sec_place,'act_move_to_bin','move_to_bin')    
    act_release = NodeAction(sec_place,'act_release','release')
    act_reset = NodeAction(sec_pick_move_to_bin,'act_reset','reset')



    self.pub_ = rospy.Publisher('/beetree/dot',String)
    print self.root.generate_dot()
    self.dot_widget.set_dotcode(self.root.generate_dot())
    print 'Connecting'
    self.connect(self.dot_widget,SIGNAL("clicked"), self.clicked)


  def closeEvent(self, event):
    # self.settings.setValue('size', self.size())
    # self.settings.setValue('pos', self.pos())
    event.accept()

  def clicked(self,event):
    print 'You clicked ' + event

  def clean_up(self):
    pass

  def check_ok(self):
    self.pub_.publish(String(self.root.generate_dot()))

    if rospy.is_shutdown():
      self.clean_up()
      self.close()
      self.app_.exit()


# MAIN #########################################################################
if __name__ == '__main__':
  rospy.init_node('beetree',anonymous=True)
  app = QApplication(sys.argv)
  wrapper = BTWidget(app)
  # Running
  app.exec_()
  # Done

        


















