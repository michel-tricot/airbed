import sys

from airbyte_embed_cdk.platform.source_runner import ContainerSourceRunner


def main():
    source_runner = ContainerSourceRunner("airbyte/source-pokeapi", "0.1.5-dev.819dd97d48")
    source_runner.spec()

    # runner = None
    # worker = Worker(runner)
    # worker.start()


if __name__ == "__main__":
    sys.exit(main())
