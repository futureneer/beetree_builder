#!/usr/bin/env python
import roslib; roslib.load_manifest('instruktor')
import rospy

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from xdot.xdot_qt import DotWidget
import rospkg
from beetree import *
import beetree_builder
import sys, inspect
from std_msgs.msg import *

class BeetreeBuilder(QWidget):
  def __init__(self,app):
    super(BeetreeBuilder,self).__init__()
    self.app_ = app
    self.setMinimumWidth(700)
    self.setMinimumHeight(500)

    ### SAVE SETTINGS 
    # if rospy.has_param('test_path'):
    #   setting_path = rospy.get_param('test_path')
    #   self.settings = QSettings(setting_path, QSettings.IniFormat)
    # else:
    #   rospy.logerr('Programmer: No settings found, using default')
    #   self.settings = QSettings('/home/kel/ros_workspace/adjutant/adjutant_programmer/settings.ini', QSettings.IniFormat)
    # self.settings.setFallbacksEnabled(False) 
    # self.resize( self.settings.value('size', QSize(270, 225), type=QSize) )
    # self.move(self.settings.value('pos', QPoint(50, 50), type=QPoint))
    ###

    # Load the ui attributes into the main widget
    rospack = rospkg.RosPack()
    ui_path = rospack.get_path('beetree_builder') + '/ui/main.ui'
    uic.loadUi(ui_path, self)

    self.dot_widget = DotWidget()
    self.beetree_layout.addWidget(self.dot_widget)    
    self.show()
    self.showMaximized()

    # Set up ros_ok watchdog timer to handle termination and ctrl-c
    self.ok_timer_ = QTimer(self)
    self.connect(self.ok_timer_, QtCore.SIGNAL("timeout()"), self.check_ok)
    self.ok_timer_.start(1000)

    self.current_tree = {}
    self.root_node = None
    self.gui_selected_node = None
    self.selected_node_field.setText('NONE')

    self.set_up_gui()

    # self.root = NodeRoot('root','start')
    # para_look_and_grab = NodeParallel(self.root,'para_look_and_grab','detect_obj_move_to_bin')
    # act_detect_object = NodeAction(para_look_and_grab,'act_detect_object','detect_obj')
    # sec_pick_move_to_bin = NodeSequence(para_look_and_grab,'sec_pick_move_to_bin','pick_move_to_bin')
    # cond_found_obj = NodeParamCondition(sec_pick_move_to_bin,'cond_found_obj','object_found','test','test')
    # sec_pick_up = NodeSequence(sec_pick_move_to_bin,'sec_pick_up','pick_up')
    # act_move_to_obj = NodeAction(sec_pick_up,'act_move_to_obj','move_to_object')
    # act_grab = NodeAction(sec_pick_up,'act_grab','grab')
    # act_lift = NodeAction(sec_pick_up,'act_lift','lift')
    # act_move = NodeAction(sec_pick_move_to_bin,'act_move','move_above_bin')
    # sec_place = NodeSequence(sec_pick_move_to_bin,'sec_place','place')
    # act_move_to_bin = NodeAction(sec_place,'act_move_to_bin','move_to_bin')    
    # act_release = NodeAction(sec_place,'act_release','release')
    # act_reset = NodeAction(sec_pick_move_to_bin,'act_reset','reset')
    # self.pub_ = rospy.Publisher('/beetree/dot',String)
    # print self.root.generate_dot()
    # self.dot_widget.set_dotcode(self.root.generate_dot())
    # print 'Connecting'

    self.connect(self.dot_widget,SIGNAL("clicked"), self.node_gui_selected_cb)

  # TODO
  # check for unique name when adding nodes
  # recursively turn on or off labels on logical nodes
  # add node as brother - requires change to beetree

  def set_up_gui(self):
    self.node_ready = False
    self.node_list = []
    self.node_names = []
    self.selected_node_type = None
    for name, obj in inspect.getmembers(beetree_builder):
        if inspect.isclass(obj):
            self.node_list.append(obj)
            self.node_names.append(name)

    self.node_type_list.addItems(self.node_names)
    self.node_type_list.activated[str].connect(self.node_type_selected_cb)
    self.add_node_root_btn.clicked.connect(self.add_root_cb)
    self.add_node_child_btn.clicked.connect(self.add_child_cb)
    self.add_node_sibling_btn.clicked.connect(self.add_sibling_cb)
    self.delete_node_btn.clicked.connect(self.delete_cb)
    self.add_node_child_btn.hide()
    self.add_node_sibling_btn.hide()
    self.delete_node_btn.hide()
    #85DE00

  def add_root_cb(self):
    print 'adding root node of type ' + self.selected_node_type
    if self.selected_node_type != None:
      N = self.current_node_generator.generate()
      if type(N) == str:
        # There was an error
        rospy.logerr(str(N))
      else:
        self.current_tree[self.current_node_generator.name] = N 
        self.root_node = N
        self.add_node_child_btn.show()
        self.add_node_root_btn.hide()
        self.generate_tree()
        # Reset the selected node
        self.gui_selected_node = None
        self.selected_node_field.setText('NONE')
        self.selected_node_field.setStyleSheet('background-color:#FFB85C')

  def add_child_cb(self):
    print 'adding child node of type ' + self.selected_node_type
    if self.selected_node_type != None:
        if self.gui_selected_node == None:
          rospy.logerr('There is no parent node selected')
        else:
          N = self.current_node_generator.generate(self.current_tree[self.gui_selected_node])
          if type(N) == str:
            # There was an error
            rospy.logerr(str(N))
          else:
              self.current_tree[self.current_node_generator.name] = N 
              self.generate_tree()
              self.add_node_sibling_btn.show()
              # Reset the selected node
              self.gui_selected_node = None
              self.selected_node_field.setText('NONE')
              self.selected_node_field.setStyleSheet('background-color:#FFB85C')

  def add_sibling_cb(self):
    rospy.logerr('Not implemented yet')
    pass

  def generate_tree(self):
    # print self.root_node.generate_dot()
    self.dot_widget.set_dotcode(self.root_node.generate_dot())

  def delete_cb(self):
    pass

  def node_type_selected_cb(self,text):
    self.clear_node_info()
    self.current_node_generator = self.node_list[self.node_names.index(str(text))]()
    self.selected_node_type = str(text)
    self.node_info_layout.addWidget(self.current_node_generator)

  def clear_node_info(self):
    for i in reversed(range(self.node_info_layout.count())): 
        self.node_info_layout.itemAt(i).widget().setParent(None)

  def closeEvent(self, event):
    # self.settings.setValue('size', self.size())
    # self.settings.setValue('pos', self.pos())
    event.accept()

  def node_gui_selected_cb(self,event):
    if event == 'none':
      self.gui_selected_node = None
      self.selected_node_field.setText('NONE')
      self.selected_node_field.setStyleSheet('background-color:#FFB85C')
    else:
      if event in self.current_tree:
        # print '[' + event + '] found in current tree'
        self.gui_selected_node = event
        self.selected_node_field.setText(str(event).upper())
        self.selected_node_field.setStyleSheet('background-color:#B2E376')
    
  def clean_up(self):
    pass

  def check_ok(self):
    self.update()
    if rospy.is_shutdown():
      self.clean_up()
      self.close()
      self.app_.exit()

# MAIN #########################################################################
if __name__ == '__main__':
  rospy.init_node('beetree',anonymous=True)
  app = QApplication(sys.argv)
  wrapper = BeetreeBuilder(app)
  # Running
  app.exec_()
  # Done

        









  # if self.root_node == None:
  #   self.add_node_child_btn.setText('Add Root Node')
  # else:
  #   self.add_node_child_btn.setText('Add Child Node')








