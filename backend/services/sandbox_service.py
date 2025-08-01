# In backend/services/sandbox_service.py

import docker
import os
from pathlib import Path
from typing import Tuple, Dict, Any
import io
import tarfile

# (Keep LANGUAGE_CONFIGS definition here)
LANGUAGE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "python": {
        "image": "python:3.11-slim-bullseye",
        "filename": "main.py",
        "command": ["python", "main.py"],
    },
    # ... other languages ...
}


class SandboxService:
    # --- THIS IS THE FIX ---
    # Move the client initialization inside the class to make it a class attribute.
    # It will be initialized only once when the class is defined.
    docker_client = None
    try:
        docker_client = docker.from_env()
        docker_client.ping()
        print("✅ Docker client connected successfully.")
    except Exception as e:
        print(f"❌ Could not connect to Docker daemon. Please ensure Docker is running. Error: {e}")
        # `docker_client` remains None if connection fails

    @staticmethod
    def execute_code(language: str, code: str) -> Tuple[str, str, int]:
        """
        Executes code by creating a container, injecting the file, starting it,
        and then explicitly executing the command.
        """
        # Now, access the client as a class attribute using `SandboxService.docker_client`
        if not SandboxService.docker_client:
            return "Error: Docker client is not available.", "Could not connect to Docker daemon.", 1

        if language not in LANGUAGE_CONFIGS:
            return f"Error: Language '{language}' is not supported.", "", 1

        config = LANGUAGE_CONFIGS[language]
        container_name = f"sandbox-exec-{os.urandom(6).hex()}"
        container = None

        try:
            # Step 1: Create the container.
            print(f"Creating sandbox container '{container_name}'...")
            # Access the client via the class name.
            container = SandboxService.docker_client.containers.create(
                image=config["image"],
                command=["sleep", "60"],
                working_dir="/app",
                name=container_name,
                network_disabled=True,
                mem_limit="256m",
                cpu_shares=512,
                detach=True,
            )

            # Step 2: Create and inject the TAR archive.
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                code_bytes = code.encode('utf-8')
                tar_info = tarfile.TarInfo(name=config["filename"])
                tar_info.size = len(code_bytes)
                tar.addfile(tar_info, io.BytesIO(code_bytes))
            tar_stream.seek(0)

            print(f"Injecting code into '{container_name}'...")
            container.put_archive(path="/app", data=tar_stream)

            # Step 3: Start the container.
            container.start()

            # Step 4: Execute commands in the running container.
            print("Running diagnostic 'ls'...")
            ls_exit_code, (ls_stdout, ls_stderr) = container.exec_run("ls -la /app", demux=True)
            
            stdout = ls_stdout.decode('utf-8') if ls_stdout else ""
            stderr = ls_stderr.decode('utf-8') if ls_stderr else ""

            if ls_exit_code == 0 and config["filename"] in stdout:
                print(f"File found. Executing main command...")
                exec_exit_code, (exec_stdout, exec_stderr) = container.exec_run(config["command"], demux=True)
                
                stdout += "\n--- EXECUTION ---\n" + (exec_stdout.decode('utf-8') if exec_stdout else "")
                stderr += "\n--- EXECUTION ---\n" + (exec_stderr.decode('utf-8') if exec_stderr else "")
                final_exit_code = exec_exit_code
            else:
                print("Error: File was not found in container even after injection.")
                stderr += f"\nError: ls failed with code {ls_exit_code} or file not found."
                final_exit_code = ls_exit_code if ls_exit_code != 0 else 1

            return stdout, stderr, final_exit_code

        except Exception as e:
            print(f"An unexpected error occurred for {container_name}: {e}")
            return "", str(e), 1
        finally:
            if container:
                try:
                    # Access the client via the class name for cleanup if needed.
                    SandboxService.docker_client.containers.get(container_name).remove(force=True)
                    print(f"Container {container_name} removed successfully.")
                except docker.errors.NotFound:
                    pass # Already removed or failed to create
                except Exception as e:
                    print(f"Error during container cleanup: {e}")