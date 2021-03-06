""" Copyright 2016-2022 by Bitmain Technologies Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
import subprocess
import sys
from ..common.base_compiler import Compiler

PY_COMAND = 'python'
if sys.version > '3':
  PY_COMAND = 'python3'


class CaffeCompiler(Compiler):
  """ Compile tf graphs into bmodels.
  """
  def check_init(self):
    assert self.platform == 'caffe'
    assert self.layout == 'NCHW'

  def generate_compiling_script(self, compile_info):
    proto = compile_info['model_info']['proto']
    weight = compile_info['model_info']['weight']
    outdir = os.path.join(self.folder, compile_info['context_dir'])
    outdir_ = outdir.split('/')
    ret = "import bmnetc as bm\n"
    ret = ret + "import os\n\n"
    ret = ret + "proto='{0}'\n".format(proto)
    ret = ret + "weight='{0}'\n".format(weight)
    ret = ret + "outdir='{0}'\n".format(compile_info['context_dir'])
    ret = ret + "target='{0}'\n".format(self.target)
    ret = ret + \
        "net_name='auto_caffe_{0}_{1}'\n\n".format(outdir_[-2], outdir_[-1])
    ret = ret + "bm.compile(proto, weight, outdir, target, " + \
                "net_name=net_name, dyn={0})\n\n".format(self.dynamic)
    ret = ret + "# os.remove('bm_multi_engine_stas_0.dat')\n\n"
    with open(os.path.join(self.folder, \
        'compile_to_{0}.py'.format(compile_info['context_dir'])), \
        'w+') as save_stream:
      save_stream.write(ret)

  def compile_model_using_bmcompiler(self, compile_info):
    ret = subprocess.call([PY_COMAND, \
                    'compile_to_{0}.py'.format(compile_info['context_dir'])], \
                    cwd=self.folder, close_fds=True)
    if ret != 0:
      raise RuntimeError("compile failed: {}".format\
            ('compile_to_{0}.py'.format(compile_info['context_dir'])))
