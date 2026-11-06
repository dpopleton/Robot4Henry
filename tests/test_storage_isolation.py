from config import settings


def test_default_storage_paths_are_not_the_real_storage():
    real_storage = settings.BASE_DIR / "storage"
    assert not settings.DB_PATH.startswith(str(real_storage))
    assert not settings.CHROMA_PATH.startswith(str(real_storage))
