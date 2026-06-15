import pytest
import subprocess
import time
import socket
import signal
import os


def wait_for_port(host: str, port: int, timeout: float = 10.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Server did not start on {host}:{port} within {timeout}s")


@pytest.fixture(scope="session")
def server():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(project_dir, "src")
    env = os.environ.copy()
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        ["python", "-m", "workflow_agent.app.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_dir,
        env=env,
    )
    try:
        wait_for_port("localhost", 8000)
        yield "http://localhost:8000"
    finally:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=5)
