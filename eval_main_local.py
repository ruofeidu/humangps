# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A evaluation framework using distributed strategy."""
import os

from absl import app
from absl import flags
import gin.tf

from google3.vr.perception.deepholodeck.human_correspondence import train_eval_lib_local

flags.DEFINE_enum('mode', None, ['cpu', 'gpu'],
                  'Distributed strategy approach.')
flags.DEFINE_string('base_folder', None, 'Path to checkpoints/summaries.')
flags.DEFINE_string('job_name', '', 'Name of the job.')
flags.DEFINE_multi_string('gin_bindings', None, 'Gin parameter bindings.')
flags.DEFINE_multi_string('gin_configs', None, 'Gin config files.')

FLAGS = flags.FLAGS


def main(argv):
  del argv  # Unused.

  gin.parse_config_files_and_bindings(
      config_files=FLAGS.gin_configs,
      bindings=FLAGS.gin_bindings,
      skip_unknown=True)

  base_folder = FLAGS.base_folder
  train_base_folder = os.path.join(base_folder, 'train')
  eval_base_folder = os.path.join(base_folder, FLAGS.job_name)

  train_eval_lib_local.eval_pipeline(
      eval_mode=FLAGS.mode,
      dataset_params=gin.REQUIRED,
      train_base_folder=train_base_folder,
      eval_base_folder=eval_base_folder,
      batch_size=gin.REQUIRED,
      eval_name=FLAGS.job_name)


if __name__ == '__main__':
  flags.mark_flag_as_required('mode')
  flags.mark_flag_as_required('base_folder')
  app.run(main)
