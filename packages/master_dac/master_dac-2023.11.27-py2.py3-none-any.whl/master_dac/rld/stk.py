import importlib
import logging
import sys
import zipfile
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List

import torch
from bbrl.agents import Agent, Agents, TemporalAgent
from bbrl.agents.gymnasium import ParallelGymAgent, make_env
from bbrl.workspace import Workspace
from gymnasium import spec
import gymnasium as gym
import gymnasium.spaces as spaces
from gymnasium.envs.registration import load_env_creator
from pystk2_gymnasium import AgentSpec, MonoAgentWrapperAdapter
from tqdm.auto import tqdm


def fail(message: str):
    logging.error(message)
    sys.exit(1)


@contextmanager
def sys_path(dir: Path):
    sys.path.insert(0, str(dir.absolute()))
    yield
    sys.path.pop(0)


def load_player(dir: Path, key: str, zip_file: Path):
    """Check that the BBRL agent is valid and load the agent

    The zip file should contain a:

    - a `pystk_actor.py` file
    - a `pystk_actor.pth` file
    """

    # Extract
    py_dir = dir / f"player_{key}"
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_path = zipfile.Path(zip_ref)
        assert (
            zip_path / "pystk_actor.py"
        ).is_file, "Could not find an pystk_actor.py file"
        assert (
            zip_path / "pystk_actor.pth"
        ).is_file, "Could not find an pystk_actor.pth file"
        logging.info("Extracting %s into %s", zip_file, dir)

        # Extract and set path
        zip_ref.extractall(py_dir)

    (py_dir / "__init__.py").touch()

    # Load and test
    with sys_path(dir):
        # Get the module
        mod_actor = importlib.import_module(f"player_{key}.pystk_actor")

        # Get the environment
        env_name = getattr(mod_actor, "env_name", None) or fail(
            "No env_name in pystk_actor.py"
        )
        assert isinstance(env_name, str), "env_name is not as string in pystk_actor.py"

        # Get the player name
        player_name = getattr(mod_actor, "player_name", None) or fail(
            "No player_name in pystk_actor.py"
        )
        assert isinstance(
            player_name, str
        ), "player_name is not as string in pystk_actor.py"

        env_spec = spec(env_name)
        assert (
            env_spec.entry_point == "pystk2_gymnasium.envs:STKRaceEnv"
        ), f"Not a standard STK race environment (got {env_spec.entry_point})"

        def wrappers_factory(env):
            # Apply environment wrappers
            for wrapper_spec in env_spec.additional_wrappers:
                env = load_env_creator(wrapper_spec.entry_point)(
                    env=env, **wrapper_spec.kwargs
                )

            # Apply the wrappers (if they exist)
            get_wrappers = getattr(mod_actor, "get_wrappers", lambda: [])
            for wrapper in get_wrappers():
                env = wrapper(env)
            return env

        # Load the actor
        get_actor = getattr(mod_actor, "get_actor", None) or fail(
            "No get_actor function in pystk_actor.py"
        )

        def actor_factory(env: gym.Env):
            actor = get_actor(
                torch.load(py_dir / "pystk_actor.pth"),
                env.observation_space[key],
                env.action_space[key],
            )
            return actor

        logging.info("Loaded player %s", player_name)
        return player_name, wrappers_factory, actor_factory

def get_action(workspace: Workspace, t: int):
    name = "action"
    if name in workspace.variables:
        # Action is a tensor
        action = workspace.get(name, t)
    else:
        # Action is a dictionary
        action = {}
        prefix = f"{action}/"
        len_prefix = len(prefix)
        for varname in workspace.variables:
            if not varname.startswith(prefix):
                continue
            keys = varname[len_prefix:].split("/")
            current = action
            for key in keys[:-1]:
                current = current.setdefault(key, {})
            current[keys[-1]] = workspace.get(varname, t)
    return action

def dict_slice(k: int, object):
    if isinstance(object, dict):
        return {key: dict_slice(k, value) for key, value in object.items()}
    return object[k]

def race(hide: bool, zip_files: List[Path]):
    with TemporaryDirectory() as dir:
        dir = Path(dir)
        logging.info("Loading the agents")
        agent_factories = {}
        wrapper_factories = {}
        agents_spec = []
        player_names = []
        for agent_ix, zip_file in enumerate(zip_files):
            key = str(agent_ix)
            player_name, wrappers_factory, agent_factory = load_player(
                dir, key, zip_file
            )
            player_names.append(player_name)
            agent_factories[key] = agent_factory
            wrapper_factories[key] = wrappers_factory
            agents_spec.append(AgentSpec(name=player_name))

        # Create the environment
        n_agents = len(agents_spec)
        env = make_env(
            "supertuxkart/multi-full-v0",
            render_mode=None if hide else "human",
            num_kart=n_agents,
            agents=agents_spec,
            wrappers=[
                partial(MonoAgentWrapperAdapter, wrapper_factories=wrapper_factories)
            ],
        )

        # Get the actors
        assert isinstance(env, MonoAgentWrapperAdapter)

        agents = [agent_factory(env) for key, agent_factory in agent_factories.items()]

        workspaces = [Workspace() for _ in range(n_agents)]
        logging.info("Starting a race")
        
        done = False
        obs, _ = env.reset()
        from bbrl.agents.gymnasium import ParallelGymAgent
        t = 0
        while not done:
            actions = {}
            for ix in range(n_agents):
                key = str(ix)
                obs_agent = ParallelGymAgent._format_frame(obs[key])
                for var_key, var_value in obs_agent.items():
                    workspaces[ix].set(f"env/{var_key}", t, var_value)
                agents[ix](workspaces[ix], t=t)
                action = get_action(workspaces[ix], t=t)
                if isinstance(action, dict):
                    action = dict_slice(0, action)
                else:
                    action = action[0]

                actions[key] = action
                
            obs, reward, terminated, truncated, info = env.step(actions)
            done = terminated or truncated
            t += 1
            
        rewards = info["reward"]
        for ix in range(n_agents):
            key = str(ix)
            print(f"{rewards[key]}\t{info['infos'][key]['position']}\t{ix}\t{player_names[ix]}")
