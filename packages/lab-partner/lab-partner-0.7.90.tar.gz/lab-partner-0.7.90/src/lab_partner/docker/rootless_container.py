import logging
import sys
import time
import itertools
from subprocess import CalledProcessError
from typing import Tuple, Dict

from .daemon_info import DockerDaemonInfo
from .run_builder import DockerRunBuilder
from ..process_utils import run_process, run_process_quiet


logger = logging.getLogger(__name__)


ROOTLESS_DOCKER_NAME = 'lab-rootless-docker'
ROOTLESS_DOCKER_HOST = 'localhost'
ROOTLESS_DOCKER_PORT = 2375
ROOTLESS_DOCKER_URL = f'tcp://{ROOTLESS_DOCKER_HOST}:{ROOTLESS_DOCKER_PORT}'

WAITING_ANIMATION_FRAMES = itertools.cycle(['|', '/', '—', '\\'])


class RootlessDockerContainer(object):
    """

    """
    def __init__(self, container_name: str, daemon_info: DockerDaemonInfo):
        self.container_name = container_name
        self._daemon_info = daemon_info

    def does_rootless_container_exist(self) -> bool:
        for c in self._daemon_info.containers:
            if self.container_name == c['Names']:
                return True
        return False

    def is_rootless_container_running(self) -> bool:
        for c in self._daemon_info.containers:
            if self.container_name == c['Names'] and 'running' == c['State']:
                return True
        return False

    def is_rootless_container_not_running(self) -> bool:
        for c in self._daemon_info.containers:
            if self.container_name == c['Names'] and 'running' != c['State']:
                return True
        return False

    def start_rootless_container(self, workspace_path: str, network_name: str) -> DockerDaemonInfo:
        if self.is_rootless_container_running():
            logger.info(f'Rootless container {self.container_name}')
            return DockerDaemonInfo.build_with_docker_host(ROOTLESS_DOCKER_URL)
        else:
            logger.info(f'Starting rootless container. It can take a couple minutes to start')

        if self.is_rootless_container_not_running():
            logger.info(f'Killing dead rootless container {self.container_name}')
            for log_line in run_process(f'docker rm -f {self.container_name}'):
                logger.info(log_line)

        run_rootless_docker_cmd = DockerRunBuilder('docker:24.0.7-dind-rootless')
        run_rootless_docker_cmd.options() \
            .with_name(self.container_name) \
            .with_hostname(self.container_name) \
            .with_privileged() \
            .with_daemon() \
            .with_user() \
            .with_env('DOCKER_TLS_CERTDIR', '') \
            .with_port_mapping(ROOTLESS_DOCKER_PORT, ROOTLESS_DOCKER_PORT) \
            .with_port_mapping(80, 80) \
            .with_bind_mount(workspace_path, workspace_path) \
            .with_bind_mount('/tmp', '/tmp') \
            .with_bind_mount('/dev', '/dev') \
            .with_named_volume('rootless-storage', '/var/lib/docker') \
            .with_named_volume('rootless-user-storage', '/home/rootless/.local/share/docker') \
            .with_mount_home() \
            .with_mount_user_run() \
            .with_network(network_name)

        for log_line in run_process(run_rootless_docker_cmd.build()):
            logger.info(log_line)

        self._wait_for_rootless()

        docker_daemon_info = DockerDaemonInfo.build_with_docker_host(ROOTLESS_DOCKER_URL)
        if not docker_daemon_info.network_exists(network_name):
            docker_daemon_info.create_network(network_name)
        return docker_daemon_info

    def _wait_for_rootless(self, timeout: int = 60) -> None:
        start_time = time.perf_counter()
        while True:
            if not self.is_rootless_container_running():
                time.sleep(1)
                continue
            try:
                run_process_quiet('docker info', {'DOCKER_HOST': ROOTLESS_DOCKER_URL})
                break
            except CalledProcessError as ex:
                elapsed_time = time.perf_counter() - start_time
                sys.stdout.write(f'{next(WAITING_ANIMATION_FRAMES)} Waiting for rootless docker to start\r')
                sys.stdout.flush()
                if elapsed_time >= timeout:
                    raise TimeoutError(f'Timeout waiting for rootless docker after {timeout} seconds', ex)
                time.sleep(.1)
