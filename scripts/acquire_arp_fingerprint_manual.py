#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire the pinned arp-fingerprint manual and its file-specific copying notice."""
import argparse,hashlib,json,pathlib,zipfile
from roff_manual import prepare_roff_manual

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache',type=pathlib.Path,required=True)
    args=parser.parse_args()
    path=ROOT/'catalog/source-registry.json'
    registry=json.loads(path.read_text(encoding='utf-8'))
    record=registry['arp-scan']; cache=args.cache/'arp-scan'
    archive=cache/(record['commit']+'.zip')
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        name=next(n for n in z.namelist() if n.endswith('/arp-fingerprint.1'))
        data=z.read(name)
    markdown,evidence=prepare_roff_manual(data.decode('utf-8'),'arp-scan')
    assert evidence['sections']==['NAME','SYNOPSIS','DESCRIPTION','OPTIONS','EXAMPLES','NOTES','SEE ALSO']
    assert evidence['option_syntax']==['-h','-v','-o <option-string>','-l','-m']
    assert len(evidence['literal_blocks'])==4
    notice=evidence['license_notice'].encode()
    assert b'Copyright (C) Roy Hills' in notice
    assert b'Copying and distribution of this file, with or without modification,' in notice
    assert b'are permitted in any medium without royalty provided the copyright' in notice
    assert b'notice and this notice are preserved.' in notice
    dest=cache/'docs/arp-fingerprint.1'; dest.write_bytes(data)
    license_path='LICENSE.arp-fingerprint-manpage.txt'
    (cache/'docs'/license_path).write_bytes(notice)
    (ROOT/'LICENSES/LicenseRef-ARP-Fingerprint-Manpage.txt').write_bytes(notice)
    doc={'path':'arp-fingerprint.1','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'source_url':record['repository']+'/blob/'+record['commit']+'/arp-fingerprint.1',
         'language':'en','source_format':'man-roff-v1',
         'license_spdx':'LicenseRef-ARP-Fingerprint-Manpage','license_asset':license_path}
    asset={'path':license_path,'bytes':len(notice),'sha256':hashlib.sha256(notice).hexdigest(),
           'source_url':doc['source_url'],'language':'en','role':'file-specific-copyright-and-copying-notice'}
    record['documents']=[x for x in record['documents'] if x['path']!=doc['path']]+[doc]
    record['assets']=[x for x in record['assets'] if x['path']!=license_path]+[asset]
    record['source_scope']='Pinned README and full arp-fingerprint.1 manual; manpage has its own preserved copying notice, not the repository GPL notice. Wiki and main arp-scan reference coverage remain pending.'
    path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'evidence/arp-fingerprint-manual-acquisition.json').write_text(json.dumps({
        'commit':record['commit'],'source_sha256':doc['sha256'],'license_spdx':doc['license_spdx'],
        'license_notice_sha256':asset['sha256'],'license_notice_asset':license_path,
        'sections':evidence['sections'],'options':evidence['option_syntax'],'literal_blocks':4,
        'roff_executed':False,'all_source_text_accounted':True},indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'tool':'arp-scan','binary':'arp-fingerprint','full_reference_manual_acquired':True,
                      'sections':7,'options':5,'license_spdx':doc['license_spdx'],'roff_executed':False}))

if __name__=='__main__':
    main()
