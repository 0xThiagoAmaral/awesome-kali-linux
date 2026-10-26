#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Acquire the complete pinned main manpage, preserving its own copying notice."""
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
        name=next(n for n in z.namelist() if n.endswith('/arp-scan.1.dist')); data=z.read(name)
    markdown,evidence=prepare_extended_roff(data.decode(),'arp-scan')
    assert evidence['sections']==['NAME','SYNOPSIS','DESCRIPTION','OPTIONS','EXIT STATUS','FILES','EXAMPLES','SEE ALSO']
    assert len(evidence['option_syntax'])==42 and len(evidence['subsections'])==13
    assert len(evidence['tables'])==6 and len(evidence['equations'])==1 and len(evidence['literal_blocks'])==8
    assert evidence['all_source_text_accounted']
    notice=evidence['license_notice'].encode()
    expected=(cache/'docs/LICENSE.arp-fingerprint-manpage.txt').read_bytes()
    assert notice==expected,'Main manual notice differs; copying conditions need a separate review'
    filename='LICENSE.arp-scan-manpage.txt'
    (cache/'docs/arp-scan.1.dist').write_bytes(data)
    (cache/'docs'/filename).write_bytes(notice)
    (ROOT/'LICENSES/LicenseRef-ARP-Scan-Manpage.txt').write_bytes(notice)
    original=ROOT/'sources/upstream/arp-scan/arp-scan.1.dist.source'; original.write_bytes(data)
    doc={'path':'arp-scan.1.dist','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'source_url':record['repository']+'/blob/'+record['commit']+'/arp-scan.1.dist',
         'language':'en','source_format':'man-roff-extended-v1','license_spdx':'LicenseRef-ARP-Scan-Manpage',
         'license_asset':filename,'runtime_evidence_file':'arp-scan-main-tests.json'}
    asset={'path':filename,'bytes':len(notice),'sha256':hashlib.sha256(notice).hexdigest(),
           'source_url':doc['source_url'],'language':'en','role':'file-specific-copyright-and-copying-notice'}
    record['documents']=[d for d in record['documents'] if d['path']!=doc['path']]+[doc]
    record['assets']=[a for a in record['assets'] if a['path']!=filename]+[asset]
    record['source_scope']='Pinned README plus complete arp-fingerprint.1 and main arp-scan.1.dist manuals, each with its own preserved copying notice. Wiki, additional utilities and remaining sources still require coverage review.'
    path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (cache/'source.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'evidence/arp-scan-main-acquisition.json').write_text(json.dumps({
        'source_sha256':doc['sha256'],'commit':record['commit'],'license_spdx':doc['license_spdx'],
        'sections':evidence['sections'],'options':42,'subsections':13,'tables':6,'equations':1,
        'literal_blocks':8,'all_source_text_accounted':True,'roff_tbl_eqn_executed':False},indent=2)+'\n',
        encoding='utf-8',newline='\n')
    print(json.dumps({'main_manual_acquired':True,'sections':8,'options':42,'tables':6,'equations':1}))

if __name__=='__main__':
    main()
