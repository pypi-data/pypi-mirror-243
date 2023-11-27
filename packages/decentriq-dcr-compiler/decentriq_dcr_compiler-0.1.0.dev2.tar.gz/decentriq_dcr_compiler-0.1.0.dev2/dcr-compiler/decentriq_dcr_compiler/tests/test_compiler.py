from decentriq_dcr_compiler import __version__, compiler
from decentriq_dcr_compiler.schemas.data_science_data_room import (
    DataScienceDataRoom,
    DataScienceDataRoomConfiguration,
    DataScienceDataRoomItem,
    DataScienceDataRoomItem1,
)


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_compile_and_verify() -> None:
    example = DataScienceDataRoomItem(
        V0=DataScienceDataRoom(
            __root__=DataScienceDataRoomItem1(
                Static=DataScienceDataRoomConfiguration(
                    id="lol",
                    title="lol",
                    description="lol",
                    enable_development=True,
                    enclave_root_certificate_pem="lol",
                    enclave_specifications=[],
                    nodes=[],
                    participants=[],
                )
            )
        )
    )
    output = compiler.compile_data_science_data_room(example)
    verified = compiler.verify_data_room(
        data_room=output.data_room,
        commits=output.commits,
        high_level=output.datascience_data_room_encoded,
        version=0,
    )
    assert example == verified
