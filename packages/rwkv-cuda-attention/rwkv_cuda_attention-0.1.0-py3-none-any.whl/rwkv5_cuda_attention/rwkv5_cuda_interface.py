import os
import torch
from torch.utils.cpp_extension import load

current_path = os.path.dirname(os.path.realpath(__file__))
cache_kernels = None

def load_rwkv5_cuda_kernel(HEAD_SIZE):
    global cache_kernels
    if cache_kernels is None:
        cache_kernels = load(
            name="rwkv5",
            sources=[
                os.path.join(current_path, "rwkv5_op.cpp"),
                os.path.join(current_path, "rwkv5.cu")
            ],
            verbose=True,
            extra_cuda_cflags=[
                "-res-usage",
                "--use_fast_math",
                "-O3",
                "-Xptxas -O3" if os.name != "nt" else "",
                "--extra-device-vectorization",
                f"-D_N_={HEAD_SIZE}"
            ]
        )
    return cache_kernels

def rwkv_linear_attention_v5_2_cuda(B, T, C, H, state, r, k, v, w, u):
    HEAD_SIZE = C // H
    cache_kernels = load_rwkv5_cuda_kernel(HEAD_SIZE)
    ctx.B = B
    ctx.T = T
    ctx.C = C
    ctx.H = H
    assert state.dtype == torch.float32
    assert w.dtype == torch.float32
    assert r.is_contiguous()
    assert k.is_contiguous()
    assert v.is_contiguous()
    assert w.is_contiguous()                            
    assert u.is_contiguous()                            
    assert state.is_contiguous()

    y = torch.empty((B, T, C), device=w.device, dtype=r.dtype, memory_format=torch.contiguous_format)
    if r.dtype == torch.bfloat16:
        cache_kernels.forward_bf16(B, T, C, H, state, r, k, v, w, u, y)
    elif r.dtype == torch.float16:
        cache_kernels.forward_fp16(B, T, C, H, state, r, k, v, w, u, y)
    elif r.dtype == torch.float32:
        cache_kernels.forward_fp32(B, T, C, H, state, r, k, v, w, u, y)
    return y, state

