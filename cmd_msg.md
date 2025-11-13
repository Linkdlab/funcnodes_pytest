feat(pytest-funcnodes): add async funcnodes_test decorator

Provide a funcnodes_test decorator that sets async markers and handles
setup/teardown via a dedicated fixture so async node tests share the same
helpers. Align pytester invocations to use the function-scoped asyncio loop.
