import math

import torch


def apply_rotary_embeddings(x, max_seq_len=None, dim=-1):
    """
    Apply rotary embeddings to the input tensors x.

    Args:
    - x (torch.Tensor): The input tensors of shape (batch_size, seq_len, dim).
    - max_seq_len (int): The maximum sequence length for positional embeddings.
    - dim (int): The dimension of the x tensors that contains the embeddings.

    Returns:
    - torch.Tensor: The tensors with rotary embeddings applied.
    """
    dim = x.shape[dim]
    if len(x.shape) == 2:
        x = x.unsqueeze(0)
    assert dim % 2 == 0, "Rotary embeddings require even-dimensional space."

    # Create the positional embeddings matrix
    max_seq_len = max_seq_len if max_seq_len is not None else x.size(0)
    position_indices = torch.arange(0, max_seq_len, dtype=torch.float32).unsqueeze(1)
    indices = torch.arange(0, dim // 2, dtype=torch.float32).unsqueeze(0)
    freqs = torch.exp(-math.log(10000) * indices / (dim // 2))
    angles = position_indices * freqs * (2 * math.pi)

    # Create the sines and cosines for the embeddings
    sine = torch.sin(angles)
    cosine = torch.cos(angles)

    # Repeat and interleave sine and cosine along the sequence length and embedding dimensions
    sine = sine.repeat_interleave(2, dim=1)
    cosine = cosine.repeat_interleave(2, dim=1)

    # Expand the embeddings to match the input tensors's batch size
    sine = sine.unsqueeze(0).expand(x.size(0), -1, -1)
    cosine = cosine.unsqueeze(0).expand(x.size(0), -1, -1)

    # Rotary position encoding formula: x' = x * cos + (rotate_left(x) * sin)
    x_rotated = (x * cosine[:, :x.size(1), :] + torch.roll(x, shifts=1, dims=-1) * sine[:, :x.size(1), :])

    return x_rotated

#
# # Generate some data (using the previously defined apply_rotary_embeddings function)
# batch_size = 5
# seq_len = 50
# embeding_len = 512  # Embedding dimension must be even
# max_seq_len = 512
#
# # Assume embeddings_tensor is the tensors you obtained from OpenAI with shape [batch, seq_len, num_features]
# embeddings_tensor = torch.rand(batch_size, seq_len, embeding_len)
#
# # Apply rotary embeddings
# rotary_embeddings_tensor = apply_rotary_embeddings(embeddings_tensor, max_seq_len)
#
# print(rotary_embeddings_tensor.shape)  # Should be the same shape as embeddings_tensor
# import matplotlib.pyplot as plt
# import seaborn as sns
# import torch
# import numpy as np
#
#
# # Function to calculate pairwise cosine similarity
# def cosine_similarity_matrix(embeddings):
#     similarities = torch.nn.functional.cosine_similarity(
#         embeddings.unsqueeze(1), embeddings.unsqueeze(0), dim=-1)
#
#     return similarities
#
# # Calculate cosine similarities
# original_cosine_similarities = cosine_similarity_matrix(embeddings_tensor[0]).detach().numpy()
# rotated_cosine_similarities = cosine_similarity_matrix(rotary_embeddings_tensor[0]).detach().numpy()
#
# # Function to plot cosine similarity heatmap
# def plot_cosine_similarity_heatmap(data, ax, title):
#     sns.heatmap(data, cmap='viridis', ax=ax)
#     ax.set_title(title)
#     ax.set_xlabel('Position')
#     ax.set_ylabel('Position')
#
# # Create subplots: 3 rows, 1 column
# fig, axes = plt.subplots(3, 1, figsize=(10, 15))
#
# # Plot the mean cosine similarity as a function of relative distance on the first row
# mean_original_cosine = np.mean(original_cosine_similarities, axis=0)
# mean_rotated_cosine = np.mean(rotated_cosine_similarities, axis=0)
# axes[0].plot(mean_original_cosine, label='Original', color='blue')
# axes[0].plot(mean_rotated_cosine, label='Rotary', color='orange')
# axes[0].set_title('Mean Cosine Similarity by Position')
# axes[0].set_xlabel('Position')
# axes[0].set_ylabel('Mean Cosine Similarity')
# axes[0].legend()
#
# # Plot the original cosine similarity heatmap on the second row
# plot_cosine_similarity_heatmap(original_cosine_similarities, axes[1], 'Original Cosine Similarity')
#
# # Plot the rotated cosine similarity heatmap on the third row
# plot_cosine_similarity_heatmap(rotated_cosine_similarities, axes[2], 'Rotary Cosine Similarity')
#
# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
#
