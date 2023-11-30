"""Step to run automated tests in the pipeline."""
import os
import sys

import anyio
import base
import dagger


async def test_all(version: str):
    """Run all the automated tests."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        gcp_credentials_content = (
            client.set_secret(
                'GOOGLE_APPLICATION_CREDENTIALS_CONTENT',
                os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT'],
            )
        )

        src = client.host().directory('.')

        setup = (
            base.thipster_base(client, version)
            .with_mounted_directory('/src', src)
            .with_workdir('/src')
            .with_exec(['pip', 'install', '-e', '.[test]'])
            .with_secret_variable(
                'GOOGLE_APPLICATION_CREDENTIALS_CONTENT', gcp_credentials_content,
            )
        )

        tests = setup.with_exec(['pytest', 'tests'])
        # execute
        await tests.sync()

    print('Tests succeeded!')


if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(test_all, python_version)
