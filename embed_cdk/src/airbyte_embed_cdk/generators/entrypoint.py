import json
from pathlib import Path
from tempfile import TemporaryDirectory

from airbyte_cdk.models import Type
from datamodel_code_generator import generate

from airbyte_embed_cdk.source_runner import SourceRunner
from airbyte_embed_cdk.tools import get_first_message


def generate_llama_index(source: SourceRunner, destination_path: Path[str]):
    message = get_first_message(source.spec(), Type.SPEC)

    if not message:
        raise Exception("No spec available")

    with TemporaryDirectory() as temporary_directory_name:
        temporary_directory = Path(temporary_directory_name)
        output = temporary_directory / 'model.py'
        generate(
            json.dumps(message.spec.connectionSpecification),
            output=output,
            class_name="abc"
        )
        model = output.read_text()
        print(model)
