# Copyright 2023 Agnostiq Inc.


from typing import Optional
from covalent_cloud.shared.classes.exceptions import handle_error
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.shared.schemas.volume import BaseVolume, Volume
from covalent_cloud import get_client


def volume(name: str, settings: Optional[Settings] = settings):
    """Return the persistent volume in the file system containing path

    :param name: name of volume
    :return: volume id of the file system containing path
    """
    try:
        # will check if name is valid else throw error
        volume = BaseVolume(name=name)

        #should be valid name without any slashes since the validator cleaned it
        volume_name = volume.name

        client = get_client(settings)
        response = client.post(
            "/api/v2/volumes",
            request_options={"json": {"name": volume_name}}
        )

        data = response.json()
        volume = Volume(**data)
        return volume
    except Exception as e:
        handle_error(e)

