# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import textwrap

from apibase import APIBase

obj = APIBase("torch.autograd.function.FunctionCtx.set_materialize_grads")


def test_case_1():
    pytorch_code = textwrap.dedent(
        """
        import torch
        from torch.autograd import Function

        # Inherit from Function
        class cus_tanh(Function):
            @staticmethod
            def forward(ctx, x):
                ctx.set_materialize_grads(False)
                return x+x+x, x+x

            @staticmethod
            def backward(ctx, grad, grad2):
                assert grad2==None
                return grad

        x = torch.ones([1], dtype=torch.float64)
        x.requires_grad = True
        cus_tanh.apply(x)[0].backward()

        result = x.grad
        result.requires_grad = False
        """
    )
    obj.run(pytorch_code, ["result"])
