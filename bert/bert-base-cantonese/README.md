---
language:
- yue
license: cc-by-4.0
tags:
- generated_from_trainer
base_model: bert-base-chinese
pipeline_tag: fill-mask
widget:
- text: 香港原本[MASK]一個人煙稀少嘅漁港。
  example_title: 係
model-index:
- name: bert-base-cantonese
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# bert-base-cantonese

This model is a continue pre-train version of bert-base-chinese on Cantonese Common Crawl dataset with 198m tokens.

## Model description

This model has extended 500 more Chinese characters which very common in Cantonese, such as 冧, 噉, 麪, 笪, 冚, 乸 etc.

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 24
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 8
- total_train_batch_size: 192
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 1.0

### Training results



### Framework versions

- Transformers 4.35.0.dev0
- Pytorch 2.1.1+cu121
- Datasets 2.14.6
- Tokenizers 0.14.1
