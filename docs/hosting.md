# Hosting decision

Decided for v1.0.0. Prices and free-tier limits change often: re-check the
providers' pages before relying on them.

| Part | Host | Why |
| --- | --- | --- |
| Frontend (Next.js) | Vercel, Hobby plan | Made by the Next.js team; deploys every push to `main`; preview URL per pull request |
| API (FastAPI, Docker) | Render web service | Free plan (512 MB RAM) fits the slim API: ONNX query encoder, no PyTorch |
| Feedback database | Neon (hosted Postgres) | Container disks are not persistent, so feedback must live outside the API container |
| Model and artifacts | Hugging Face Hub, **private** repo | Too large for Git; private because they contain Yelp review text |

## Known limits

- **Render free instances sleep when idle.** The first search after a pause
  waits for the container to start and download the artifacts (up to about a
  minute). The frontend's error panel says so and offers "Try again".
- **512 MB RAM.** The API loads the ONNX model (about 90 MB), the restaurant
  vectors and the parquet tables. Check memory in the Render dashboard after
  the first deploy; if it is too tight, use the fallback below.

## Fallbacks

| If | Then |
| --- | --- |
| The API runs out of memory on Render | Google Cloud Run: same Docker image, set memory to 1-2 GB; scales to zero; needs a billing account (student credits help) |
| A host without sleeping is needed for a demo | Render's smallest paid instance, only for the demo week |

Hugging Face Spaces (2 vCPU, 16 GB RAM) was considered for the API, but new
Docker Spaces on personal accounts now need a PRO plan.

## Sources

- [Render pricing](https://render.com/pricing)
- [Hugging Face Spaces overview](https://huggingface.co/docs/hub/en/spaces-overview)
- [Hugging Face forum: free CPU Basic change](https://discuss.huggingface.co/t/official-community-complaint-revert-free-cpu-basic-spaces-and-remove-anti-developer-sdk-restrictions/177703)
