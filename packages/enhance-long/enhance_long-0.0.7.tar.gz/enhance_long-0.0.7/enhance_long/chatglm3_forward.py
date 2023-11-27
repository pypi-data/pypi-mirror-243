# !usr/bin/env python
# -*- coding:utf-8 -*-

'''
 Description  : 
 Version      : 1.0
 Author       : MrYXJ
 Github       : https://github.com/MrYxJ
 Date         : 2023-11-11 15:16:27
 LastEditTime : 2023-11-11 15:51:31
 Copyright (C) 2023 mryxj. All rights reserved.
'''
CHATGLM3_MAX_LENGTH = 8 * 1024

def forward(
        self, hidden_states, attention_mask, rotary_pos_emb, kv_cache=None, use_cache=True
):
    # hidden_states: [sq, b, h]

    # =================================================
    # Pre-allocate memory for key-values for inference.
    # =================================================
    # =====================
    # Query, Key, and Value
    # =====================
    
    # Attention heads [sq, b, h] --> [sq, b, (np * 3 * hn)]
    mixed_x_layer = self.query_key_value(hidden_states)

    if self.multi_query_attention:
        (query_layer, key_layer, value_layer) = mixed_x_layer.split(
            [
                self.num_attention_heads_per_partition * self.hidden_size_per_attention_head,
                self.num_multi_query_groups_per_partition * self.hidden_size_per_attention_head,
                self.num_multi_query_groups_per_partition * self.hidden_size_per_attention_head,
            ],
            dim=-1,
        )
        query_layer = query_layer.view(
            query_layer.size()[:-1] + (self.num_attention_heads_per_partition, self.hidden_size_per_attention_head)
        )
        key_layer = key_layer.view(
            key_layer.size()[:-1] + (self.num_multi_query_groups_per_partition, self.hidden_size_per_attention_head)
        )
        value_layer = value_layer.view(
            value_layer.size()[:-1]
            + (self.num_multi_query_groups_per_partition, self.hidden_size_per_attention_head)
        )
    else:
        new_tensor_shape = mixed_x_layer.size()[:-1] + \
                            (self.num_attention_heads_per_partition,
                            3 * self.hidden_size_per_attention_head)
        mixed_x_layer = mixed_x_layer.view(*new_tensor_shape)

        # [sq, b, np, 3 * hn] --> 3 [sq, b, np, hn]
        (query_layer, key_layer, value_layer) = split_tensor_along_last_dim(mixed_x_layer, 3)

    # apply relative positional encoding (rotary embedding)
    if rotary_pos_emb is not None:
        query_layer = apply_rotary_pos_emb(query_layer, rotary_pos_emb)
        key_layer = apply_rotary_pos_emb(key_layer, rotary_pos_emb)
    
    sel_len = query_layer.size()[0]
    logn_list = [
        math.log(i, CHATGLM3_MAX_LENGTH) if i > CHATGLM3_MAX_LENGTH else 1
        for i in range(1, sel_len+1)
    ]
    logn_tensor = torch.tensor(logn_list)[:, None, None, None].type_as(query_layer).to(query_layer.device)
    #self.register_buffer("logn_tensor", logn_tensor, persistent=False)
    query_layer = query_layer * logn_tensor.expand_as(query_layer)
    
    # adjust key and value for inference
    if kv_cache is not None:
        cache_k, cache_v = kv_cache
        key_layer = torch.cat((cache_k, key_layer), dim=0)
        value_layer = torch.cat((cache_v, value_layer), dim=0)
    if use_cache:
        kv_cache = (key_layer, value_layer)
    else:
        kv_cache = None
    
    if self.multi_query_attention:
        key_layer = key_layer.unsqueeze(-2)
        key_layer = key_layer.expand(
            -1, -1, -1, self.num_attention_heads_per_partition // self.num_multi_query_groups_per_partition, -1
        )
        key_layer = key_layer.contiguous().view(
            key_layer.size()[:2] + (self.num_attention_heads_per_partition, self.hidden_size_per_attention_head)
        )
        value_layer = value_layer.unsqueeze(-2)
        value_layer = value_layer.expand(
            -1, -1, -1, self.num_attention_heads_per_partition // self.num_multi_query_groups_per_partition, -1
        )
        value_layer = value_layer.contiguous().view(
            value_layer.size()[:2] + (self.num_attention_heads_per_partition, self.hidden_size_per_attention_head)
        )

    # ==================================
    # core attention computation
    # ==================================

    context_layer = self.core_attention(query_layer, key_layer, value_layer, attention_mask)

    # =================
    # Output. [sq, b, h]
    # =================

    output = self.dense(context_layer)

    return output, kv_cache