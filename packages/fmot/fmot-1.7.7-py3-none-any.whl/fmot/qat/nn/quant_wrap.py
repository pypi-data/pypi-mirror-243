from functools import partial
import torch
from torch import Tensor
from .quantizers import DEFAULT_OBSERVERS, Quantizer
from ..annotated_tensors import tag_dim
from typing import *
from inspect import Signature, _empty
from collections import OrderedDict


def recursive_key(x: Union[Tensor, dict, list, tuple], key: str):
    if x is None:
        return []
    elif isinstance(x, Tensor):
        return [key]
    elif isinstance(x, dict):
        return sum(
            [recursive_key(v, f"{key}.{subkey}") for subkey, v in x.items()], start=[]
        )
    elif isinstance(x, (list, tuple)):
        return sum(
            [recursive_key(v, f"{key}.{idx}") for idx, v in enumerate(x)], start=[]
        )


class ListQuantCollection(torch.nn.Module):
    def __init__(self, bitwidth, observer=DEFAULT_OBSERVERS["default"], **kwargs):
        super().__init__()
        self.bitwidth = bitwidth
        self.obs_class = partial(observer, **kwargs)
        self.quantizers = torch.nn.ModuleList()
        self.kwargs = kwargs

    def add_quantizer(self, value: Union[list, dict, Tensor]):
        if value is None or isinstance(value, Tensor):
            self.quantizers.append(Quantizer(self.bitwidth, observer=self.obs_class))
        elif isinstance(value, list):
            self.quantizers.append(ListQuantCollection(self.bitwidth, self.obs_class))
        elif isinstance(value, dict):
            self.quantizers.append(DictQuantCollection(self.bitwidth, self.obs_class))
        else:
            raise ValueError(f"Unexpected type {type(value)}")

    def forward(self, x: list):
        outputs = []
        for i, x in enumerate(x):
            if i + 1 > len(self.quantizers):
                self.add_quantizer(x)
            outputs.append(self.quantizers[i](x))
        return outputs

    def all_quantizers(self):
        out = []
        for q in self.quantizers:
            if isinstance(q, Quantizer):
                out.append(q)
            else:
                out += q.all_quantizers()
        return out


class DictQuantCollection(torch.nn.Module):
    def __init__(self, bitwidth, observer=DEFAULT_OBSERVERS["default"], **kwargs):
        super().__init__()
        self.bitwidth = bitwidth
        self.obs_class = partial(observer, **kwargs)
        self.quantizers = torch.nn.ModuleDict()
        self.kwargs = kwargs

    def add_quantizer(self, key: str, value: Union[list, tuple, dict, Tensor]):
        if value is None or isinstance(value, Tensor):
            self.quantizers[key] = Quantizer(self.bitwidth, observer=self.obs_class)
        elif isinstance(value, dict):
            self.quantizers[key] = DictQuantCollection(self.bitwidth, self.obs_class)
        elif isinstance(value, (list, tuple)):
            self.quantizers[key] = ListQuantCollection(self.bitwidth, self.obs_class)
        else:
            raise ValueError(f"Unexpected type {type(value)}")

    def forward(self, x: dict):
        outputs = OrderedDict()
        for k, v in x.items():
            if k not in self.quantizers:
                self.add_quantizer(k, v)
            outputs[k] = self.quantizers[k](v)
        return outputs

    def all_quantizers(self):
        out = []
        for q in self.quantizers.values():
            if isinstance(q, Quantizer):
                out.append(q)
            else:
                out += q.all_quantizers()
        return out


class QuantCollection(torch.nn.Module):
    def __init__(
        self,
        bitwidth,
        signature: Optional[Signature] = None,
        observer=DEFAULT_OBSERVERS["default"],
        **kwargs,
    ):
        super().__init__()
        self.bitwidth = bitwidth
        self.obs_class = partial(observer, **kwargs)
        self.quantizers = torch.nn.ModuleList()
        self.signature = signature
        if signature is not None:
            for _ in range(len(signature.parameters)):
                self.add_quantizer()

        self.utilized_signature = []

    def add_quantizer(self):
        self.quantizers.append(Quantizer(self.bitwidth, observer=self.obs_class))

    def check_matches_signature(self, *args, **kwargs):
        if self.signature is not None:
            params = self.signature.parameters
            kwarg_keys = set(list(params.keys())[len(args) :])
            for k in kwargs:
                kwarg_keys.remove(k)

            # make sure remaining kwarg_keys have defaults
            for k in kwarg_keys:
                if params[k] == _empty:
                    raise ValueError(
                        f"Called model without specifying required arg {kwarg_keys}"
                    )

    def get_signature_name(self, key: Union[int, str]):
        if isinstance(key, int):
            return list(self.signature.parameters.keys())[key]
        else:
            return key

    def call_quantizer(self, idx: int, x: Union[Tensor, dict, list, tuple]):
        key = self.get_signature_name(idx)
        quantizer = self.quantizers[idx]

        if x is None:
            res = None

        elif isinstance(x, Tensor) and isinstance(quantizer, Quantizer):
            res = quantizer(x)
        elif isinstance(x, Tensor) and not isinstance(quantizer, Quantizer):
            quantizer = Quantizer(self.bitwidth, self.obs_class)
            self.quantizers[idx] = quantizer
            res = quantizer(x)

        elif isinstance(x, dict) and isinstance(quantizer, DictQuantCollection):
            res = quantizer(x)
        elif isinstance(x, dict) and not isinstance(quantizer, DictQuantCollection):
            quantizer = DictQuantCollection(self.bitwidth, self.obs_class)
            self.quantizers[idx] = quantizer
            res = quantizer(x)

        elif isinstance(x, (list, tuple)) and not isinstance(
            quantizer, ListQuantCollection
        ):
            quantizer = ListQuantCollection(self.bitwidth, self.obs_class)
            self.quantizers[idx] = quantizer
            res = quantizer(x)
        elif isinstance(x, (list, tuple)) and isinstance(
            quantizer, ListQuantCollection
        ):
            res = quantizer(x)

        else:
            raise ValueError(
                f"Incompatible types: quantizer: {type(quantizer)} x: {type(x)}"
            )

        sig = recursive_key(res, key)
        return res, sig

    def forward(self, *args, **kwargs):
        self.check_matches_signature(*args, **kwargs)
        new_args = []
        self.utilized_signature = []

        for i, arg in enumerate(args):
            if i + 1 > len(self.quantizers):
                if self.signature is None:
                    self.add_quantizer()
                else:
                    raise ValueError("Recieved an unexpected number of inputs")
            arg, sig = self.call_quantizer(i, arg)
            new_args.append(arg)
            self.utilized_signature += sig

        if len(kwargs) != 0 and self.signature is None:
            raise ValueError(
                f"Cannot call model with unknown signature using keyword arguments"
            )

        new_kwargs = {}
        for key, arg in kwargs.items():
            idx = list(self.signature.parameters.keys()).index(key)
            arg, sig = self.call_quantizer(idx, arg)
            new_kwargs[key] = arg
            self.utilized_signature += sig

        return new_args, new_kwargs

    def all_quantizers(self) -> List[Quantizer]:
        out = []
        for q in self.quantizers:
            if isinstance(q, Quantizer):
                out.append(q)
            elif isinstance(q, (DictQuantCollection, ListQuantCollection)):
                out += q.all_quantizers()
            else:
                raise ValueError(f"Unexpected type {type(q)} in self.quantizers")
        return out


class QuantWrapper(torch.nn.Module):
    def __init__(
        self,
        model,
        bitwidth,
        observer=DEFAULT_OBSERVERS["default"],
        signature: List[str] = None,
        dimensions=None,
        **kwargs,
    ):
        super().__init__()
        self.quantizers = QuantCollection(
            bitwidth, signature=signature, observer=observer, **kwargs
        )
        self.bitwidth = bitwidth
        self.model = model
        self.dimensions = dimensions
        self.signature = signature

    @tag_dim
    def forward(self, *args, **kwargs):
        args, kwargs = self.quantizers(*args, **kwargs)
        return self.model(*args, **kwargs)
