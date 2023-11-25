import sys
from importlib.resources import files
from pathlib import Path

from copier import Worker
from qualia_core.utils.path import resources_to_path


def qualia_create_plugin(plugin_name: str) -> None:
    src_path = resources_to_path(files('qualia_plugin_template.assets'))/'template'
    dst_path = Path()/f'qualia-plugin-{plugin_name.lower()}'

    print(f'Plugin name: {plugin_name}')
    print(f'Source path: {src_path}')
    print(f'Destination path: {dst_path}')

    data = {'plugin_name': plugin_name}

    with Worker(src_path=str(src_path),
                dst_path=dst_path,
                vcs_ref='HEAD',
                unsafe=True,
                data=data) as worker:
        worker.run_copy()

def main() -> int:
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <plugin_name>')
        sys.exit(1)

    qualia_create_plugin(sys.argv[1])
    return 0


if __name__ == '__main__':
    sys.exit(main())
