from pyzettel.utils import generate_id
from datetime import datetime
import uuid

def test_generate_id():
    dt = datetime(2021, 8, 1, 12, 0, 0)
    my_uuid = uuid.UUID(bytes = b"\x00" * 16)
    id_template = "{{now | hexdate(12)}}"
    assert generate_id(id_template, dt) == "017b0127f100"
    id_template = "{{now | intdate(14)}}"
    assert generate_id(id_template, dt) == "01627812000000"
    id_template = "{{uuid}}"
    assert generate_id(id_template, dt, my_uuid=my_uuid) == "00000000-0000-0000-0000-000000000000"
    id_template = "{{now | hexdate(12)}}-{{uuid}}"
    assert generate_id(id_template, dt, my_uuid=my_uuid) == "017b0127f100-00000000-0000-0000-0000-000000000000"
    id_template = "{{now | intdate(14)}}-{{uuid}}"
    assert generate_id(id_template, dt, my_uuid=my_uuid) == "01627812000000-00000000-0000-0000-0000-000000000000"