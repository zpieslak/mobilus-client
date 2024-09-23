import argparse
import logging
import sys
from typing import Tuple, Dict
from mobilus_client.config import Config
from mobilus_client.app import App

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Mobilus Client with specific commands and parameters."
    )
    parser.add_argument('--host', required=True, help="Cosmo GTW address")
    parser.add_argument('--login', required=True, help="User login")
    parser.add_argument('--password', required=True, help="User password")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose logging")
    parser.add_argument('commands', nargs='+', help="Commands to run")

    # Parse arguments
    args = parser.parse_args()

    # Create a config object
    config = Config(
        gateway_host=args.host,
        user_login=args.login,
        user_password=args.password,
    )

    # Set up logging
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format='{"name": "[%(name)s]", "levelname": "%(levelname)s", "message": "%(message)s"}'
    )

    commands = []
    for command_str in args.commands:
        command, params = _parse_command(command_str)
        commands.append((command, params))

    app = App(config)
    responses = app.call(commands)
    print(responses)


def _parse_command(command_str: str) -> Tuple[str, Dict[str, str]]:
    """
    " Parse a command string into a command and a dictionary of parameters. "
    " Example: 'command:param1=value1,param2=value2' "
    " Returns: ('command', {'param1': 'value1', 'param2': 'value2'}) "
    """
    command, *params = command_str.split(':', 1)
    params_dict = dict(param.split('=') for param in params[0].split(',')) if params else {}
    return command, params_dict


if __name__ == '__main__':
    main()
