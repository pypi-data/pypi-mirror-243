# -*- coding: utf-8 -*-

import pywph as pw
import torch
import numpy as np

M, N = 256, 256
J = 7
L = 8
dn = 2

device = 0

# Load data and convert it to a torch.tensor (mind the single precision)
data = np.load('data/I_1.npy')[::2, ::2]
data_torch = torch.from_numpy(data.astype(np.float32)).to(device)

# Record the operations performed on data_torch
data_torch.requires_grad = True

wph_op = pw.WPHOp(M, N, J, L=L, dn=dn, device=device)

# Compute the coefficients and the gradient of a final loss by accumulating the gradients of the chunks of the loss
data_torch, nb_chunks = wph_op.preconfigure(data_torch) # Divide the computation into chunks

max_len = 0
for i in range(len(wph_op.wph_moments_chunk_list)):
    if wph_op.wph_moments_chunk_list[i].shape[0] > max_len:
        max_len = wph_op.wph_moments_chunk_list[i].shape[0]
print(f"max_len = {max_len}")

torch.cuda.empty_cache()

cov_chunk = wph_op.wph_moments_chunk_list[18]
cov_indices = wph_op.wph_moments_indices[cov_chunk]

curr_psi_1_indices = wph_op._psi_1_indices[cov_chunk]
curr_psi_2_indices = wph_op._psi_2_indices[cov_chunk]

xpsi1_k1 = torch.index_select(wph_op._tmp_data_wt_mod, -3, curr_psi_1_indices)
xpsi2_k2 = torch.index_select(wph_op._tmp_data_wt, -3, curr_psi_2_indices)

# xpsi1_k1 = wph_op._tmp_data_wt_mod[..., curr_psi_1_indices, :, :]
# xpsi2_k2 = wph_op._tmp_data_wt[..., curr_psi_2_indices, :, :]

cov = torch.mean(xpsi1_k1 * xpsi2_k2, (-1, -2))
l = torch.absolute(cov).sum()
l.backward()

#coeffs_chunk = wph_op(data_torch, 18)

coeffs = []
for i in range(nb_chunks):
    print(f"{i}/{nb_chunks}")
    coeffs_chunk = wph_op(data_torch, i)
    loss_chunk = (torch.absolute(coeffs_chunk) ** 2).sum()
    loss_chunk.backward(retain_graph=True)
    coeffs.append(coeffs_chunk.detach().cpu())
    del coeffs_chunk, loss_chunk # To free GPU memory
coeffs = torch.cat(coeffs, -1)
grad = data_torch.grad

print(grad)
