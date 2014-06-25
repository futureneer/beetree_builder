#! /usr/bin/env python

import roslib; roslib.load_manifest('beetree_builder')
import rospy

import actionlib
import beetree_builder.msg

class TestAction(object):
  # create messages that are used to publish feedback/result
  _feedback = beetree_builder.msg.TestFeedback()
  _result   = beetree_builder.msg.TestResult()

  def __init__(self, name):
    self._action_name = name
    self._as = actionlib.SimpleActionServer(self._action_name, beetree_builder.msg.TestAction, execute_cb=self.execute_cb, auto_start = False)
    self._as.start()
    
  def execute_cb(self, goal):
    # helper variables
    r = rospy.Rate(1)
    success = True
    
    if self._as.is_preempt_requested():
        rospy.loginfo('%s: Preempted' % self._action_name)
        self._as.set_preempted()
        success = False
        break
    self._as.publish_feedback('RUNNING')
    r.sleep()
      
    if success:
      self._as.set_succeeded('ACTION SUCCEEDED')
      
if __name__ == '__main__':
  rospy.init_node('beetree_builder_test_action')
  TestAction(rospy.get_name())
  rospy.spin()