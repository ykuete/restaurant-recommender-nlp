---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:80000
- loss:MultipleNegativesRankingLoss
base_model: BAAI/bge-small-en-v1.5
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

# SentenceTransformer based on BAAI/bge-small-en-v1.5

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5). It maps inputs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) <!-- at revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a -->
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
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'cls', 'include_prompt': True})
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
# tensor([[1.0000, 0.9439, 0.3669],
#         [0.9439, 1.0000, 0.3784],
#         [0.3669, 0.3784, 1.0000]])
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

- `per_device_train_batch_size`: 4
- `num_train_epochs`: 2
- `learning_rate`: 0.0001
- `warmup_steps`: 0.1
- `fp16`: True

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 4
- `num_train_epochs`: 2
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
- `fp16`: True
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
| 0.0013 | 25    | 1.1720        |
| 0.0025 | 50    | 1.1773        |
| 0.0037 | 75    | 1.1425        |
| 0.005  | 100   | 1.1801        |
| 0.0063 | 125   | 0.9962        |
| 0.0075 | 150   | 1.0784        |
| 0.0088 | 175   | 0.9308        |
| 0.01   | 200   | 0.8460        |
| 0.0112 | 225   | 0.8613        |
| 0.0125 | 250   | 0.9403        |
| 0.0138 | 275   | 0.8186        |
| 0.015  | 300   | 0.7368        |
| 0.0163 | 325   | 0.8529        |
| 0.0175 | 350   | 0.9358        |
| 0.0187 | 375   | 0.7305        |
| 0.02   | 400   | 0.8583        |
| 0.0213 | 425   | 0.7224        |
| 0.0225 | 450   | 0.6680        |
| 0.0238 | 475   | 0.7141        |
| 0.025  | 500   | 0.8095        |
| 0.0262 | 525   | 0.5968        |
| 0.0275 | 550   | 0.7621        |
| 0.0288 | 575   | 0.7356        |
| 0.03   | 600   | 0.6734        |
| 0.0312 | 625   | 0.7552        |
| 0.0325 | 650   | 0.8634        |
| 0.0338 | 675   | 0.8347        |
| 0.035  | 700   | 0.7469        |
| 0.0362 | 725   | 0.7268        |
| 0.0375 | 750   | 0.6041        |
| 0.0387 | 775   | 0.8846        |
| 0.04   | 800   | 0.6239        |
| 0.0413 | 825   | 0.7081        |
| 0.0425 | 850   | 0.7754        |
| 0.0437 | 875   | 0.5644        |
| 0.045  | 900   | 0.6323        |
| 0.0462 | 925   | 0.7477        |
| 0.0475 | 950   | 0.7268        |
| 0.0488 | 975   | 0.8043        |
| 0.05   | 1000  | 0.7969        |
| 0.0512 | 1025  | 0.8838        |
| 0.0525 | 1050  | 0.7585        |
| 0.0537 | 1075  | 0.7896        |
| 0.055  | 1100  | 0.7711        |
| 0.0563 | 1125  | 0.7577        |
| 0.0575 | 1150  | 0.6282        |
| 0.0587 | 1175  | 0.5964        |
| 0.06   | 1200  | 0.7863        |
| 0.0612 | 1225  | 0.8022        |
| 0.0625 | 1250  | 0.7270        |
| 0.0638 | 1275  | 0.7476        |
| 0.065  | 1300  | 0.7348        |
| 0.0663 | 1325  | 0.6784        |
| 0.0675 | 1350  | 0.8741        |
| 0.0688 | 1375  | 0.5776        |
| 0.07   | 1400  | 0.7434        |
| 0.0712 | 1425  | 0.5636        |
| 0.0725 | 1450  | 0.6886        |
| 0.0737 | 1475  | 0.9013        |
| 0.075  | 1500  | 0.6583        |
| 0.0762 | 1525  | 0.7769        |
| 0.0775 | 1550  | 0.7108        |
| 0.0788 | 1575  | 0.6420        |
| 0.08   | 1600  | 0.6336        |
| 0.0813 | 1625  | 0.6613        |
| 0.0825 | 1650  | 0.7204        |
| 0.0838 | 1675  | 0.7762        |
| 0.085  | 1700  | 0.5416        |
| 0.0862 | 1725  | 0.8808        |
| 0.0875 | 1750  | 0.5922        |
| 0.0887 | 1775  | 0.7220        |
| 0.09   | 1800  | 0.6069        |
| 0.0912 | 1825  | 0.8696        |
| 0.0925 | 1850  | 0.7731        |
| 0.0938 | 1875  | 0.9837        |
| 0.095  | 1900  | 0.7733        |
| 0.0963 | 1925  | 0.7222        |
| 0.0975 | 1950  | 0.6210        |
| 0.0988 | 1975  | 0.7256        |
| 0.1    | 2000  | 0.7595        |
| 0.1013 | 2025  | 0.6504        |
| 0.1025 | 2050  | 0.6095        |
| 0.1037 | 2075  | 0.8327        |
| 0.105  | 2100  | 0.7491        |
| 0.1062 | 2125  | 0.7542        |
| 0.1075 | 2150  | 0.5834        |
| 0.1087 | 2175  | 0.5628        |
| 0.11   | 2200  | 0.5588        |
| 0.1113 | 2225  | 0.6768        |
| 0.1125 | 2250  | 0.7092        |
| 0.1138 | 2275  | 0.5909        |
| 0.115  | 2300  | 0.9505        |
| 0.1163 | 2325  | 0.6630        |
| 0.1175 | 2350  | 0.6489        |
| 0.1187 | 2375  | 0.6012        |
| 0.12   | 2400  | 0.8489        |
| 0.1212 | 2425  | 0.7961        |
| 0.1225 | 2450  | 0.7865        |
| 0.1237 | 2475  | 0.6973        |
| 0.125  | 2500  | 0.6758        |
| 0.1263 | 2525  | 0.8036        |
| 0.1275 | 2550  | 0.6732        |
| 0.1288 | 2575  | 0.5501        |
| 0.13   | 2600  | 0.8136        |
| 0.1313 | 2625  | 0.9047        |
| 0.1325 | 2650  | 0.7709        |
| 0.1338 | 2675  | 0.9437        |
| 0.135  | 2700  | 0.6624        |
| 0.1363 | 2725  | 0.5397        |
| 0.1375 | 2750  | 0.8910        |
| 0.1388 | 2775  | 0.5968        |
| 0.14   | 2800  | 0.7734        |
| 0.1412 | 2825  | 0.6326        |
| 0.1425 | 2850  | 0.7235        |
| 0.1437 | 2875  | 0.7253        |
| 0.145  | 2900  | 0.7907        |
| 0.1462 | 2925  | 0.6860        |
| 0.1475 | 2950  | 0.9049        |
| 0.1487 | 2975  | 0.7557        |
| 0.15   | 3000  | 0.7385        |
| 0.1512 | 3025  | 0.6431        |
| 0.1525 | 3050  | 0.7585        |
| 0.1537 | 3075  | 0.5211        |
| 0.155  | 3100  | 0.8872        |
| 0.1562 | 3125  | 0.7649        |
| 0.1575 | 3150  | 0.6976        |
| 0.1588 | 3175  | 0.5451        |
| 0.16   | 3200  | 0.6942        |
| 0.1613 | 3225  | 1.1890        |
| 0.1625 | 3250  | 0.7170        |
| 0.1638 | 3275  | 0.6607        |
| 0.165  | 3300  | 0.8268        |
| 0.1663 | 3325  | 0.8651        |
| 0.1675 | 3350  | 0.7202        |
| 0.1688 | 3375  | 0.6963        |
| 0.17   | 3400  | 0.8843        |
| 0.1713 | 3425  | 0.6403        |
| 0.1725 | 3450  | 0.7863        |
| 0.1737 | 3475  | 0.6866        |
| 0.175  | 3500  | 0.5810        |
| 0.1762 | 3525  | 0.7537        |
| 0.1775 | 3550  | 0.6948        |
| 0.1787 | 3575  | 0.8373        |
| 0.18   | 3600  | 0.7274        |
| 0.1812 | 3625  | 0.8091        |
| 0.1825 | 3650  | 0.6713        |
| 0.1837 | 3675  | 0.8520        |
| 0.185  | 3700  | 0.7152        |
| 0.1862 | 3725  | 0.8255        |
| 0.1875 | 3750  | 0.9193        |
| 0.1888 | 3775  | 0.6136        |
| 0.19   | 3800  | 0.9089        |
| 0.1913 | 3825  | 0.8172        |
| 0.1925 | 3850  | 0.7399        |
| 0.1938 | 3875  | 0.6348        |
| 0.195  | 3900  | 0.7493        |
| 0.1963 | 3925  | 0.7031        |
| 0.1975 | 3950  | 0.7467        |
| 0.1988 | 3975  | 0.7618        |
| 0.2    | 4000  | 0.7422        |
| 0.2013 | 4025  | 0.6903        |
| 0.2025 | 4050  | 0.8278        |
| 0.2037 | 4075  | 0.6404        |
| 0.205  | 4100  | 0.6817        |
| 0.2062 | 4125  | 0.8449        |
| 0.2075 | 4150  | 0.7293        |
| 0.2087 | 4175  | 0.6591        |
| 0.21   | 4200  | 0.7780        |
| 0.2112 | 4225  | 0.7680        |
| 0.2125 | 4250  | 0.7690        |
| 0.2137 | 4275  | 0.6399        |
| 0.215  | 4300  | 0.7721        |
| 0.2162 | 4325  | 0.6944        |
| 0.2175 | 4350  | 0.7551        |
| 0.2188 | 4375  | 0.6087        |
| 0.22   | 4400  | 0.9479        |
| 0.2213 | 4425  | 0.8096        |
| 0.2225 | 4450  | 0.8135        |
| 0.2238 | 4475  | 0.7946        |
| 0.225  | 4500  | 0.7188        |
| 0.2263 | 4525  | 0.8069        |
| 0.2275 | 4550  | 0.6695        |
| 0.2288 | 4575  | 0.8403        |
| 0.23   | 4600  | 0.6601        |
| 0.2313 | 4625  | 0.8322        |
| 0.2325 | 4650  | 0.8946        |
| 0.2338 | 4675  | 0.8243        |
| 0.235  | 4700  | 0.5381        |
| 0.2362 | 4725  | 0.9481        |
| 0.2375 | 4750  | 0.7711        |
| 0.2387 | 4775  | 0.8293        |
| 0.24   | 4800  | 0.7969        |
| 0.2412 | 4825  | 0.6313        |
| 0.2425 | 4850  | 0.6665        |
| 0.2437 | 4875  | 0.9213        |
| 0.245  | 4900  | 0.6396        |
| 0.2462 | 4925  | 0.7863        |
| 0.2475 | 4950  | 0.5868        |
| 0.2487 | 4975  | 0.8873        |
| 0.25   | 5000  | 0.7655        |
| 0.2512 | 5025  | 0.6181        |
| 0.2525 | 5050  | 0.7801        |
| 0.2537 | 5075  | 0.5086        |
| 0.255  | 5100  | 1.1006        |
| 0.2562 | 5125  | 0.9027        |
| 0.2575 | 5150  | 0.7157        |
| 0.2587 | 5175  | 0.6769        |
| 0.26   | 5200  | 0.7328        |
| 0.2612 | 5225  | 0.7803        |
| 0.2625 | 5250  | 0.5774        |
| 0.2637 | 5275  | 0.7223        |
| 0.265  | 5300  | 0.8073        |
| 0.2662 | 5325  | 0.6083        |
| 0.2675 | 5350  | 0.8730        |
| 0.2687 | 5375  | 0.7656        |
| 0.27   | 5400  | 0.7174        |
| 0.2712 | 5425  | 0.6723        |
| 0.2725 | 5450  | 0.6507        |
| 0.2737 | 5475  | 0.5976        |
| 0.275  | 5500  | 0.6147        |
| 0.2762 | 5525  | 0.7443        |
| 0.2775 | 5550  | 0.8941        |
| 0.2787 | 5575  | 0.7434        |
| 0.28   | 5600  | 0.5462        |
| 0.2812 | 5625  | 0.7130        |
| 0.2825 | 5650  | 0.7030        |
| 0.2838 | 5675  | 0.7378        |
| 0.285  | 5700  | 0.5149        |
| 0.2863 | 5725  | 0.9110        |
| 0.2875 | 5750  | 0.7971        |
| 0.2888 | 5775  | 0.7137        |
| 0.29   | 5800  | 0.6038        |
| 0.2913 | 5825  | 0.6924        |
| 0.2925 | 5850  | 0.8485        |
| 0.2938 | 5875  | 0.5826        |
| 0.295  | 5900  | 0.7660        |
| 0.2963 | 5925  | 0.6651        |
| 0.2975 | 5950  | 0.6939        |
| 0.2988 | 5975  | 0.6861        |
| 0.3    | 6000  | 0.7184        |
| 0.3013 | 6025  | 0.6125        |
| 0.3025 | 6050  | 0.9232        |
| 0.3038 | 6075  | 0.6511        |
| 0.305  | 6100  | 0.7772        |
| 0.3063 | 6125  | 0.7413        |
| 0.3075 | 6150  | 0.6506        |
| 0.3088 | 6175  | 0.6082        |
| 0.31   | 6200  | 0.5507        |
| 0.3113 | 6225  | 0.7732        |
| 0.3125 | 6250  | 0.7673        |
| 0.3137 | 6275  | 0.6672        |
| 0.315  | 6300  | 0.6711        |
| 0.3162 | 6325  | 0.7702        |
| 0.3175 | 6350  | 0.6679        |
| 0.3187 | 6375  | 0.8133        |
| 0.32   | 6400  | 0.7465        |
| 0.3212 | 6425  | 0.8514        |
| 0.3225 | 6450  | 0.7013        |
| 0.3237 | 6475  | 0.5119        |
| 0.325  | 6500  | 0.7577        |
| 0.3262 | 6525  | 0.7215        |
| 0.3275 | 6550  | 0.7440        |
| 0.3287 | 6575  | 0.7362        |
| 0.33   | 6600  | 0.6160        |
| 0.3312 | 6625  | 0.5898        |
| 0.3325 | 6650  | 0.6859        |
| 0.3337 | 6675  | 0.5794        |
| 0.335  | 6700  | 0.6803        |
| 0.3362 | 6725  | 0.8837        |
| 0.3375 | 6750  | 0.4898        |
| 0.3387 | 6775  | 0.7045        |
| 0.34   | 6800  | 0.6478        |
| 0.3412 | 6825  | 0.7346        |
| 0.3425 | 6850  | 0.8569        |
| 0.3438 | 6875  | 0.7088        |
| 0.345  | 6900  | 0.7558        |
| 0.3463 | 6925  | 0.7785        |
| 0.3475 | 6950  | 0.5615        |
| 0.3488 | 6975  | 0.5123        |
| 0.35   | 7000  | 0.4913        |
| 0.3513 | 7025  | 0.6631        |
| 0.3525 | 7050  | 0.9468        |
| 0.3538 | 7075  | 0.5844        |
| 0.355  | 7100  | 0.6657        |
| 0.3563 | 7125  | 0.6421        |
| 0.3575 | 7150  | 0.5126        |
| 0.3588 | 7175  | 0.6357        |
| 0.36   | 7200  | 0.6946        |
| 0.3613 | 7225  | 0.6451        |
| 0.3625 | 7250  | 0.8367        |
| 0.3638 | 7275  | 0.9583        |
| 0.365  | 7300  | 0.5129        |
| 0.3663 | 7325  | 0.6705        |
| 0.3675 | 7350  | 0.7964        |
| 0.3688 | 7375  | 0.5663        |
| 0.37   | 7400  | 0.5722        |
| 0.3713 | 7425  | 0.8434        |
| 0.3725 | 7450  | 0.8503        |
| 0.3738 | 7475  | 0.6634        |
| 0.375  | 7500  | 0.5629        |
| 0.3762 | 7525  | 0.4004        |
| 0.3775 | 7550  | 0.7572        |
| 0.3787 | 7575  | 0.8749        |
| 0.38   | 7600  | 0.9116        |
| 0.3812 | 7625  | 0.8550        |
| 0.3825 | 7650  | 0.9189        |
| 0.3837 | 7675  | 0.5963        |
| 0.385  | 7700  | 0.8114        |
| 0.3862 | 7725  | 0.5772        |
| 0.3875 | 7750  | 0.6490        |
| 0.3887 | 7775  | 0.7431        |
| 0.39   | 7800  | 0.9081        |
| 0.3912 | 7825  | 0.6333        |
| 0.3925 | 7850  | 0.5336        |
| 0.3937 | 7875  | 0.6337        |
| 0.395  | 7900  | 0.6618        |
| 0.3962 | 7925  | 0.7822        |
| 0.3975 | 7950  | 0.8131        |
| 0.3987 | 7975  | 0.6685        |
| 0.4    | 8000  | 0.7892        |
| 0.4012 | 8025  | 0.5601        |
| 0.4025 | 8050  | 0.6577        |
| 0.4037 | 8075  | 0.8196        |
| 0.405  | 8100  | 0.6321        |
| 0.4062 | 8125  | 0.7432        |
| 0.4075 | 8150  | 0.5869        |
| 0.4088 | 8175  | 0.7964        |
| 0.41   | 8200  | 0.6237        |
| 0.4113 | 8225  | 0.6304        |
| 0.4125 | 8250  | 0.7284        |
| 0.4138 | 8275  | 0.8963        |
| 0.415  | 8300  | 0.8918        |
| 0.4163 | 8325  | 0.7350        |
| 0.4175 | 8350  | 0.6279        |
| 0.4188 | 8375  | 0.7538        |
| 0.42   | 8400  | 0.6798        |
| 0.4213 | 8425  | 0.6402        |
| 0.4225 | 8450  | 0.5884        |
| 0.4238 | 8475  | 0.6890        |
| 0.425  | 8500  | 0.9278        |
| 0.4263 | 8525  | 0.6678        |
| 0.4275 | 8550  | 0.8428        |
| 0.4288 | 8575  | 0.4930        |
| 0.43   | 8600  | 0.5718        |
| 0.4313 | 8625  | 0.8381        |
| 0.4325 | 8650  | 0.6172        |
| 0.4338 | 8675  | 0.7783        |
| 0.435  | 8700  | 0.6666        |
| 0.4363 | 8725  | 0.6182        |
| 0.4375 | 8750  | 0.6740        |
| 0.4387 | 8775  | 0.7049        |
| 0.44   | 8800  | 0.6070        |
| 0.4412 | 8825  | 0.8557        |
| 0.4425 | 8850  | 0.6740        |
| 0.4437 | 8875  | 0.5745        |
| 0.445  | 8900  | 0.6174        |
| 0.4462 | 8925  | 0.8036        |
| 0.4475 | 8950  | 0.8130        |
| 0.4487 | 8975  | 0.7159        |
| 0.45   | 9000  | 0.7310        |
| 0.4512 | 9025  | 0.6194        |
| 0.4525 | 9050  | 0.6612        |
| 0.4537 | 9075  | 0.7787        |
| 0.455  | 9100  | 0.6648        |
| 0.4562 | 9125  | 0.6190        |
| 0.4575 | 9150  | 0.6827        |
| 0.4587 | 9175  | 0.9336        |
| 0.46   | 9200  | 0.7655        |
| 0.4612 | 9225  | 0.7665        |
| 0.4625 | 9250  | 0.7164        |
| 0.4637 | 9275  | 0.6320        |
| 0.465  | 9300  | 0.6982        |
| 0.4662 | 9325  | 0.5862        |
| 0.4675 | 9350  | 0.8501        |
| 0.4688 | 9375  | 0.6600        |
| 0.47   | 9400  | 0.6304        |
| 0.4713 | 9425  | 0.7223        |
| 0.4725 | 9450  | 0.5505        |
| 0.4738 | 9475  | 0.7912        |
| 0.475  | 9500  | 0.6309        |
| 0.4763 | 9525  | 0.8334        |
| 0.4775 | 9550  | 0.5647        |
| 0.4788 | 9575  | 0.5977        |
| 0.48   | 9600  | 0.7143        |
| 0.4813 | 9625  | 0.7207        |
| 0.4825 | 9650  | 0.7016        |
| 0.4838 | 9675  | 0.6509        |
| 0.485  | 9700  | 0.6379        |
| 0.4863 | 9725  | 0.6272        |
| 0.4875 | 9750  | 0.8231        |
| 0.4888 | 9775  | 0.8246        |
| 0.49   | 9800  | 0.7630        |
| 0.4913 | 9825  | 0.6404        |
| 0.4925 | 9850  | 0.5923        |
| 0.4938 | 9875  | 0.6745        |
| 0.495  | 9900  | 0.6000        |
| 0.4963 | 9925  | 0.7072        |
| 0.4975 | 9950  | 0.5523        |
| 0.4988 | 9975  | 0.5976        |
| 0.5    | 10000 | 0.9657        |
| 0.5012 | 10025 | 0.5100        |
| 0.5025 | 10050 | 0.5682        |
| 0.5038 | 10075 | 0.7408        |
| 0.505  | 10100 | 0.7876        |
| 0.5062 | 10125 | 0.7953        |
| 0.5075 | 10150 | 0.6079        |
| 0.5088 | 10175 | 0.7043        |
| 0.51   | 10200 | 0.6294        |
| 0.5112 | 10225 | 0.7488        |
| 0.5125 | 10250 | 0.6616        |
| 0.5138 | 10275 | 0.6115        |
| 0.515  | 10300 | 0.8339        |
| 0.5162 | 10325 | 0.5206        |
| 0.5175 | 10350 | 0.7688        |
| 0.5188 | 10375 | 0.5632        |
| 0.52   | 10400 | 0.5319        |
| 0.5212 | 10425 | 0.6973        |
| 0.5225 | 10450 | 0.6258        |
| 0.5238 | 10475 | 0.8200        |
| 0.525  | 10500 | 0.6554        |
| 0.5262 | 10525 | 0.6676        |
| 0.5275 | 10550 | 0.7165        |
| 0.5288 | 10575 | 0.6084        |
| 0.53   | 10600 | 0.6789        |
| 0.5312 | 10625 | 0.7738        |
| 0.5325 | 10650 | 0.6353        |
| 0.5337 | 10675 | 0.5687        |
| 0.535  | 10700 | 0.7877        |
| 0.5363 | 10725 | 0.5800        |
| 0.5375 | 10750 | 0.6925        |
| 0.5387 | 10775 | 0.5422        |
| 0.54   | 10800 | 0.5345        |
| 0.5413 | 10825 | 1.0529        |
| 0.5425 | 10850 | 0.8141        |
| 0.5437 | 10875 | 0.6341        |
| 0.545  | 10900 | 0.7083        |
| 0.5463 | 10925 | 0.7265        |
| 0.5475 | 10950 | 0.5723        |
| 0.5487 | 10975 | 0.6198        |
| 0.55   | 11000 | 0.6677        |
| 0.5513 | 11025 | 0.7644        |
| 0.5525 | 11050 | 0.5949        |
| 0.5537 | 11075 | 0.6413        |
| 0.555  | 11100 | 0.7729        |
| 0.5563 | 11125 | 0.5190        |
| 0.5575 | 11150 | 0.8312        |
| 0.5587 | 11175 | 0.7787        |
| 0.56   | 11200 | 0.5835        |
| 0.5613 | 11225 | 0.6664        |
| 0.5625 | 11250 | 0.5641        |
| 0.5637 | 11275 | 0.5979        |
| 0.565  | 11300 | 0.8471        |
| 0.5663 | 11325 | 0.7396        |
| 0.5675 | 11350 | 0.9150        |
| 0.5687 | 11375 | 0.4850        |
| 0.57   | 11400 | 0.7094        |
| 0.5713 | 11425 | 0.7696        |
| 0.5725 | 11450 | 0.6256        |
| 0.5737 | 11475 | 0.4181        |
| 0.575  | 11500 | 0.6260        |
| 0.5763 | 11525 | 0.7961        |
| 0.5775 | 11550 | 0.6363        |
| 0.5787 | 11575 | 0.7281        |
| 0.58   | 11600 | 0.7880        |
| 0.5813 | 11625 | 0.5954        |
| 0.5825 | 11650 | 0.5743        |
| 0.5837 | 11675 | 0.6753        |
| 0.585  | 11700 | 0.7345        |
| 0.5863 | 11725 | 0.5402        |
| 0.5875 | 11750 | 0.8656        |
| 0.5887 | 11775 | 0.6105        |
| 0.59   | 11800 | 0.5451        |
| 0.5913 | 11825 | 0.5330        |
| 0.5925 | 11850 | 0.6919        |
| 0.5938 | 11875 | 0.5351        |
| 0.595  | 11900 | 0.5684        |
| 0.5962 | 11925 | 0.5776        |
| 0.5975 | 11950 | 0.6554        |
| 0.5988 | 11975 | 0.5905        |
| 0.6    | 12000 | 0.7046        |
| 0.6012 | 12025 | 0.4556        |
| 0.6025 | 12050 | 0.8084        |
| 0.6038 | 12075 | 0.6321        |
| 0.605  | 12100 | 0.5836        |
| 0.6062 | 12125 | 0.7661        |
| 0.6075 | 12150 | 0.6410        |
| 0.6088 | 12175 | 0.6460        |
| 0.61   | 12200 | 0.8993        |
| 0.6112 | 12225 | 0.7221        |
| 0.6125 | 12250 | 0.6570        |
| 0.6138 | 12275 | 0.5692        |
| 0.615  | 12300 | 0.8256        |
| 0.6162 | 12325 | 0.7164        |
| 0.6175 | 12350 | 0.5457        |
| 0.6188 | 12375 | 0.5881        |
| 0.62   | 12400 | 0.6600        |
| 0.6212 | 12425 | 0.5578        |
| 0.6225 | 12450 | 0.6449        |
| 0.6238 | 12475 | 0.5915        |
| 0.625  | 12500 | 0.7445        |
| 0.6262 | 12525 | 0.6955        |
| 0.6275 | 12550 | 0.6722        |
| 0.6288 | 12575 | 0.5770        |
| 0.63   | 12600 | 0.7057        |
| 0.6312 | 12625 | 0.6814        |
| 0.6325 | 12650 | 0.7027        |
| 0.6338 | 12675 | 0.5903        |
| 0.635  | 12700 | 0.8004        |
| 0.6362 | 12725 | 0.6020        |
| 0.6375 | 12750 | 0.6946        |
| 0.6388 | 12775 | 0.6845        |
| 0.64   | 12800 | 0.7056        |
| 0.6412 | 12825 | 0.8180        |
| 0.6425 | 12850 | 0.7238        |
| 0.6438 | 12875 | 0.6541        |
| 0.645  | 12900 | 0.6842        |
| 0.6462 | 12925 | 0.5381        |
| 0.6475 | 12950 | 0.6597        |
| 0.6488 | 12975 | 0.6249        |
| 0.65   | 13000 | 0.7225        |
| 0.6512 | 13025 | 0.7401        |
| 0.6525 | 13050 | 0.6021        |
| 0.6538 | 13075 | 0.5380        |
| 0.655  | 13100 | 0.5733        |
| 0.6562 | 13125 | 0.7120        |
| 0.6575 | 13150 | 0.7729        |
| 0.6587 | 13175 | 0.7281        |
| 0.66   | 13200 | 0.7641        |
| 0.6613 | 13225 | 0.6122        |
| 0.6625 | 13250 | 0.4197        |
| 0.6637 | 13275 | 0.6554        |
| 0.665  | 13300 | 0.5363        |
| 0.6663 | 13325 | 0.7377        |
| 0.6675 | 13350 | 0.5302        |
| 0.6687 | 13375 | 0.5821        |
| 0.67   | 13400 | 0.5834        |
| 0.6713 | 13425 | 0.8220        |
| 0.6725 | 13450 | 0.6231        |
| 0.6737 | 13475 | 0.7209        |
| 0.675  | 13500 | 0.5883        |
| 0.6763 | 13525 | 0.5178        |
| 0.6775 | 13550 | 0.6742        |
| 0.6787 | 13575 | 0.6166        |
| 0.68   | 13600 | 0.8851        |
| 0.6813 | 13625 | 0.7724        |
| 0.6825 | 13650 | 0.6440        |
| 0.6837 | 13675 | 0.6304        |
| 0.685  | 13700 | 0.7454        |
| 0.6863 | 13725 | 0.7291        |
| 0.6875 | 13750 | 0.5706        |
| 0.6887 | 13775 | 0.5932        |
| 0.69   | 13800 | 0.8993        |
| 0.6913 | 13825 | 0.5399        |
| 0.6925 | 13850 | 0.6689        |
| 0.6937 | 13875 | 0.6743        |
| 0.695  | 13900 | 0.6404        |
| 0.6963 | 13925 | 0.5449        |
| 0.6975 | 13950 | 0.5138        |
| 0.6987 | 13975 | 0.9076        |
| 0.7    | 14000 | 0.6606        |
| 0.7013 | 14025 | 0.5405        |
| 0.7025 | 14050 | 0.7246        |
| 0.7037 | 14075 | 0.8294        |
| 0.705  | 14100 | 0.6852        |
| 0.7063 | 14125 | 0.7603        |
| 0.7075 | 14150 | 0.6912        |
| 0.7087 | 14175 | 0.6014        |
| 0.71   | 14200 | 0.9365        |
| 0.7113 | 14225 | 0.6306        |
| 0.7125 | 14250 | 0.6067        |
| 0.7137 | 14275 | 0.5687        |
| 0.715  | 14300 | 0.4934        |
| 0.7163 | 14325 | 0.7941        |
| 0.7175 | 14350 | 0.5560        |
| 0.7188 | 14375 | 0.7085        |
| 0.72   | 14400 | 0.7127        |
| 0.7212 | 14425 | 1.0005        |
| 0.7225 | 14450 | 0.5768        |
| 0.7238 | 14475 | 0.8644        |
| 0.725  | 14500 | 0.4697        |
| 0.7262 | 14525 | 0.7212        |
| 0.7275 | 14550 | 0.5020        |
| 0.7288 | 14575 | 0.6072        |
| 0.73   | 14600 | 0.6263        |
| 0.7312 | 14625 | 0.6389        |
| 0.7325 | 14650 | 0.5850        |
| 0.7338 | 14675 | 0.6762        |
| 0.735  | 14700 | 0.5702        |
| 0.7362 | 14725 | 0.5890        |
| 0.7375 | 14750 | 0.5934        |
| 0.7388 | 14775 | 0.6484        |
| 0.74   | 14800 | 0.5826        |
| 0.7412 | 14825 | 0.6881        |
| 0.7425 | 14850 | 0.5846        |
| 0.7438 | 14875 | 0.7771        |
| 0.745  | 14900 | 0.6375        |
| 0.7462 | 14925 | 0.6834        |
| 0.7475 | 14950 | 0.5860        |
| 0.7488 | 14975 | 0.5808        |
| 0.75   | 15000 | 0.6539        |

</details>

### Training Time
- **Training**: 1.7 hours

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