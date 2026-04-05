from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_recommend_batch_size():
    script = Path("scripts/find_batch_size.py")
    spec = spec_from_file_location("find_batch_size", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load scripts/find_batch_size.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.recommend_batch_size


def test_batch_size_recommendation_monotonic():
    recommend_batch_size = _load_recommend_batch_size()
    assert recommend_batch_size(8.0) <= recommend_batch_size(16.0) <= recommend_batch_size(24.0)
