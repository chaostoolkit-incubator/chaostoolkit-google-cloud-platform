from chaosgcp import is_lueur_installed
from chaosgcp.lb.actions import __all__


def test_import_lueur() -> None:
    if is_lueur_installed():
        assert "add_latency_to_endpoint" in __all__
        assert "remove_latency_from_endpoint" in __all__
    else:
        assert "add_latency_to_endpoint" not in __all__
        assert "remove_latency_from_endpoint" not in __all__
