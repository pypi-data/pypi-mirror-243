"""Release a python package on pypi and GitHub."""
import os
import re
import sys

import anyio
import base
import dagger


async def release(python_version):
    """Run python semantic-release."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory('.')

        cr_pat = client.set_secret('password', os.environ['CR_PAT'])

        setup = await src.file('setup.py').contents()
        semver = re.search(
            r"__version__ = '(?P<version>(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+))'",  # noqa: E501
            setup,
        )
        cli_version = semver.group('version')

        image = (
            base.thipster_base(client, python_version)
            .with_workdir('/tmp')
            .with_exec(['pip', 'install', f'thipstercli=={cli_version}'])
            .with_entrypoint(['thipster'])
            .with_label(
                'org.opencontainers.image.source',
                'https://github.com/THipster/THipster-cli',
            )
            .with_registry_auth('ghcr.io', 'rcattin', cr_pat)
        )
        tags = [
            cli_version,
            f"{semver.group('major')}.{semver.group('minor')}",
            'latest',
        ]
        if int(semver.group('major')) > 0:
            tags.append(semver.group('major'))

        for tag in tags:
            address = await (
                image.publish(f'ghcr.io/thipster/cli:{tag}')
            )

            print(f'Image published at {address} ')

if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(release, python_version)
