# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that handle code documentation generation"""

from __future__ import annotations

import subprocess
import sys
from pprint import  pprint

from .helper_base import cl_helper_base


class cl_install_deps(cl_helper_base):
    """dependencies installer implementation class"""


    @classmethod
    def do_job(cls) -> None:
        """helper job method implementation"""
        deps=[]
        opt_deps={}
        if 'project' in cls.pyproject:
            prj = cls.pyproject["project"]
            if 'dependencies' in prj:
                deps = prj['dependencies']
            if 'optional-dependencies'in prj:
                opt_deps = prj['optional-dependencies']
        if len(deps)>0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + deps)
        for opt_key in opt_deps.keys():
            if len(opt_deps[opt_key]) > 0:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + opt_deps[opt_key])
