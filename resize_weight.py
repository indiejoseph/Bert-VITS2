import torch
import torch.nn as nn
from text.symbols import symbols, num_tones, num_languages
import argparse


def resize_embedding_layer(weight, new_vocab_size):
    old_vocab_size = weight.size(0)
    if new_vocab_size < old_vocab_size:
        return weight[:new_vocab_size, :]
    elif new_vocab_size == old_vocab_size:
        return weight
    else:
        new_weight = weight.new_zeros(
            new_vocab_size - old_vocab_size, weight.size(1))
        hidden_channels = weight.size(1)
        new_weight = nn.init.normal_(new_weight, 0.0, hidden_channels**-0.5)

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
