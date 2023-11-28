"""Pull request pipeline."""
import anyio
from automated_tests import test_all
from precommit import pre_commit


async def pr_handler(version):
    """Run the pre-commit and test pipelines in parallel."""
    async with anyio.create_task_group() as tg:
        tg.start_soon(pre_commit, version)
        tg.start_soon(test_all, version)

if __name__ == '__main__':
    versions = ['3.11.3']
    for version in versions:
        anyio.run(pr_handler, version)
