from configparser import ConfigParser
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent

config = ConfigParser()

for config_path in (
    Path('/config/skill_config.cfg'),
    PACKAGE_DIR.parent.parent / 'skill_config.cfg',
):
    if config_path.exists():
        config.read(config_path)
