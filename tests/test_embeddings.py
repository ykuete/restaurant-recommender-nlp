import numpy as np
import pytest

from recommender import config, embeddings


def test_restaurant_vectors_average_and_normalize():
    ids, matrix = embeddings.restaurant_vectors(
        ["b", "a", "b"], np.array([[1, 0], [0, 1], [0, 1]], dtype=np.float32)
    )
    assert list(ids) == ["a", "b"]
    np.testing.assert_allclose(matrix, [[0, 1], [np.sqrt(0.5), np.sqrt(0.5)]], atol=1e-6)


def test_index_search_returns_nearest_first():
    pytest.importorskip("faiss")
    ids = np.array(["x", "y", "z"])
    index = embeddings.build_index(np.eye(3, dtype=np.float32))
    hits = embeddings.search(index, ids, np.array([0, 1, 0], dtype=np.float32), k=2)
    assert hits[0] == ("y", pytest.approx(1.0))


@pytest.fixture
def toy_onnx_model(tmp_path):
    """A 6-word vocabulary and an ONNX graph whose 'hidden state' is just an
    embedding lookup: enough to test tokenizing, padding and pooling."""
    onnx = pytest.importorskip("onnx")
    from onnx import TensorProto, helper, numpy_helper
    from tokenizers import Tokenizer, models, pre_tokenizers

    vocab = {"[PAD]": 0, "[UNK]": 1, "great": 2, "pasta": 3, "slow": 4, "service": 5}
    tokenizer = Tokenizer(models.WordLevel(vocab, unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    tokenizer.save(str(tmp_path / "tokenizer.json"))

    table = np.arange(6 * 3, dtype=np.float32).reshape(6, 3)
    graph = helper.make_graph(
        [helper.make_node("Gather", ["table", "input_ids"], ["last_hidden_state"])],
        "toy",
        [
            helper.make_tensor_value_info("input_ids", TensorProto.INT64, ["n", "t"]),
            helper.make_tensor_value_info("attention_mask", TensorProto.INT64, ["n", "t"]),
        ],
        [helper.make_tensor_value_info("last_hidden_state", TensorProto.FLOAT, ["n", "t", 3])],
        initializer=[numpy_helper.from_array(table, "table")],
    )
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 13)])
    model.ir_version = 8
    onnx.save(model, str(tmp_path / "model.onnx"))
    return tmp_path, table


def test_onnx_encoder_mean_pools_real_tokens_only(toy_onnx_model):
    pytest.importorskip("onnxruntime")
    path, table = toy_onnx_model
    vectors = embeddings.OnnxEncoder(path)(["great pasta", "slow service great"])

    def expected(token_ids):
        v = table[token_ids].mean(axis=0)
        return v / np.linalg.norm(v)

    # The first text is padded to 3 tokens; padding must not change its vector.
    np.testing.assert_allclose(vectors[0], expected([2, 3]), rtol=1e-5)
    np.testing.assert_allclose(vectors[1], expected([4, 5, 2]), rtol=1e-5)


ARTIFACTS = config.ARTIFACTS_DIR


@pytest.mark.skipif(
    not (embeddings.onnx_dir(ARTIFACTS) / "model.onnx").exists()
    or not (embeddings.model_dir(ARTIFACTS) / "model.safetensors").exists(),
    reason="needs the trained model and its ONNX export in ARTIFACTS_DIR",
)
def test_onnx_matches_pytorch_model():
    pytest.importorskip("sentence_transformers")
    sentences = ["quiet date-night spot with great pasta", "fast, cheap lunch"]
    torch_vecs = embeddings.encode(
        embeddings.load_model(embeddings.model_dir(ARTIFACTS)), sentences
    )
    onnx_vecs = embeddings.OnnxEncoder(embeddings.onnx_dir(ARTIFACTS))(sentences)
    assert np.min(np.sum(torch_vecs * onnx_vecs, axis=1)) > 0.999
