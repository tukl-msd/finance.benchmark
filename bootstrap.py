#!/usr/bin/env python
#
# Copyright (C) 2013 University of Kaiserslautern
# Microelectronic Systems Design Research Group
#
# This file is part of the financial mathematics research project
# de.uni-kl.eit.ems.finance
# 
# Christian Brugger (brugger@eit.uni-kl.de)
# 29. January 2013
#

import os

tag = "v0.3"

if os.environ.get("BZR_USE_LOCAL", None) != '1':
    repo = "https+webdav://ekstera.eit.uni-kl.de/bazaar/development/common/buildsys/"
else:
    repo_root = os.environ.get("BZR_COMMON_ROOT")
    print(repo_root)
    repo = os.path.join(repo_root, "buildsys")
    print(repo)

os.system("bzr branch " + repo + " buildsys -r " + tag)

