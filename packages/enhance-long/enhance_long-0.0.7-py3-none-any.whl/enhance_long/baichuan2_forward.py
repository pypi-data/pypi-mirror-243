# !usr/bin/env python
# -*- coding:utf-8 -*-

'''
 Description  : 
 Version      : 1.0
 Author       : MrYXJ
 Mail         : code_job@163.com
 Github       : https://github.com/MrYxJ
 Date         : 2023-11-10 01:26:27
 LastEditTime : 2023-11-10 01:28:55
 FilePath     : \\EnhanceLong\\enhance_long\\baichuan2_forward.py
 Copyright (C) 2023 mryxj. All rights reserved.
'''
import torch
import math

from typing import Optional, Tuple
from torch.nn import F
from transformers.models.llama.modeling_llama import apply_rotary_pos_emb

try:
    from xformers import ops as xops
except ImportError:
    xops = None
    # logger.warning(
    #     "Xformers is not installed correctly. If you want to use memory_efficient_attention to accelerate training use the following command to install Xformers\npip install xformers."
    # )

BAICHUAN_MAX_LENGTH = 4 * 1024

def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        use_attn_logn: bool = True
) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
    bsz, q_len, _ = hidden_states.size()

    proj = self.W_pack(hidden_states)
    proj = proj.unflatten(-1, (3, self.hidden_size)).unsqueeze(0).transpose(0, -2).squeeze(-2)
    query_states = proj[0].view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
    key_states = proj[1].view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
    value_states = proj[2].view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)

    kv_seq_len = key_states.shape[-2]
    if past_key_value is not None:
        kv_seq_len += past_key_value[0].shape[-2]
    cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, position_ids)
    # [bsz, nh, t, hd]
    
    if use_attn_logn:
        logn_list = [
        math.log(i, BAICHUAN_MAX_LENGTH) if i > BAICHUAN_MAX_LENGTH else 1
                for i in range(1, q_len+1)
        ]
        logn_tensor = torch.tensor(logn_list)[None, None, :, None].type_as(query_states).to(query_states.device)
        #self.register_buffer("logn_tensor", logn_tensor, persistent=False)
        query_states = query_states * logn_tensor.expand_as(query_states)

    if past_key_value is not None:
        # reuse k, v, self_attention
        key_states = torch.cat([past_key_value[0], key_states], dim=2)
        value_states = torch.cat([past_key_value[1], value_states], dim=2)

    past_key_value = (key_states, value_states) if use_cache else None
    if xops is not None and self.training:
        attn_weights = None
        query_states = query_states.transpose(1, 2)
        key_states = key_states.transpose(1, 2)
        value_states = value_states.transpose(1, 2)
        attn_output = xops.memory_efficient_attention(
            query_states, key_states, value_states, attn_bias=xops.LowerTriangularMask()
        )
    else:
        with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=True, enable_mem_efficient=True):
            attn_output = F.scaled_dot_product_attention(query_states, key_states, value_states, attn_mask = attention_mask)
        attn_output = attn_output.transpose(1, 2)
    attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)
    attn_output = self.o_proj(attn_output)

    if not output_attentions:
        attn_weights = None

    return attn_output, attn_weights, past_key_value