import numpy as np
import torch
from rustshed import Result, Ok, Err


def detail_nda(arr: np.ndarray, type_name: str = 'ndarray') -> str:
    """np.ndarray 细节"""
    assert isinstance(arr, np.ndarray)
    min1 = np.min(arr)
    max1 = np.max(arr)
    return f'{type_name}[{arr.dtype}] shape={arr.shape} value=[{min1}~{max1}]'


def detail_tensor(arr: torch.Tensor) -> str:
    """torch.Tensor 细节"""
    assert isinstance(arr, torch.Tensor)
    return detail_nda(arr.cpu().numpy(), 'Tensor')


def detail(arr: np.ndarray | torch.Tensor) -> Result[str, str]:
    """显示类型细节"""
    if isinstance(arr, np.ndarray):
        return Ok(detail_nda(arr))
    elif isinstance(arr, torch.Tensor):
        return Ok(detail_tensor(arr))
    else:
        return Err(f'Unknown type: {type(arr)}')


def trace_arr(title: str, arr: np.ndarray | torch.Tensor) -> None:
    """显示类型细节"""

    s = detail(arr).unwrap()
    print(f'[{title}]: {s}')


def test_trace() -> None:
    print('')
    arr1 = np.zeros((4, 4))
    trace_arr('arr1', arr1)

    arr2 = torch.ones((4, 4))
    trace_arr('arr2', arr2)
