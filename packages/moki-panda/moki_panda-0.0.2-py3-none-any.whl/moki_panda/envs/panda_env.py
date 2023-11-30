#  --panda机械臂环境--
#  引用库
import gym
from gym import spaces
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

class PandaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):                             #   初始化
        #    创建服务端
        self.Client = p.connect(p.GUI)
        #    设置视角
        p.resetDebugVisualizerCamera(cameraDistance=1.5,
                                     cameraYaw=0,  # left/right angle
                                     cameraPitch=-40,  # up/down angle
                                     cameraTargetPosition=[0.55, -0.35, 0.2])  # camera focus point
        #    动作空间，包括目标三维坐标加上机器人手指关节变量（一共四维）
        self.action_space = spaces.Box(np.array([-1] * 4).astype(np.float32), np.array([1] * 4).astype(np.float32))
        #    观测空间，包括抓钩坐标和两支手指关节变量（一共五维）
        self.observation_space = spaces.Box(np.array([-1] * 5).astype(np.float32), np.array([1] * 5).astype(np.float32))

        self.pandaUid = None
        self.objectUid = None
    def step(self, action):                        #   动作
        p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING)
        orientation = p.getQuaternionFromEuler([0., -math.pi, math.pi / 2.])
        dv = 0.005
        dx = action[0] * dv
        dy = action[1] * dv
        dz = action[2] * dv
        fingers = action[3]

        currentPose = p.getLinkState(self.pandaUid, 11)        # 获取当前状态末连杆信息
        currentPosition = currentPose[4]                       # [0]质心的笛卡尔位置；[4]URDF链接框架的世界位置
        newPosition = [currentPosition[0] + dx,                # 更新末端位置信息
                       currentPosition[1] + dy,
                       currentPosition[2] + dz]
        jointPoses = p.calculateInverseKinematics(self.pandaUid, 11, newPosition, orientation)    #  用逆运动学计算关节角度
        print(jointPoses)
        print(fingers)
        print(list(jointPoses[:7]) + 2 * [fingers])
        p.setJointMotorControlArray(self.pandaUid, list(range(7)) + [9, 10], p.POSITION_CONTROL,  #  驱动关节电机，控制机械臂运动
                                    list(jointPoses[:7]) + 2 * [fingers])                             #  7臂末端，8抓夹与臂链接的固定关节
        p.stepSimulation()

        state_object, _ = p.getBasePositionAndOrientation(self.objectUid)           #  获取当前抓取对象状态信息，位置和姿态
        state_robot = p.getLinkState(self.pandaUid, 11)[0]                          #  获取当前机械臂末连杆状态信息
        state_fingers = (p.getJointState(self.pandaUid, 9)[0], p.getJointState(self.pandaUid, 10)[0])     # 获取当前抓夹手指状态信息

        if state_object[2] > 0.45:            #  抓住物体，且提升0.45高度，奖励1
            reward = 1                        #  奖励可优化，结合距离等因素，可换算比例奖励
            done = True
        else:
            reward = 0
            done = False

        info = {}
        observation = state_robot + state_fingers
        return observation, reward, done, info
    def reset(self):                               #   重置PyBullet环境，返回observation
        #   重置仿真环境
        p.resetSimulation()
        #   配置图形GUI
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)  # 初始化过程不显示
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # 是否打开控件  1=显示GUI控件  0=不显示GUI控件
        p.configureDebugVisualizer(p.COV_ENABLE_TINY_RENDERER, 0)  # 是否使用核显渲染
        #   添加资源路径
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        #   设置环境参数
        p.setGravity(0, 0, -9.8)  # 设置重力
        #   加载模型
        planeUid =  p.loadURDF("plane.urdf", basePosition=[0.5, 0, -0.65])
        tableUid =  p.loadURDF("table/table.urdf", basePosition=[0.5, 0, -0.65])
        trayUid = p.loadURDF("tray/traybox.urdf", basePosition=[0.65, 0, 0])
        self.pandaUid = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)
        #   停靠位置
        rest_poses = [0, -0.215, 0, -2.57, 0, 2.356, 2.356, 0.08, 0.08]
        #   遍历机械臂关节，令其恢复初始位置
        for i in range(7):
            p.resetJointState(self.pandaUid, i, rest_poses[i])
        #   随机放置抓取物体
        state_object = [random.uniform(0.5, 0.8), random.uniform(-0.2, 0.2), 0.05]
        self.objectUid = p.loadURDF("random_urdfs/000/000.urdf", basePosition=state_object)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)  # 初始化过程不显示
        #   获取机械臂状态
        state_robot = p.getLinkState(self.pandaUid, 11)[0]     #[0]  只获取位置新信息
        #   获取抓夹状态
        state_fingers = (p.getJointState(self.pandaUid, 9)[0], p.getJointState(self.pandaUid, 10)[0])
        #   状态观测值
        observation = state_robot + state_fingers
        print(observation)
        # observation = np.array(observation, dtype=float)
        # print(type( observation))
        return observation

    def render(self, mode='human'):                #   可视化，设置相机，获取物体位置信息
        #   设置相机
        view_matrix = p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0.7, 0, 0.05],
                                                          distance=.7,
                                                          yaw=90,
                                                          pitch=-70,
                                                          roll=0,
                                                          upAxisIndex=2)
        #   获取相机数据
        proj_matrix = p.computeProjectionMatrixFOV(fov=60,
                                                   aspect=float(960) / 720,
                                                   nearVal=0.1,
                                                   farVal=100.0)
        #    获取图像
        (_, _, px, _, _) = p.getCameraImage(width=960,
                                            height=720,
                                            viewMatrix=view_matrix,
                                            projectionMatrix=proj_matrix,
                                            renderer=p.ER_BULLET_HARDWARE_OPENGL)

        rgb_array = np.array(px, dtype=np.uint8)
        rgb_array = np.reshape(rgb_array, (720, 960, 4))

        rgb_array = rgb_array[:, :, :3]
        return rgb_array
    def seed(self, seed=None):
        pass
    def close(self):                               #   关闭
        p.disconnect()


