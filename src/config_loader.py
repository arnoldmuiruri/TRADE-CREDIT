"""Load configuration from YAML files and environment variables."""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


def load_config(config_path):
    """
    Load YAML config and substitute environment variables.

    Args:
        config_path: Path to YAML config file

    Returns:
        Dictionary with loaded config
    """
    # Load environment variables from .env
    load_dotenv()

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Substitute user_agent_template with email from environment
    if 'edgar' in config:
        if 'user_agent_template' in config['edgar']:
            email = os.getenv('SEC_USER_AGENT_EMAIL')
            if not email:
                raise ValueError(
                    "SEC_USER_AGENT_EMAIL not found in .env file"
                )
            config['edgar']['user_agent'] = \
                config['edgar']['user_agent_template'].format(email=email)
            del config['edgar']['user_agent_template']

    return config
