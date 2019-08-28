"""Asset Panda Connector
Collect Asset Panda information using an API Token
"""

from runners.helpers import db, log
from runners.helpers.dbconfig import ROLE as SA_ROLE

from datetime import datetime

import snowflake
import requests
from urllib.error import HTTPError
from .utils import yaml_dump

PAGE_SIZE = 50


CONNECTION_OPTIONS = [
    {
        'name': 'api_token',
        'title': "Asset Panda API Token",
        'prompt': "Your Asset Panda API Token",
        'type': 'str',
        'secret': True,
        'required': True,
    },
]

LANDING_TABLE_COLUMNS= [
    ('INSERT_ID', 'NUMBER IDENTITY START 1 INCREMENT 1'),
    ('SNAPSHOT_AT', 'TIMESTAMP_LTZ(9)'),
    ('RAW', 'VARIANT'),
    ('DEPARTMENT', 'VARIANT'),
    ('STATUS', 'VARIANT'),
    ('ASSIGNED_TO', 'VARIANT'),
    ('BUILDING', 'VARIANT'),
    ('CATEGORY', 'VARIANT'),
    ('GPS_COORDINATES', 'VARIANT'),
    ('DEFAULT_ATTACHMENT', 'VARIANT'), 
    ('ROOM', 'VARIANT'),
    ('ENTITY', 'VARIANT'),
    ('ID', 'VARCHAR(256)'),
    ('STORAGE_CAPACITY', 'VARCHAR(256)'),
    ('ASSET_TAG_NUMBER', 'VARCHAR(256)'),
    ('PURCHASE_FROM', 'VARCHAR(256)'),
    ('DISPLAY_WITH_SECONDARY', 'VARCHAR(256)'),
    ('DISPLAY_NAME', 'VARCHAR(256)'),
    ('BRAND', 'VARCHAR(256)'),
    ('SHARE_URL', 'VARCHAR(256)'),
    ('CREATED_BY', 'VARCHAR(256)'),
    ('DESCRIPTION', 'VARCHAR(256)'),
    ('CHANGED_BY', 'VARCHAR(256)'),
    ('WIRELESS_STATUS', 'VARCHAR(256)'),
    ('NOTES', 'VARCHAR(256)'),
    ('WIFI_MAC_ADDRESS', 'VARCHAR(256)'),
    ('DISPLAY_SIZE', 'VARCHAR(256)'),
    ('OPERATING_SYSTEM', 'VARCHAR(256)'),
    ('SERIAL', 'VARCHAR(256)'),
    ('IMEI_MEID', 'VARCHAR(256)'),
    ('MODEL', 'VARCHAR(256)'),
    ('MAC_ADDRESS', 'VARCHAR(256)'),
    ('PO', 'VARCHAR(256)'),
    ('DATE_ADDED', 'TIMESTAMP_LTZ(9)'),
    ('CREATED_AT', 'TIMESTAMP_LTZ(9)'),
    ('UPDATED_AT', 'TIMESTAMP_LTZ(9)'),
    ('ASSET_PANDA_NUMBER', 'NUMBER(38,0)'),
    ('YUBIKEY_IDENTIFIER', 'NUMBER(38,0)'),
    ('OBJECT_VERSION_IDS', 'NUMBER(38,0)'),
    ('PURCHASE_PRICE', 'DATE'),
    ('PURCHASE_DATE', 'DATE'),
    ('CREATION_DATE', 'DATE'),
    ('NEXT_SERVICE', 'DATE'),
    ('CHANGE_DATE', 'DATE'),
    ('END_OF_LIFE_DATE', 'DATE'),
    ('IS_LOCKED', 'BOOLEAN'),
    ('IS_DELETABLE', 'BOOLEAN'),
    ('HAS_AUDIT_HISTORY', 'BOOLEAN'),
    ('OBJECT_APPRECIATION', 'BOOLEAN'),
    ('LOANER_POOL', 'BOOLEAN'),
    ('OBJECT_DEPRECIATION', 'BOOLEAN'),
    ('IS_EDITABLE', 'BOOLEAN'),
]


def get_data(token: str, url: str, params: dict = {}) -> dict:
    headers: dict = {"Authorization": f"Bearer {token}"}
    try:
        log.debug(f"Preparing GET: url={url} with params={params}")
        req = requests.get(url, params=params, headers=headers)
        req.raise_for_status()
    except HTTPError as http_err:
        log.error(f"Error GET: url={url}")
        log.error(f"HTTP error occurred: {http_err}")
        raise http_err
    try:
        json = req.json()
    except Exception as json_error:
        log.debug(f"JSON error occurred: {json_error}")
        log.debug(f"requests response {req}")
        json = {}
    return json

def connect(connection_name, options):
    landing_table = f'data.assetpanda_{connection_name}_connection'
    comment = yaml_dump(module='meraki_devices', **options)

    db.create_table(name=landing_table,
                    cols=LANDING_TABLE_COLUMNS, comment=comment)
    db.execute(f'GRANT INSERT, SELECT ON {landing_table} TO ROLE {SA_ROLE}')
    return {
        'newStage': 'finalized',
        'newMessage': "Asset Panda ingestion tables created!",
    }


def ingest(table_name, options):
    landing_table = f'data.{table_name}'
    timestamp = datetime.utcnow()
    api_key = options['api_token']
    url_objet = 
    url_metadata = 

    params: dict = {
        "limit": PAGE_SIZE,
        "page": 1,  # API starts at 1
    }

    dict_objects: dict = get_data(api_key, url_objet, params)

    dict_fields: dict = get_data(api_key, url_metadata)
    list_field: list = dict_fields["fields"]

    db.insert(
        landing_table,
        values=[(
            timestamp,
            device,
            device.get('department'),
            device.get('status'),
            device.get('assignedTo'),
            device.get('building'),
            device.get('category'),
            device.get('gpsCoordinates'),
            device.get('defaultAttachment'),
            device.get('room'),
            device.get('entity'),
            device.get('id'),
            device.get('storageCapacity'),
            device.get('assetTagNumber'),
            device.get('purchaseFrom'),
            device.get('displayWithSecondary'),
            device.get('displayName'),
            device.get('brand'),
            device.get('shareUrl'),
            device.get('createdBy'),
            device.get('description'),
            device.get('changedBy'),
            device.get('wirelessStatus'),
            device.get('notes'),
            device.get('wifiMacAddress'),
            device.get('displaySize'),
            device.get('operationSystem'),
            device.get('serial'),
            device.get('imeiMeid'),
            device.get('model'),
            device.get('macAddress'),
            device.get('po'),
            device.get('dateAdded'),
            device.get('createdAt'),
            device.get('updatedAt'),
            device.get('assetPandaNumber'),
            device.get('yubikeyIdentifier'),
            device.get('objectVersionIds'),
            device.get('purchasePrice'),
            device.get('purchaseDate'),
            device.get('creationDate'),
            device.get('nextService'),
            device.get('changeDate'),
            device.get('endOfLifeDate'),
            device.get('isLocked'),
            device.get('isDeletable'),
            device.get('hasAuditHistory'),
            device.get('objectAppreciation'),
            device.get('loanerPool'),
            device.get('objectDepreciation'),
            device.get('isEditable'),

        ) for device in devices],
        select=db.derive_insert_select(LANDING_TABLE_COLUMNS),
        columns=db.derive_insert_columns(LANDING_TABLE)
    )
    log.info(f'Inserted {len(devices)} rows (devices).')
    yield len(devices)