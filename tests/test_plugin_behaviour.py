import pytest
from pytest_funcnodes import nodetest

PYTESTER_OPTIONS = ["-v", "-o", "asyncio_default_fixture_loop_scope=function"]


def test_nodetest_rejects_non_node_class():
    with pytest.raises(TypeError, match="node must be a subclass"):

        @nodetest("not-a-node")  # type: ignore[arg-type]
        async def _():  # pragma: no cover - function never runs
            ...


def test_nodetest_handles_typeerror_from_custom_class():
    class ExplodingMeta(type):
        def __subclasscheck__(cls, subclass):
            raise TypeError("boom")

    class Exploding(metaclass=ExplodingMeta):
        pass

    with pytest.raises(TypeError, match="node must be a subclass"):

        @nodetest(Exploding)  # type: ignore[arg-type]
        async def _():  # pragma: no cover - function never runs
            ...


def test_nodetest_rejects_sync_function():
    with pytest.raises(TypeError):

        @nodetest()
        def _sync():  # pragma: no cover - function never runs
            return True


def test_funcnodes_test_decorator_with_kwargs(pytester: pytest.Pytester):
    test_file = pytester.makepyfile(
        """
        import funcnodes_core
        from pytest_funcnodes import funcnodes_test


        @funcnodes_test(add_pid=False, disable_file_handler=False)
        def test_config_dir_name_is_stable():
            config_dir = funcnodes_core.config.get_config_dir()
            assert config_dir.name == "funcnodes_test"
    """
    )
    result = pytester.runpytest(*PYTESTER_OPTIONS)
    result.assert_outcomes(passed=1)
    assert test_file.is_file()


def test_plugin_filters_and_tracks_nodetests(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import funcnodes_core as fn
        import pytest
        from pytest_funcnodes import nodetest


        @fn.NodeDecorator("tracked_node")
        def tracked_node():
            pass

        @nodetest(tracked_node)
        async def test_nodetest_only():
            assert True

        def test_regular():
            assert True

        def test_recorded_nodes(all_nodes):
            assert tracked_node in all_nodes
            assert len(all_nodes) == 1
    """
    )
    filtered = pytester.runpytest("--nodetests-only", *PYTESTER_OPTIONS)
    filtered.assert_outcomes(passed=1)
    regular = pytester.runpytest(*PYTESTER_OPTIONS)
    regular.assert_outcomes(passed=3)


def test_plugin_handles_marker_without_nodes(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.nodetest
        @pytest.mark.asyncio
        async def test_missing_nodes_marker():
            assert True

        def test_all_nodes_empty(all_nodes):
            assert all_nodes == set()
    """
    )
    result = pytester.runpytest(*PYTESTER_OPTIONS)
    result.assert_outcomes(passed=2)
