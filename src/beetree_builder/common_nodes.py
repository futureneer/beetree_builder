#!/usr/bin/env python
import roslib; roslib.load_manifest('beetree')
import rospy 
from std_msgs.msg import *
import beetree

class NodeRoot(Node):

    def __init__(self, name, label):
        L = '?'
        # L = '( ? )\\n ' + label.upper()
        super(NodeRoot,self).__init__(True,None,name,L,'',)

    def get_node_type(self):
        return 'ROOT'

    def get_node_name(self):
        return 'Root'

    def execute(self):
        print 'Executing Root: (' + self.name_ + ')'
        self.child_status_ = self.first_child_.execute()
        print 'ROOT: Child returned status: ' + self.child_status_
        return self.child_status_
