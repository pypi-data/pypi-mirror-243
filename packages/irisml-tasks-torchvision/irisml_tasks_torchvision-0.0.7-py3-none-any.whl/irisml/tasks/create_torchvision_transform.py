import ast
import dataclasses
from typing import Callable, List
import torch.nn
import torchvision.transforms
import irisml.core


class Task(irisml.core.TaskBase):
    """Create transform objects in torchvision library.

    This task creates a transform object in torchvision library from string expressions.
    The expression can be a simple method name such as "RandomCrop" or a method call such as "RandomCrop((32, 32))".

    ToTensor is always appended to the end of the transform object.

    Example expressions:
    - "RandomCrop((32, 32))"
    - "Resize(224, 'InterpolationMode.BICUBIC')"

    Config:
        transforms ([str]): A list of transform descriptions.
    """
    VERSION = '0.1.2'

    @dataclasses.dataclass
    class Config:
        transforms: List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Outputs:
        transform: Callable

    class Transform:
        def __init__(self, transform_configs: List):
            transform_instances = []
            for method_name, args in transform_configs:
                transform_class = getattr(torchvision.transforms, method_name)
                transform_instances.append(transform_class(*args))
            transform_instances.append(torchvision.transforms.ToTensor())
            self._transform = torchvision.transforms.Compose(transform_instances)
            self._transform_configs = transform_configs

        def __call__(self, x):
            return self._transform(x)

        def __getstate__(self):
            return {'transform_configs': self._transform_configs}

        def __setstate__(self, state):
            self.__init__(**state)

    def execute(self, inputs):
        transform_configs = []
        for t in self.config.transforms:
            method_name, args = self._parse_transform(t)
            args = self._convert_known_param(args)
            if not hasattr(torchvision.transforms, method_name):
                raise ValueError(f"torchvision.transforms doesn't have {method_name}")

            transform_class = getattr(torchvision.transforms, method_name)
            if not issubclass(transform_class, torch.nn.Module):
                raise RuntimeError(f"{transform_class} has unexpected type.")

            transform_configs.append((method_name, args))

        transform = Task.Transform(transform_configs)
        return self.Outputs(transform)

    def dry_run(self, inputs):
        return self.execute(inputs)

    @staticmethod
    def _parse_transform(expr):
        parsed = ast.parse(expr)
        if len(parsed.body) != 1:
            raise ValueError(f"Transform description cannot have multiple expressions: {expr}")

        if isinstance(parsed.body[0].value, ast.Name):
            return parsed.body[0].value.id, []
        elif isinstance(parsed.body[0].value, ast.Call):
            method_name = parsed.body[0].value.func.id
            ast_args = parsed.body[0].value.args
            args = []
            for arg in ast_args:
                if isinstance(arg, ast.Tuple):
                    if not all(isinstance(a, ast.Constant) for a in arg.elts):
                        raise ValueError(f"Only simple types are supported: {ast.dump(arg)}")
                    args.append(tuple(a.value for a in arg.elts))
                elif isinstance(arg, ast.Constant):
                    args.append(arg.value)
                else:
                    raise ValueError(f"Only simple types such as a number, a string, a tuple can be used as arguments: {ast.dump(arg)}")

            return method_name, args
        else:
            raise ValueError(f"Unexpected transform description: {ast.dump(parsed)}")

    @staticmethod
    def _convert_known_param(args):
        new_args = []
        for a in args:
            if a == 'InterpolationMode.NEAREST':
                a = torchvision.transforms.InterpolationMode.NEAREST
            elif a == 'InterpolationMode.NEAREST_EXACT':
                a = torchvision.transforms.InterpolationMode.NEAREST_EXACT
            elif a == 'InterpolationMode.BILINEAR':
                a = torchvision.transforms.InterpolationMode.BILINEAR
            elif a == 'InterpolationMode.BICUBIC':
                a = torchvision.transforms.InterpolationMode.BICUBIC
            new_args.append(a)
        return new_args
