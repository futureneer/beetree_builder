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
import os,sys, inspect, ast
from std_msgs.msg import *
import roslib
import rospkg

def clear_cmd():
    os.system(['clear','cls'][os.name == 'nt'])

def load_beetree_plugins():
    rospack = rospkg.RosPack()
    to_check = rospack.get_depends_on('beetree', implicit=False)
    clear_cmd()
    rospy.logwarn('Beetree Builder: Starting up...')
    print 'Found packages that have beetree dependency...'
    print to_check
    plugins = []    
    descriptions = []
    names = []
    types = []
    for pkg in to_check:
        m = rospack.get_manifest(pkg)
        p_modules = m.get_export('beetree_builder', 'plugin')
        p_types = m.get_export('beetree_builder', 'type')
        p_descriptions = m.get_export('beetree_builder', 'description')
        p_names = m.get_export('beetree_builder', 'name')
        # p_descriptions = manifest.get_export('rcommander', 'tab')
        if not p_modules:
            continue
        print '- Package ['+pkg+'] has plugins:'
        if p_modules == []:
          print '--- NONE'

        for p_module, p_description, p_name,p_type in zip(p_modules,p_descriptions,p_names,p_types):
            print '--- ' + p_module
            print '----- ' + p_description
            print '----- ' + p_name
            print '----- ' + p_type
            # try:
            roslib.load_manifest(pkg)
            package = __import__(pkg)
            sub_mod = p_module.split('.')[1:][0]
            print sub_mod
            module = getattr(package, sub_mod)
            plugins.append(module)
            descriptions.append(p_description)
            names.append(p_name)               
            types.append(p_type)                

    return plugins, descriptions, names, types

class BeetreeBuilder(QWidget):
  def __init__(self,app):
    super(BeetreeBuilder,self).__init__()
    self.app_ = app
    self.setMinimumWidth(700)
    self.setMinimumHeight(500)
    # Load the ui attributes into the main widget
    rospack = rospkg.RosPack()
    ui_path = rospack.get_path('beetree_builder') + '/ui/main_alt.ui'
    uic.loadUi(ui_path, self)
    # Create the Graph Visualization Pane
    self.dot_widget = DotWidget()
    self.beetree_layout.addWidget(self.dot_widget)    
    # Finish Up
    self.show()
    self.showMaximized()

    # Set up ros_ok watchdog timer to handle termination and ctrl-c
    self.ok_timer_ = QTimer(self)
    self.connect(self.ok_timer_, QtCore.SIGNAL("timeout()"), self.check_ok)
    self.ok_timer_.start(1000)

    # Set up Behavior Tree structure
    self.current_tree = {}
    self.root_node = None
    self.gui_selected_node = None
    self.selected_node_field.setText('NONE')
    # Get known Beetree Builder Node Plugins
    self.parse_plugin_info()
    # Set up the gui with plugin information
    self.set_up_gui()
    # Set up communication between node view and the rest of the app
    self.connect(self.dot_widget,SIGNAL("clicked"), self.node_gui_selected_cb)

  # TODO
  # check for unique name when adding nodes
  # recursively turn on or off labels on logical nodes
  # add node as brother - requires change to beetree

  def parse_plugin_info(self):
    self.plugins = {}
    plugins, plugin_descriptions, plugin_names, plugin_types = load_beetree_plugins()
    for plug,desc,name,typ in zip(plugins,plugin_descriptions,plugin_names,plugin_types):
      self.plugins[name] = {'module':plug, 'type':typ, 'name':name, 'description':desc}

  def set_up_gui(self):
    self.selected_node_label = None
    self.active_node_type = None
    # Create node list 
    self.node_model = QStandardItemModel()
    self.node_model.setHorizontalHeaderLabels(['Name', 'Description'])
    self.node_tree_view.setModel(self.node_model)
    self.node_tree_view.clicked.connect(self.selected_list_node_cb)
    self.node_tree_view.expanded.connect(self.expanded_cb)
    # Set up groups for standard types
    logical = QStandardItem('Logical Nodes')
    action = QStandardItem('Action Nodes')
    condition = QStandardItem('Condition Nodes')
    # Load in nodes
    for n in self.plugins.itervalues():
      item = QStandardItem(n['name'])
      if n['type'] == 'LOGIC':
        logical.appendRow(item)
      if n['type'] == 'ACTION':
        action.appendRow(item)
      if n['type'] == 'CONDITION':
        condition.appendRow(item)
    self.node_model.appendRow(logical)
    self.node_model.appendRow(action)
    self.node_model.appendRow(condition)
    self.node_tree_view.resizeColumnToContents(0)
    # Connect Buttons in GUI for Adding Nodes
    self.add_node_root_btn.clicked.connect(self.add_root_cb)
    self.add_node_child_btn.clicked.connect(self.add_child_cb)
    self.add_node_sibling_btn.clicked.connect(self.add_sibling_cb)
    self.delete_node_btn.clicked.connect(self.delete_cb)
    self.add_node_child_btn.hide()
    self.add_node_sibling_btn.hide()
    self.delete_node_btn.hide()

  def expanded_cb(self):
    self.node_tree_view.resizeColumnToContents(0)

  def selected_list_node_cb(self,val):
    name = str(self.node_model.itemFromIndex(val).text())
    print 'Selected node [' + name + '] from list.'
    if self.plugins.has_key(name):
      self.clear_node_info()
      self.current_node_generator = self.plugins[name]['module']()
      self.selected_node_type = self.plugins[name]['type']
      self.node_info_layout.addWidget(self.current_node_generator)

  def add_root_cb(self):
    print 'adding root node of type ' + self.selected_node_type
    if self.selected_node_type != None:
      N = self.current_node_generator.generate()
      if type(N) == str:
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

  def delete_cb(self):
    pass

  def generate_tree(self):
    # print self.root_node.generate_dot()
    self.dot_widget.set_dotcode(self.root_node.generate_dot())

  def clear_node_info(self):
    for i in reversed(range(self.node_info_layout.count())): 
        self.node_info_layout.itemAt(i).widget().setParent(None)

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

### OTHER FUNCTIONS ###
  def closeEvent(self, event):
    event.accept()

  def check_ok(self):
    self.update()
    if rospy.is_shutdown():
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








