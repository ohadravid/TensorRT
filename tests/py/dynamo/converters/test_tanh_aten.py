import torch
import torch.nn as nn
from torch.testing._internal.common_utils import run_tests
from harness import DispatchTestCase
from torch_tensorrt import Input


class TestTanhConverter(DispatchTestCase):
    def test_tanh(self):
        class TestModule(nn.Module):
            def forward(self, x):
                return nn.functional.tanh(x)

        inputs = [torch.randn(1, 10)]
        self.run_test(TestModule(), inputs, expected_ops={torch.ops.aten.tanh.default})

    def test_tanh_with_dynamic_shape(self):
        class TestModule(nn.Module):
            def forward(self, x):
                return nn.functional.tanh(x)

        input_specs = [
            Input(
                shape=(-1, -1, -1),
                dtype=torch.float32,
                shape_ranges=[((1, 1, 1), (1, 2, 3), (3, 3, 3))],
            ),
        ]
        self.run_test_with_dynamic_shape(
            TestModule(), input_specs, expected_ops={torch.ops.aten.tanh.default}
        )

    def test_tanh_with_dynamic_shape_four_dimensions(self):
        class TestModule(nn.Module):
            def forward(self, x):
                return nn.functional.tanh(x)

        input_specs = [
            Input(
                shape=(-1, -1, -1, -1),
                dtype=torch.float32,
                shape_ranges=[((1, 1, 1, 5), (1, 2, 3, 5), (3, 3, 3, 5))],
            ),
        ]

        self.run_test_with_dynamic_shape(
            TestModule(), input_specs, expected_ops={torch.ops.aten.tanh.default}
        )


if __name__ == "__main__":
    run_tests()