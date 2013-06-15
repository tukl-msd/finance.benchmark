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

tag = "v0.4"

if os.environ.get("GIT_USE_LOCAL", None) != '1':
    repo = "https+webdav://ekstera.eit.uni-kl.de/bazaar/development/common/buildsys/"
else:
    repo_root = os.environ.get("GIT_COMMON_ROOT")
    print(repo_root)
    repo = repo_root + "/buildsys"
    print(repo)

os.system("git clone " + repo + " buildsys")
os.chdir("buildsys")
os.system("git checkout " + tag)

