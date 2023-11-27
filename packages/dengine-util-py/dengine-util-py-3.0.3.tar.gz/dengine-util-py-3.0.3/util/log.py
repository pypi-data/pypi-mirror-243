import logging
import re
from logging.handlers import TimedRotatingFileHandler

from util.path import get_project_dir

# 设置日志文件的最大大小（可选）
max_file = 1024 * 1024 * 1024 * 1
# 最大备份小时
backup_count = 24 * 30

ext_match = r"^\d{10}$"
suffix = '%Y%m%d%H'

# hander = TimedRotatingFileHandler(filename=get_project_dir() + "/log/all.log", when="H", interval=1,
#                                   backupCount=backup_count)
# hander.suffix = suffix
# hander.extMatch = re.compile(ext_match, re.ASCII)

hander = TimedRotatingFileHandler(filename=get_project_dir() + "/log/public.log", when="H", interval=1,
                                            backupCount=backup_count)
hander.suffix = suffix
hander.extMatch = re.compile(ext_match, re.ASCII)

# 配置日志

# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(levelname)s][%(asctime)s.%(msecs)d][%(filename)s:%(lineno)d] _triton-inference-server||%(message)s",
#     handlers=[
#         hander
#         # logging.StreamHandler() 输出日志到标准输出
#     ],
#     datefmt='%Y-%m-%dT%H:%M:%S',
# )
#
# # 创建日志记录器
# logger = logging.getLogger(__name__)

# 配置Public日志

logging.basicConfig(
    level=logging.INFO,
    format="[triton-inference-server||timestamp=%(asctime)s||%(message)s",
    handlers=[
        hander
        # logging.StreamHandler() 输出日志到标准输出
    ],
    datefmt='%Y-%m-%d %H:%M:%S',
)

# 创建Public日志记录器
# publiclogger = logging.getLogger("publicLog")
logger = logging.getLogger(__name__)



# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json

# triton_python_backend_utils is available in every Triton Python model. You
# need to use this module to create inference requests and responses. It also
# contains some utility functions for extracting information from model_config
# and converting Triton input/output types to numpy types.
import triton_python_backend_utils as pb_utils

import pandas as pd
from gluonts.dataset.pandas import PandasDataset
from gluonts.model.predictor import Predictor
from gluonts.evaluation.backtest import make_evaluation_predictions
import numpy as np
from util.log import publicLogger
from collections import defaultdict

class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to initialize any state associated with this model.

        Parameters
        ----------
        args : dict
          Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        self.model_config = model_config = json.loads(args["model_config"])

        # Get OUTPUT0 configuration
        output0_config = pb_utils.get_output_config_by_name(model_config, "OUTPUT0")

        # Convert Triton types to numpy types
        self.output0_dtype = pb_utils.triton_string_to_numpy(
            output0_config["data_type"]
        )

    def execute(self, requests):
        """`execute` MUST be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference request is made
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse

        Parameters
        ----------
        requests : list
          A list of pb_utils.InferenceRequest

        Returns
        -------
        list
          A list of pb_utils.InferenceResponse. The length of this list must
          be the same as `requests`
        """

        output0_dtype = self.output0_dtype

        responses = []

        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for request in requests:
            # Get INPUT0
            in_0 = pb_utils.get_input_tensor_by_name(request, "INPUT0")
            input_0_obj = (in_0.as_numpy())
            input_0_str = input_0_obj[0].decode('UTF-8')
            print(input_0_str, flush=True)
            input_0_dict = json.loads(input_0_str)
            print(input_0_dict["feature"])
            publiclogger.info("input_0_dict={}".format(input_0_dict))

            def format_feature(feature_data):
                for index, item in feature_data.items():
                    for key, value in item.items():
                        if key == "item_id":
                            feature_data[index][key] = int(value)
                        else:
                            feature_data[index][key] = float(value)
                return feature_data

            feature = format_feature(input_0_dict["feature"])
            print(feature)
            df = pd.DataFrame.from_dict(feature, orient='index')
            test_dataset = PandasDataset.from_long_dataframe(
                df,
                item_id="item_id",
                feat_dynamic_real=["payuv_grow_rate", "courier_grow_rate", 'precip', 'precip_type'],
            )
            pt = Path("/home/xiaoju/model_52050500")
            predictor_deserialized = Predictor.deserialize(pt)
            forcast_it, ts_it = make_evaluation_predictions(
                dataset=test_dataset,
                predictor=predictor_deserialized,
                num_samples=500,
            )
            forcast = list(forcast_it)
            avg = np.mean(forcast[0].samples, axis=0)
            var = np.var(forcast[0].samples, axis=0)

            print(avg, flush=True)
            # Create output tensors. You need pb_utils.Tensor
            # objects to create pb_utils.InferenceResponse.
            out_tensor_0 = pb_utils.Tensor("OUTPUT0", avg.astype(output0_dtype))

            # Create InferenceResponse. You can set an error here in case
            # there was a problem with handling this inference request.
            # Below is an example of how you can set errors in inference
            # response:
            #
            # pb_utils.InferenceResponse(
            #    output_tensors=..., TritonError("An error occurred"))
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor_0]
            )
            responses.append(inference_response)

        # You should return a list of pb_utils.InferenceResponse. Length
        # of this list must match the length of `requests` list.
        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print("Cleaning up...")