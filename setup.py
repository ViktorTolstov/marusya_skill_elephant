#!/usr/bin/env python

import os

from setuptools import find_packages, setup

VERSION = os.getenv("CI_COMMIT_TAG")
if not VERSION:
    VERSION = "0.0.1"

# --- >
setup(
    name="skill-buy-elephant",
    version=VERSION,
    package_dir={'skill_buy_elephant': 'src/skill_buy_elephant'},
    python_requires=">=3.6.8",
    packages=find_packages(where='src', include=['skill_buy_elephant']),
    url="https://gitlab.com/mailru-voice/skill_buy_elephant",
    license="MIT",
    author="n.orgeev",
    author_email="n.orgeev@corp.mail.ru",
    description="skill-buy-elephant",
)

