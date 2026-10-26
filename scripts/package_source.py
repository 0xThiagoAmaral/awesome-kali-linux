#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Truthful provenance and byte validation for selected installed package sources."""
import gzip
import hashlib
import json

FIELDS=('source_kind','package','binary_version','source_package','source_version','source_snapshot_sha256')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def package_fields(record):
    if record.get('source_kind')!='installed-kali-package':
        return {'source_commit':record['commit']}
    return {key:record[key] for key in FIELDS}

def validate_package_source(record,assets):
    assert record['source_kind']=='installed-kali-package'
    assert record.get('commit') is None and record.get('git_commit') is None,'Native source cannot assert a Git commit'
    assert record['license_review_status']=='verified-selected-manual'
    path=assets/record['source_snapshot_asset']
    assert path.resolve().is_relative_to(assets.resolve())
    data=path.read_bytes()
    assert sha(data)==record['source_snapshot_sha256'],'Snapshot hash'
    snapshot=json.loads(data)
    if 'license_spdx' in snapshot:
        assert snapshot['license_spdx']==record['license_spdx'],'License choice differs from snapshot'
    assert snapshot.get('required_acknowledgement')==record.get('required_acknowledgement'),'Required acknowledgement binding'
    for field in FIELDS[:-1]:
        assert snapshot[field]==record[field],field
    assert snapshot['documents']==record['documents'],'Document provenance differs from snapshot'
    assert snapshot['license_review']==record['license_review'],'License review binding'
    for file in snapshot['retained_files']:
        path=assets/file['path']
        assert path.resolve().is_relative_to(assets.resolve())
        assert sha(path.read_bytes())==file['sha256'],file['path']
    for doc in record['documents']:
        data=(assets/doc['compressed_asset']).read_bytes()
        assert sha(data)==doc['compressed_sha256'],'Compressed original hash'
        assert sha(gzip.decompress(data))==doc['sha256'],'Decompressed original hash'
    assert sha((assets/'COPYRIGHT.package.txt').read_bytes())==record['copyright_sha256']
    assert sha((assets/'LICENSE.txt').read_bytes())==record['license_sha256']
    return True
