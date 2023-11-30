from gym.envs.registration import register

register(
    id='panda-v1',
    entry_point='moki_panda.envs:PandaEnv'
)