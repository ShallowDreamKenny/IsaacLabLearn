"""
@FileName：Humanoid.py
@Description：The Humanoid env cfg
@Author：Ferry
@Time：2024/10/31 下午8:57
@Copyright：©2024-2024 ShanghaiTech University-RIMLAB
"""
from __future__ import annotations

from omni.isaac.lab_assets import HUMANOID_CFG, H1_CFG

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.assets import ArticulationCfg
from omni.isaac.lab.envs import DirectRLEnvCfg
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.sim import SimulationCfg
from omni.isaac.lab.terrains import TerrainImporterCfg
from omni.isaac.lab.utils import configclass

from Create_a_Direct_Workflow_RL_Env.Humanoid.LocomotionEnv import LocomotionEnv

@configclass
class HumanoidCfg(DirectRLEnvCfg):
    # env
    episode_length_s = 15.0
    decimation = 2
    action_scale = 1.0
    # humanoid
    action_space = 21
    observation_space = 75

    # simulation
    sim: SimulationCfg = SimulationCfg(dt=1 / 120, render_interval=decimation)
    terrain: TerrainImporterCfg = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        collision_group=1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="average",
            restitution_combine_mode="average",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
        debug_vis=False
    )

    scene: InteractiveSceneCfg = InteractiveSceneCfg(num_envs=4096, env_spacing=4.0, replicate_physics=True)

    # robot
    robot: ArticulationCfg = HUMANOID_CFG.replace(prim_path="/World/envs/env_.*/Robot")
    joint_gears: list = [
        67.5000,  # lower_waist
        67.5000,  # lower_waist
        67.5000,  # right_upper_arm
        67.5000,  # right_upper_arm
        67.5000,  # left_upper_arm
        67.5000,  # left_upper_arm
        67.5000,  # pelvis
        45.0000,  # right_lower_arm
        45.0000,  # left_lower_arm
        45.0000,  # right_thigh: x
        135.0000,  # right_thigh: y
        45.0000,  # right_thigh: z
        45.0000,  # left_thigh: x
        135.0000,  # left_thigh: y
        45.0000,  # left_thigh: z
        90.0000,  # right_knee
        90.0000,  # left_knee
        22.5,  # right_foot
        22.5,  # right_foot
        22.5,  # left_foot
        22.5,  # left_foot
    ]

    heading_weight: float = .5
    up_weight: float = .1

    energy_cost_scale: float = .05
    actions_cost_scale: float = .01
    alive_reward_scale: float = 2.0
    dof_vel_scale: float = .1

    death_cost: float = -1.0
    termination_height: float = .8
    angular_velocity_scale: float = .25
    contact_force_scale: float = .01

class HumanoidEnv(LocomotionEnv):
    cfg: HumanoidCfg
    def __init__(self, cfg: HumanoidCfg, render_mode:str | None = None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)