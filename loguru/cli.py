import argparse
import os.path

from loguru import LOGURU_DATA_DIR
from loguru.core.cli_app import CLIApp
from loguru.core.models.config import Config
from loguru.core.tool_impls import LogSearchTool

default_config = {
    "num_chunks_to_return": 100,
    "ollama": {
        "hosts": [
            "http://localhost:11434/"
        ],
        # "llm_name": "llama3",  # use mistral for function calling
        "llm_name": "mistral",
        "embedding_model_name": "all-MiniLM-L6-v2",
        "options": {
            "temperature": 0.1
        }
    },
    "data_sources": [
        {
            "type": "filesystem",
            "ds_params": {
                "recursion_depth": 2,
                "file_size_limit": "100MB",
                "scan_locations": [{
                    "location": "/path/to/logs",
                    "pattern": r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2})'
                }]
            }
        }
    ]
}

tool_implementations = [
    LogSearchTool,
]


def _init_cfg(cfg_file_path: str) -> Config:
    if not os.path.exists(cfg_file_path):
        print(f'Config file not found: {cfg_file_path}, creating default config...')
        cfg = Config(**default_config)
        os.makedirs(os.path.dirname(cfg_file_path), exist_ok=True)
        with open(cfg_file_path, 'w') as f:
            f.write(cfg.model_dump_json(indent=4))
    else:
        print(f'Using config: {cfg_file_path}')
        with open(cfg_file_path, 'r') as f:
            cfg_contents = f.read()
        return Config.model_validate_json(cfg_contents)


def main():
    parser = argparse.ArgumentParser(description="CLI for Loguru AI")
    parser.add_argument(
        '-c',
        '--config',
        dest='config_file_path',
        help='Path to the config file',
        required=False,
        default=None
    )
    op_choices = ['run', 'scan', 'show-config']
    parser.add_argument(
        dest='operation',
        help=f'Operation to perform. i.e, {" / ".join(op_choices)}',
        choices=op_choices,
        metavar='operation'
    )

    args: argparse.Namespace = parser.parse_args()

    operation = args.operation
    cfg_path = None

    if 'config_file_path' not in args or args.config_file_path is None or args.config_file_path == "":
        cfg_path = os.path.join(LOGURU_DATA_DIR, 'config.json')
    else:
        cfg_path = args.config_file_path
    loaded_config: Config = _init_cfg(cfg_path)

    if operation == 'run':
        CLIApp(config=loaded_config, with_tools=False, tool_registry=tool_implementations).start()
    elif operation == 'scan':
        # reload log files and their metadata and rebuild the vectorstore
        CLIApp(config=loaded_config, with_tools=False, tool_registry=tool_implementations).scan_and_rebuild_cache()
    elif operation == 'show-config':
        show_config(config_file_path=cfg_path)
    else:
        print('Unknown operation!')
        parser.print_help()


def show_config(config_file_path: str):
    print('Config file contents:')
    with open(config_file_path, 'r') as f:
        print(f.read())


if __name__ == "__main__":
    main()
