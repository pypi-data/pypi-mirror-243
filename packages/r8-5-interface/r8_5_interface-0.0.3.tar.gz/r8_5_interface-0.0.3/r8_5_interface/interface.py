from aero_controller.msg import ScriptReqJNameInterf
from aero_controller.srv import RunScript
from aero_controller.srv import RunScriptRequest
import control_msgs.msg
import rospy
from skrobot.interfaces.ros.base import ROSRobotInterfaceBase
from zaxis_controller.srv import ZMove


class R85ROSRobotInterface(ROSRobotInterfaceBase):

    def __init__(self, *args, **kwargs):
        self.disable_larm = False
        super(R85ROSRobotInterface, self).__init__(*args, **kwargs)
        self.vacuum_service = rospy.ServiceProxy(
            '/aero_controller/run_script', RunScript)

    def zmove_client(self, z1, z2, duration):
        rospy.wait_for_service('/zaxis_controller/zmove')
        try:
            zmove = rospy.ServiceProxy('/zaxis_controller/zmove', ZMove)
            resp = zmove(z1, z2, duration)
            return resp
        except rospy.ServiceException as e:
            rospy.logwarn("Service call failed: %s" % e)

    def start_suction(self, arm):
        req = RunScriptRequest()
        if arm == 'rarm':
            req.jname_interf = [
                ScriptReqJNameInterf(
                    joint_name='r_upper_arm_y_joint', script_no=2),
                ScriptReqJNameInterf(
                    joint_name='r_lower_arm_y_joint', script_no=2)]
        else:
            req.jname_interf = [
                ScriptReqJNameInterf(
                    joint_name='l_upper_arm_y_joint', script_no=2),
                ScriptReqJNameInterf(
                    joint_name='l_lower_arm_y_joint', script_no=2)]
        self.vacuum_service(req)

    def stop_suction(self, arm):
        req = RunScriptRequest()
        if arm == 'rarm':
            req.jname_interf = [
                ScriptReqJNameInterf(
                    joint_name='r_upper_arm_y_joint', script_no=3),
                ScriptReqJNameInterf(
                    joint_name='r_lower_arm_y_joint', script_no=3)]
        else:
            req.jname_interf = [
                ScriptReqJNameInterf(
                    joint_name='l_upper_arm_y_joint', script_no=3),
                ScriptReqJNameInterf(
                    joint_name='l_lower_arm_y_joint', script_no=3)]
        self.vacuum_service(req)

    @property
    def larm_controller(self):
        # "r_finger_lower_joint",
        return dict(
            controller_type='larm_controller',
            controller_action='larm_controller/follow_joint_trajectory',  # NOQA
            controller_state='larm_controller/state',
            action_type=control_msgs.msg.FollowJointTrajectoryAction,
            joint_names=[
                "l_zaxis_joint",
                "l_shoulder_y_joint",
                "l_elbow_p1_joint",
                "l_elbow_p2_joint",
                "l_upper_arm_y_joint",
                "l_wrist_y_joint",
                "l_wrist_r_joint",
                "l_wrist_p_joint",
                ]
        )

    @property
    def rarm_controller(self):
        # "r_finger_lower_joint",
        return dict(
            controller_type='rarm_controller',
            controller_action='rarm_controller/follow_joint_trajectory',  # NOQA
            controller_state='rarm_controller/state',
            action_type=control_msgs.msg.FollowJointTrajectoryAction,
            joint_names=[
                "r_zaxis_joint",
                "r_shoulder_y_joint",
                "r_elbow_p1_joint",
                "r_elbow_p2_joint",
                "r_upper_arm_y_joint",
                "r_wrist_y_joint",
                "r_wrist_r_joint",
                "r_wrist_p_joint",
                ]
        )

    @property
    def lhand_controller(self):
        return dict(
            controller_type='lhand_controller',
            controller_action='lhand_controller/follow_joint_trajectory',  # NOQA
            controller_state='lhand_controller/state',
            action_type=control_msgs.msg.FollowJointTrajectoryAction,
            joint_names=[
                "l_finger_lower_joint",
                "l_finger_upper_joint",
                ]
        )

    @property
    def rhand_controller(self):
        return dict(
            controller_type='rhand_controller',
            controller_action='rhand_controller/follow_joint_trajectory',  # NOQA
            controller_state='rhand_controller/state',
            action_type=control_msgs.msg.FollowJointTrajectoryAction,
            joint_names=[
                "r_finger_lower_joint",
                "r_finger_upper_joint",
                ]
        )

    def default_controller(self):
        if self.disable_larm:
            return [self.rarm_controller,
                    self.rhand_controller]
        else:
            return [self.rarm_controller,
                    self.larm_controller,
                    self.lhand_controller,
                    self.rhand_controller]
