#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire the complete pinned get-oui manual without fetching IEEE registry data."""
import argparse,hashlib,json,pathlib,zipfile
from roff_extended_manual import prepare_extended_roff

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--cache',type=pathlib.Path,required=True)
    args=parser.parse_args()
    path=ROOT/'catalog/source-registry.json'
    registry=json.loads(path.read_text(encoding='utf-8')); record=registry['arp-scan']
    cache=args.cache/'arp-scan'; archive=cache/(record['commit']+'.zip')
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        name=next(n for n in z.namelist() if n.endswith('/get-oui.1.dist')); data=z.read(name)
    assert hashlib.sha256(data).hexdigest()=='88cd4df36ba67aadfe42d7b2774aeada2b5984c763372f5aa71987bd02c776a7'
    prepared,evidence=prepare_extended_roff(data.decode(),'arp-scan')
    assert evidence['sections']==['NAME','SYNOPSIS','DESCRIPTION','OPTIONS','FILES','EXAMPLES','NOTES','SEE ALSO']
    assert evidence['option_syntax']==['-h','-f <fn>','-v']
    assert len(evidence['tables'])==1 and len(evidence['literal_blocks'])==3
    notice=evidence['license_notice'].encode()
    assert notice==(cache/'docs/LICENSE.arp-scan-manpage.txt').read_bytes()
    filename='LICENSE.get-oui-manpage.txt'
    (cache/'docs/get-oui.1.dist').write_bytes(data)
    (cache/'docs'/filename).write_bytes(notice)
    (ROOT/'LICENSES/LicenseRef-Get-OUI-Manpage.txt').write_bytes(notice)
    (ROOT/'sources/upstream/arp-scan/get-oui.1.dist.source').write_bytes(data)
    doc={'path':'get-oui.1.dist','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'source_url':record['repository']+'/blob/'+record['commit']+'/get-oui.1.dist',
         'language':'en','source_format':'man-roff-extended-v1','license_spdx':'LicenseRef-Get-OUI-Manpage',
         'license_asset':filename,'runtime_evidence_file':'get-oui-help-tests.json'}
    asset={'path':filename,'bytes':len(notice),'sha256':hashlib.sha256(notice).hexdigest(),
           'source_url':doc['source_url'],'language':'en','role':'file-specific-copyright-and-copying-notice'}
    record['documents']=[d for d in record['documents'] if d['path']!=doc['path']]+[doc]
    record['assets']=[a for a in record['assets'] if a['path']!=filename]+[asset]
    record['source_scope']='Pinned README plus full arp-scan, arp-fingerprint and get-oui manpages, with individual copying notices. Wiki and other sources remain a separate coverage review; IEEE data files are not mirrored by this acquisition.'
    path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'evidence/get-oui-manual-acquisition.json').write_text(json.dumps({
        'source_sha256':doc['sha256'],'commit':record['commit'],'license_spdx':doc['license_spdx'],
        'sections':evidence['sections'],'options':evidence['option_syntax'],'tables':1,'literal_blocks':3,
        'all_source_text_accounted':evidence['all_source_text_accounted'],'ieee_data_fetched':False},indent=2)+'\n',
        encoding='utf-8',newline='\n')
    print(json.dumps({'manual_acquired':True,'sections':8,'options':3,'tables':1,'ieee_data_fetched':False}))

if __name__=='__main__':
    main()
