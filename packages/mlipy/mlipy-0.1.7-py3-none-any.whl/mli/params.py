__all__ = [
    'LlamaCppParams',
    'CandleParams',
    'LLMParams',
]

from typing import TypedDict, Optional, Required


class LlamaCppParams(TypedDict):
    kind: Optional[str]                     # 'main'
    model: Optional[str]                    # model name
    model_id: Optional[str]                 # creator of model
    chatml: Optional[bool]                  # False
    n_predict: Optional[int]                # -1
    ctx_size: Optional[int]                 # 2048
    batch_size: Optional[int]               # 512
    temp: Optional[float]                   # 0.8
    n_gpu_layers: Optional[int]             # 0 (max usually 35)
    top_k: Optional[int]                    # 40
    top_p: Optional[float]                  # 0.9
    stop: Optional[list[str]]               # []
    prompt: Optional[str]                   # | prompt xor messages
    messages: Optional[list[dict]]          # /


class CandleParams(TypedDict):
    kind: Optional[str]                     # 'phi', 'stable-lm', 'llama', 'mistral', 'quantized'
    model: Optional[str]
    model_id: Optional[str]
    cpu: Optional[bool]                     # False
    temperature: Optional[int]              # 0.8
    top_p: Optional[int]                    # 0.9
    sample_len: Optional[int]               # 100
    quantized: Optional[bool]               # False
    use_flash_attn: Optional[bool]          # False
    stop: Optional[list[str]]               # []
    prompt: Optional[str]                   # | prompt xor messages
    messages: Optional[list[dict]]          # /


LLMParams: type = LlamaCppParams | CandleParams
