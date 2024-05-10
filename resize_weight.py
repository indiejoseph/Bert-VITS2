import torch
import torch.nn as nn
from text.symbols import symbols, num_tones, num_languages
import argparse
import math


def resize_embedding_layer(weight, new_size):
    old_vocab_size = weight.size(0)
    if new_size < old_vocab_size:
        return weight[:new_size, :]
    elif new_size == old_vocab_size:
        return weight
    else:
        new_weight = weight.new_zeros(
            new_size - old_vocab_size, weight.size(1))
        embedding_dim = weight.size(1)
        avg_weight = weight.mean(dim=0, keepdim=True)
        noise_weight = torch.empty_like(new_weight)
        noise_weight.normal_(mean=0, std=(1.0 / math.sqrt(embedding_dim)))
        new_weight = avg_weight + noise_weight

        return torch.cat([weight, new_weight], dim=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weight",
        type=str,
        help="path to original weight file",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="path to output weight file",
    )
    args, _ = parser.parse_known_args()

    checkpoint_dict = torch.load(args.weight, map_location="cpu")
    checkpoint_dict['model']['enc_p.emb.weight'] = resize_embedding_layer(
        checkpoint_dict['model']['enc_p.emb.weight'], len(symbols))
    checkpoint_dict['model']['enc_p.tone_emb.weight'] = resize_embedding_layer(
        checkpoint_dict['model']['enc_p.tone_emb.weight'], num_tones)
    checkpoint_dict['model']['enc_p.language_emb.weight'] = resize_embedding_layer(
        checkpoint_dict['model']['enc_p.language_emb.weight'], num_languages)

    torch.save(checkpoint_dict, args.output)

    print("Resize weight file done!")
