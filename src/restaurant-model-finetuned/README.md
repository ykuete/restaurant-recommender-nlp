---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:80000
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L12-v2
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

# SentenceTransformer based on sentence-transformers/all-MiniLM-L12-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2). It maps inputs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2) <!-- at revision a50ef00143b4d5391434df20ae11632588ac25be -->
- **Maximum Sequence Length:** 128 tokens
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
# tensor([[1.0000, 0.6055, 0.1623],
#         [0.6055, 1.0000, 0.2966],
#         [0.1623, 0.2966, 1.0000]])
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
  |          | anchor                                                                              | positive                                                                          |
  |:---------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
  | type     | string                                                                              | string                                                                            |
  | modality | text                                                                                | text                                                                              |
  | details  | <ul><li>min: 19 tokens</li><li>mean: 85.98 tokens</li><li>max: 128 tokens</li></ul> | <ul><li>min: 8 tokens</li><li>mean: 20.61 tokens</li><li>max: 58 tokens</li></ul> |
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

- `per_device_train_batch_size`: 64
- `learning_rate`: 0.0001
- `warmup_steps`: 0.1

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 64
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 0.0001
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

| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 0.02   | 25   | 3.4024        |
| 0.04   | 50   | 3.1024        |
| 0.06   | 75   | 3.0067        |
| 0.08   | 100  | 2.8329        |
| 0.1    | 125  | 2.8462        |
| 0.12   | 150  | 2.7329        |
| 0.14   | 175  | 2.7015        |
| 0.16   | 200  | 2.6413        |
| 0.18   | 225  | 2.6594        |
| 0.2    | 250  | 2.5631        |
| 0.22   | 275  | 2.6281        |
| 0.24   | 300  | 2.5733        |
| 0.26   | 325  | 2.5619        |
| 0.28   | 350  | 2.4783        |
| 0.3    | 375  | 2.5449        |
| 0.32   | 400  | 2.4977        |
| 0.34   | 425  | 2.4947        |
| 0.36   | 450  | 2.3976        |
| 0.38   | 475  | 2.3590        |
| 0.4    | 500  | 2.4398        |
| 0.42   | 525  | 2.4968        |
| 0.44   | 550  | 2.4493        |
| 0.46   | 575  | 2.4472        |
| 0.48   | 600  | 2.4170        |
| 0.5    | 625  | 2.3904        |
| 0.52   | 650  | 2.3715        |
| 0.54   | 675  | 2.3788        |
| 0.56   | 700  | 2.4151        |
| 0.58   | 725  | 2.3315        |
| 0.6    | 750  | 2.2804        |
| 0.62   | 775  | 2.3113        |
| 0.64   | 800  | 2.3612        |
| 0.66   | 825  | 2.3402        |
| 0.68   | 850  | 2.3219        |
| 0.7    | 875  | 2.3198        |
| 0.72   | 900  | 2.3304        |
| 0.74   | 925  | 2.3018        |
| 0.76   | 950  | 2.3670        |
| 0.78   | 975  | 2.2322        |
| 0.8    | 1000 | 2.2646        |
| 0.82   | 1025 | 2.3064        |
| 0.84   | 1050 | 2.2560        |
| 0.86   | 1075 | 2.2377        |
| 0.88   | 1100 | 2.2932        |
| 0.9    | 1125 | 2.2988        |
| 0.92   | 1150 | 2.2878        |
| 0.94   | 1175 | 2.2407        |
| 0.96   | 1200 | 2.2642        |
| 0.98   | 1225 | 2.2775        |
| 1.0    | 1250 | 2.2520        |
| 1.02   | 1275 | 2.0788        |
| 1.04   | 1300 | 2.0590        |
| 1.06   | 1325 | 1.9675        |
| 1.08   | 1350 | 2.0198        |
| 1.1    | 1375 | 2.0357        |
| 1.12   | 1400 | 2.0023        |
| 1.1400 | 1425 | 2.0342        |
| 1.16   | 1450 | 2.0831        |
| 1.18   | 1475 | 2.0534        |
| 1.2    | 1500 | 2.0219        |
| 1.22   | 1525 | 2.0651        |
| 1.24   | 1550 | 1.9620        |
| 1.26   | 1575 | 2.0491        |
| 1.28   | 1600 | 2.0376        |
| 1.3    | 1625 | 2.0769        |
| 1.32   | 1650 | 1.9944        |
| 1.34   | 1675 | 2.0076        |
| 1.3600 | 1700 | 1.9353        |
| 1.38   | 1725 | 2.0186        |
| 1.4    | 1750 | 2.0528        |
| 1.42   | 1775 | 1.9582        |
| 1.44   | 1800 | 2.0882        |
| 1.46   | 1825 | 2.1299        |
| 1.48   | 1850 | 1.9363        |
| 1.5    | 1875 | 2.0281        |
| 1.52   | 1900 | 2.0451        |
| 1.54   | 1925 | 2.0219        |
| 1.56   | 1950 | 2.0249        |
| 1.58   | 1975 | 2.0002        |
| 1.6    | 2000 | 2.0483        |
| 1.62   | 2025 | 2.0175        |
| 1.6400 | 2050 | 2.0009        |
| 1.6600 | 2075 | 2.0057        |
| 1.6800 | 2100 | 2.0142        |
| 1.7    | 2125 | 1.9401        |
| 1.72   | 2150 | 2.0336        |
| 1.74   | 2175 | 2.0433        |
| 1.76   | 2200 | 2.0208        |
| 1.78   | 2225 | 1.9698        |
| 1.8    | 2250 | 1.9271        |
| 1.8200 | 2275 | 2.0185        |
| 1.8400 | 2300 | 2.0080        |
| 1.8600 | 2325 | 2.0605        |
| 1.88   | 2350 | 2.0419        |
| 1.9    | 2375 | 2.0041        |
| 1.92   | 2400 | 1.9892        |
| 1.94   | 2425 | 2.0001        |
| 1.96   | 2450 | 1.9322        |
| 1.98   | 2475 | 2.0071        |
| 2.0    | 2500 | 1.9827        |
| 2.02   | 2525 | 1.7543        |
| 2.04   | 2550 | 1.7380        |
| 2.06   | 2575 | 1.7148        |
| 2.08   | 2600 | 1.6868        |
| 2.1    | 2625 | 1.7038        |
| 2.12   | 2650 | 1.7510        |
| 2.14   | 2675 | 1.7739        |
| 2.16   | 2700 | 1.7248        |
| 2.18   | 2725 | 1.7195        |
| 2.2    | 2750 | 1.6987        |
| 2.22   | 2775 | 1.7676        |
| 2.24   | 2800 | 1.7700        |
| 2.26   | 2825 | 1.6955        |
| 2.2800 | 2850 | 1.7098        |
| 2.3    | 2875 | 1.7667        |
| 2.32   | 2900 | 1.7456        |
| 2.34   | 2925 | 1.7434        |
| 2.36   | 2950 | 1.6820        |
| 2.38   | 2975 | 1.7370        |
| 2.4    | 3000 | 1.7368        |
| 2.42   | 3025 | 1.7393        |
| 2.44   | 3050 | 1.7149        |
| 2.46   | 3075 | 1.7903        |
| 2.48   | 3100 | 1.7328        |
| 2.5    | 3125 | 1.6855        |
| 2.52   | 3150 | 1.7175        |
| 2.54   | 3175 | 1.7571        |
| 2.56   | 3200 | 1.6761        |
| 2.58   | 3225 | 1.7442        |
| 2.6    | 3250 | 1.7348        |
| 2.62   | 3275 | 1.7314        |
| 2.64   | 3300 | 1.7678        |
| 2.66   | 3325 | 1.7167        |
| 2.68   | 3350 | 1.7636        |
| 2.7    | 3375 | 1.7021        |
| 2.7200 | 3400 | 1.7225        |
| 2.74   | 3425 | 1.7247        |
| 2.76   | 3450 | 1.7245        |
| 2.7800 | 3475 | 1.6606        |
| 2.8    | 3500 | 1.6831        |
| 2.82   | 3525 | 1.6570        |
| 2.84   | 3550 | 1.7139        |
| 2.86   | 3575 | 1.7168        |
| 2.88   | 3600 | 1.7412        |
| 2.9    | 3625 | 1.7458        |
| 2.92   | 3650 | 1.6771        |
| 2.94   | 3675 | 1.7313        |
| 2.96   | 3700 | 1.6649        |
| 2.98   | 3725 | 1.7742        |
| 3.0    | 3750 | 1.6718        |

</details>

### Training Time
- **Training**: 2.4 hours

### Framework Versions
- Python: 3.12.10
- Sentence Transformers: 6.2.0
- Transformers: 5.22.1
- PyTorch: 2.14.1+cu126
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