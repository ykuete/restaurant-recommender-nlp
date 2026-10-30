---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:80000
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: for cheap and good mexican food, this is the place to go
  sentences:
  - 'Restaurant categories: Mexican, Restaurants'
  - 'Restaurant categories: Pizza, Food, Restaurants'
  - 'Restaurant categories: Delis, Bakeries, Food, Grocery, Restaurants'
- source_sentence: 'Wanda is terrific!

    Good bread great sandwiches'
  sentences:
  - 'Restaurant categories: Restaurants, Food, Bakeries, American (New)'
  - 'Restaurant categories: Comfort Food, Southern, Desserts, Food, Restaurants'
  - 'Restaurant categories: Mexican, Restaurants'
- source_sentence: Great house salad - same stuff in all chain restaurants
  sentences:
  - 'Restaurant categories: Restaurants, Seafood, American (New)'
  - 'Restaurant categories: Pizza, Restaurants'
  - 'Restaurant categories: Restaurants, American (New), Burgers'
- source_sentence: 'The Uovo.


    That''s all you need to know.  You''re welcome.'
  sentences:
  - 'Restaurant categories: Restaurants, Italian'
  - 'Restaurant categories: Mediterranean, Restaurants, Pizza, Italian'
  - 'Restaurant categories: Restaurants, Pizza'
- source_sentence: The best hole in the wall mexican joint in philly!  Super authentic
    and decently priced.
  sentences:
  - 'Restaurant categories: Italian, Pizza, Restaurants'
  - 'Restaurant categories: Restaurants, Mexican'
  - 'Restaurant categories: Pizza, Restaurants'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps inputs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41 -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({'module_input_name': 'sentence_embedding', 'module_output_name': 'sentence_embedding'})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'The best hole in the wall mexican joint in philly!  Super authentic and decently priced.',
    'Restaurant categories: Restaurants, Mexican',
    'Restaurant categories: Pizza, Restaurants',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.8656, 0.3199],
#         [0.8656, 1.0000, 0.4345],
#         [0.3199, 0.4345, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 80,000 training samples
* Columns: <code>anchor</code> and <code>positive</code>
* Approximate statistics based on the first 100 samples:
  |          | anchor                                                                               | positive                                                                          |
  |:---------|:-------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
  | type     | string                                                                               | string                                                                            |
  | modality | text                                                                                 | text                                                                              |
  | details  | <ul><li>min: 19 tokens</li><li>mean: 110.79 tokens</li><li>max: 256 tokens</li></ul> | <ul><li>min: 8 tokens</li><li>mean: 20.61 tokens</li><li>max: 58 tokens</li></ul> |
* Samples:
  | anchor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | positive                                                                                                                                                                  |
  |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>I'm not a religious woman but I do think this is what Heaven should be, if it's not already. My god where do I start?? RIght from the get-to this place has you mesmerized. The interior/decor is stunning, with gorgeous wallpaper behind the bar and cheeky black-and-white stripes on the ceiling. The wine list is decently sized, and organized so well. Try the orange wine! Then the food, oh my! We shared the cheese plate, Caesar salad, and the Valentino pizza. Hands down the best pizza I've ever eaten. But the best part, all the pizzas come with 3 dipping sauces. No more wasting those pizza butts!! I cannot wait to visit SB again and eat more of that insanely delicious pizza. Also, shout out to Jamie, our waitress (at least I think that was her name, sorry if I got that wrong). She was an absolute sweetheart and made our night even better!</code> | <code>Restaurant categories: American (Traditional), Restaurants, Wine Bars, Pizza, Cocktail Bars, Bars, Vegan, Nightlife</code>                                          |
  | <code>Miguel was a fabulous bartender!!!  Super nice and easy going.  The Mac and cheese was amazing!!  Thanks again for the great service.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | <code>Restaurant categories: Burgers, Steakhouses, American (New), Chicken Wings, Barbeque, American (Traditional), Sandwiches, Restaurants, Nightlife, Bars, Pubs</code> |
  | <code>I had the chicken mole.   It was excellent.    Service is a little slow but the food was worth it</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | <code>Restaurant categories: Mexican, Restaurants</code>                                                                                                                  |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `learning_rate`: 0.0003
- `warmup_steps`: 0.1

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 0.0003
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0.1
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1.0
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 8
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `dataloader_multiprocessing_context`: None
- `dataloader_in_order`: True
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}
- `warmup_ratio`: None

</details>

### Training Logs
<details><summary>Click to expand</summary>

| Epoch  | Step  | Training Loss |
|:------:|:-----:|:-------------:|
| 0.02   | 100   | 1.9741        |
| 0.04   | 200   | 1.7173        |
| 0.06   | 300   | 1.6461        |
| 0.08   | 400   | 1.5872        |
| 0.1    | 500   | 1.5963        |
| 0.12   | 600   | 1.5424        |
| 0.14   | 700   | 1.5747        |
| 0.16   | 800   | 1.5546        |
| 0.18   | 900   | 1.5519        |
| 0.2    | 1000  | 1.5300        |
| 0.22   | 1100  | 1.5587        |
| 0.24   | 1200  | 1.5924        |
| 0.26   | 1300  | 1.5493        |
| 0.28   | 1400  | 1.4720        |
| 0.3    | 1500  | 1.5756        |
| 0.32   | 1600  | 1.5178        |
| 0.34   | 1700  | 1.4966        |
| 0.36   | 1800  | 1.4700        |
| 0.38   | 1900  | 1.4778        |
| 0.4    | 2000  | 1.5303        |
| 0.42   | 2100  | 1.4864        |
| 0.44   | 2200  | 1.4798        |
| 0.46   | 2300  | 1.4662        |
| 0.48   | 2400  | 1.4739        |
| 0.5    | 2500  | 1.4250        |
| 0.52   | 2600  | 1.4449        |
| 0.54   | 2700  | 1.4339        |
| 0.56   | 2800  | 1.5183        |
| 0.58   | 2900  | 1.4211        |
| 0.6    | 3000  | 1.3720        |
| 0.62   | 3100  | 1.4067        |
| 0.64   | 3200  | 1.3919        |
| 0.66   | 3300  | 1.3741        |
| 0.68   | 3400  | 1.3783        |
| 0.7    | 3500  | 1.3713        |
| 0.72   | 3600  | 1.4111        |
| 0.74   | 3700  | 1.3623        |
| 0.76   | 3800  | 1.4261        |
| 0.78   | 3900  | 1.3301        |
| 0.8    | 4000  | 1.3655        |
| 0.82   | 4100  | 1.3628        |
| 0.84   | 4200  | 1.3558        |
| 0.86   | 4300  | 1.3404        |
| 0.88   | 4400  | 1.3566        |
| 0.9    | 4500  | 1.3707        |
| 0.92   | 4600  | 1.3376        |
| 0.94   | 4700  | 1.3029        |
| 0.96   | 4800  | 1.3281        |
| 0.98   | 4900  | 1.3359        |
| 1.0    | 5000  | 1.3180        |
| 1.02   | 5100  | 1.2316        |
| 1.04   | 5200  | 1.2025        |
| 1.06   | 5300  | 1.1041        |
| 1.08   | 5400  | 1.1509        |
| 1.1    | 5500  | 1.1536        |
| 1.12   | 5600  | 1.1445        |
| 1.1400 | 5700  | 1.1975        |
| 1.16   | 5800  | 1.2238        |
| 1.18   | 5900  | 1.1951        |
| 1.2    | 6000  | 1.1674        |
| 1.22   | 6100  | 1.1744        |
| 1.24   | 6200  | 1.1343        |
| 1.26   | 6300  | 1.1749        |
| 1.28   | 6400  | 1.1592        |
| 1.3    | 6500  | 1.1574        |
| 1.32   | 6600  | 1.1600        |
| 1.34   | 6700  | 1.1251        |
| 1.3600 | 6800  | 1.0853        |
| 1.38   | 6900  | 1.1534        |
| 1.4    | 7000  | 1.2044        |
| 1.42   | 7100  | 1.0945        |
| 1.44   | 7200  | 1.1740        |
| 1.46   | 7300  | 1.1808        |
| 1.48   | 7400  | 1.0775        |
| 1.5    | 7500  | 1.1479        |
| 1.52   | 7600  | 1.1644        |
| 1.54   | 7700  | 1.1595        |
| 1.56   | 7800  | 1.1406        |
| 1.58   | 7900  | 1.1259        |
| 1.6    | 8000  | 1.1448        |
| 1.62   | 8100  | 1.1614        |
| 1.6400 | 8200  | 1.1287        |
| 1.6600 | 8300  | 1.1280        |
| 1.6800 | 8400  | 1.1420        |
| 1.7    | 8500  | 1.0890        |
| 1.72   | 8600  | 1.1185        |
| 1.74   | 8700  | 1.1312        |
| 1.76   | 8800  | 1.1478        |
| 1.78   | 8900  | 1.0869        |
| 1.8    | 9000  | 1.0869        |
| 1.8200 | 9100  | 1.1531        |
| 1.8400 | 9200  | 1.1160        |
| 1.8600 | 9300  | 1.1345        |
| 1.88   | 9400  | 1.1246        |
| 1.9    | 9500  | 1.1604        |
| 1.92   | 9600  | 1.1334        |
| 1.94   | 9700  | 1.1130        |
| 1.96   | 9800  | 1.0807        |
| 1.98   | 9900  | 1.1008        |
| 2.0    | 10000 | 1.1121        |
| 2.02   | 10100 | 0.9399        |
| 2.04   | 10200 | 0.9504        |
| 2.06   | 10300 | 0.8969        |
| 2.08   | 10400 | 0.9179        |
| 2.1    | 10500 | 0.9163        |
| 2.12   | 10600 | 0.9306        |
| 2.14   | 10700 | 0.9376        |
| 2.16   | 10800 | 0.9394        |
| 2.18   | 10900 | 0.9195        |
| 2.2    | 11000 | 0.8663        |
| 2.22   | 11100 | 0.9378        |
| 2.24   | 11200 | 0.9301        |
| 2.26   | 11300 | 0.9094        |
| 2.2800 | 11400 | 0.9402        |
| 2.3    | 11500 | 0.9275        |
| 2.32   | 11600 | 0.9110        |
| 2.34   | 11700 | 0.9052        |
| 2.36   | 11800 | 0.8661        |
| 2.38   | 11900 | 0.9080        |
| 2.4    | 12000 | 0.9207        |
| 2.42   | 12100 | 0.8970        |
| 2.44   | 12200 | 0.8956        |
| 2.46   | 12300 | 0.9505        |
| 2.48   | 12400 | 0.9230        |
| 2.5    | 12500 | 0.8703        |
| 2.52   | 12600 | 0.8709        |
| 2.54   | 12700 | 0.9033        |
| 2.56   | 12800 | 0.8823        |
| 2.58   | 12900 | 0.8861        |
| 2.6    | 13000 | 0.9184        |
| 2.62   | 13100 | 0.9239        |
| 2.64   | 13200 | 0.9189        |
| 2.66   | 13300 | 0.8717        |
| 2.68   | 13400 | 0.8950        |
| 2.7    | 13500 | 0.8454        |
| 2.7200 | 13600 | 0.8464        |
| 2.74   | 13700 | 0.8982        |
| 2.76   | 13800 | 0.8992        |
| 2.7800 | 13900 | 0.8589        |
| 2.8    | 14000 | 0.8241        |
| 2.82   | 14100 | 0.8413        |
| 2.84   | 14200 | 0.8518        |
| 2.86   | 14300 | 0.8811        |
| 2.88   | 14400 | 0.8618        |
| 2.9    | 14500 | 0.8757        |
| 2.92   | 14600 | 0.8350        |
| 2.94   | 14700 | 0.8667        |
| 2.96   | 14800 | 0.8396        |
| 2.98   | 14900 | 0.8954        |
| 3.0    | 15000 | 0.8447        |

</details>

### Training Time
- **Training**: 1.1 hours

### Framework Versions
- Python: 3.14.7
- Sentence Transformers: 6.2.0
- Transformers: 5.21.0
- PyTorch: 2.10.0
- Accelerate: 1.15.0
- Datasets: 5.1.0
- Tokenizers: 0.23.3

## Additional Resources

- [Training and Finetuning Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-sentence-transformers): the end-to-end guide for training or finetuning Sentence Transformer models.
- [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka): variable-size embeddings that can be truncated with minimal quality loss.
- [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization): post-training compression of embedding vectors.
- [Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/multimodal-sentence-transformers): use text, image, audio, and video models through the same API.
- [Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-multimodal-sentence-transformers): train multimodal embedding models, with a Visual Document Retrieval walkthrough.

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->