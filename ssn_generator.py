#!/usr/bin/env python
import sys
from pathlib import Path

# Add the project root to the path to allow running from anywhere
# and to simplify imports.
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ssn_generation.entrypoints import cli

if __name__ == '__main__':
    cli.main() 