import os
import yaml

host_script = os.path.dirname(os.path.abspath(__file__))
container_script = '/path/to/container'

config = {
    'image': 'python:3.9',
    'name': 'python_test',
    'volumes': {
        f'{host_script}': {'bind': container_script, 'mode': 'rw'}
    },
    'detach': True,
    'command': ["sh", "-c", f'cd {container_script} && python docker_example.py'],
}

yaml_file_path = 'config.yaml'

with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False)

print(f"Config saved to {yaml_file_path}")
