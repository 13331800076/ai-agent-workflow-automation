import os
import signal
import socket
import subprocess
import time

import pytest


def wait_for_port(host: str, port: int, timeout: float = 30.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError(f"Server did not start on {host}:{port} within {timeout}s")


@pytest.fixture(scope="session")
def server():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(project_dir, "src")
    env = os.environ.copy()
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    log_path = os.path.join(project_dir, "server_fixture.log")

    # Use python -m uvicorn for reliability, with --no-reload for CI stability
    with open(log_path, "w") as log_file:
        proc = subprocess.Popen(
            [
                "python", "-m", "uvicorn",
                "workflow_agent.app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            cwd=project_dir,
            env=env,
        )
        try:
            wait_for_port("localhost", 8000)
            yield "http://localhost:8000"
        except Exception as exc:
            # Print server log for debugging
            if os.path.exists(log_path):
                print("\n=== Server Fixture Log ===")
                with open(log_path) as f:
                    print(f.read())
                print("==========================\n")
            raise exc
        finally:
            proc.send_signal(signal.SIGTERM)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
