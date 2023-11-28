import os

from cached_property import cached_property
import numpy as np
import rospkg
from skrobot.coordinates import CascadedCoords
from skrobot.model import RobotModel


class R85(RobotModel):

    """R8_5 Robot Model

    """

    def __init__(self, urdf_path=None, *args, **kwargs):
        super(R85, self).__init__(*args, **kwargs)
        self.name = 'r8_5'

        self.disable_larm = False
        rospack = rospkg.RosPack()
        package_path = rospack.get_path('r8_5')
        self.urdf_path = os.path.join(
            package_path, 'model', 'r8_5.urdf')
        self.load_urdf_file(open(self.urdf_path, 'r'))

        # self.larm_end_coords = CascadedCoords(
        #     parent=self.l_hand_y_link,
        #     name='larm_end_coords')
        self.larm_end_coords = CascadedCoords(
            pos=[-0.0, 0.02, 0.015],
            rot=[0.5, -0.5, -0.5, 0.5],
            parent=self.l_finger_upper_link,
            name='larm_end_coords').rotate(-np.pi / 2.0, 'y').translate((0.0, -0.02, 0.02))
        self.rarm_end_coords = CascadedCoords(
            pos=[-0.0, 0.02, 0.015],
            rot=[0.5, -0.5, -0.5, 0.5],
            parent=self.r_finger_upper_link,
            name='rarm_end_coords').rotate(-np.pi / 2.0, 'y').translate((0.0, -0.02, 0.02))
        self.rarm_hand_camera_end_coords = CascadedCoords(
            pos=[-0.1,  0.02,  0.01],
            parent=self.r_hand_link,
            name='rarm_hand_camera_end_coords').rotate(np.pi, 'z')
        self.larm_hand_camera_end_coords = CascadedCoords(
            pos=[-0.1,  0.02,  0.01],
            parent=self.l_hand_link,
            name='larm_hand_camera_end_coords').rotate(np.pi, 'z')
        # self.larm_end_coords.translate([0.0, 0.035, -0.090]).rotate(
        #     1.6582432798494404e+00,
        #     [0.28340413776899998,
        #      0.91616853222399997,
        #      0.28340309676900000])
        # self.l_wrist_p_link.assoc(self.larm_end_coords)

        if self.disable_larm is True:
            self.joint_list = [
                self.r_zaxis_joint,
                self.r_shoulder_y_joint,
                self.r_elbow_p1_joint,
                self.r_elbow_p2_joint,
                self.r_upper_arm_y_joint,
                self.r_wrist_y_joint,
                self.r_wrist_r_joint,
                self.r_wrist_p_joint,
                self.r_finger_lower_joint,
                self.r_finger_upper_joint]
        else:
            self.joint_list = [
                self.r_zaxis_joint,
                self.r_shoulder_y_joint,
                self.r_elbow_p1_joint,
                self.r_elbow_p2_joint,
                self.r_upper_arm_y_joint,
                self.r_wrist_y_joint,
                self.r_wrist_r_joint,
                self.r_wrist_p_joint,
                self.l_zaxis_joint,
                self.l_shoulder_y_joint,
                self.l_elbow_p1_joint,
                self.l_elbow_p2_joint,
                self.l_upper_arm_y_joint,
                self.l_wrist_y_joint,
                self.l_wrist_r_joint,
                self.l_wrist_p_joint,
                self.l_finger_lower_joint,
                self.l_finger_upper_joint,
                self.r_finger_lower_joint,
                self.r_finger_upper_joint]

    def reset_pose(self):
        self.init_pose()
        self.l_zaxis_joint.joint_angle(0.75)
        self.r_zaxis_joint.joint_angle(0.75)
        self.r_finger_lower_joint.joint_angle(-0.015708)
        self.r_finger_upper_joint.joint_angle(0.054105)
        self.l_finger_lower_joint.joint_angle(-0.003491)
        self.l_finger_upper_joint.joint_angle(0.003491)
        return self.angle_vector()

    @cached_property
    def larm(self):
        larm_links = [
            self.l_zaxis_link,
            self.l_shoulder_y_link,
            self.l_elbow_p1_link,
            self.l_elbow_p2_link,
            self.l_upper_arm_y_link,
            self.l_wrist_link,
            self.l_wrist_p_link,
            self.l_hand_y_link,
            ]

        larm_joints = []
        for link in larm_links:
            if hasattr(link, 'joint'):
                larm_joints.append(link.joint)
        r = RobotModel(link_list=larm_links,
                       joint_list=larm_joints)
        r.inverse_kinematics = lambda *args, **kwargs: self.inverse_kinematics(
            link_list=r.link_list,
            *args, **kwargs)
        r.end_coords = self.larm_end_coords
        return r

    @cached_property
    def rarm(self):
        rarm_links = [
            self.r_zaxis_link,
            self.r_shoulder_y_link,
            self.r_elbow_p1_link,
            self.r_elbow_p2_link,
            self.r_upper_arm_y_link,
            self.r_wrist_link,
            self.r_wrist_p_link,
            self.r_hand_y_link,
            # self.r_hand_link,
            self.r_finger_lower_link,
            self.r_finger_upper_link,
            ]

        rarm_joints = []
        for link in rarm_links:
            if hasattr(link, 'joint'):
                rarm_joints.append(link.joint)
        r = RobotModel(link_list=rarm_links,
                       joint_list=rarm_joints)
        r.inverse_kinematics = lambda *args, **kwargs: self.inverse_kinematics(
            link_list=r.link_list,
            *args, **kwargs)
        r.end_coords = self.rarm_end_coords
        return r
