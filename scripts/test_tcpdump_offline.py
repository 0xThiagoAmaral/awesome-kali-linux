#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exercise tcpdump only on a synthetic owned PCAP. Never opens a live capture."""
import argparse,hashlib,json,os,pathlib,re,shutil,socket,struct,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def checksum(data):
    if len(data)%2:data+=b'\0'
    value=sum(struct.unpack('!'+str(len(data)//2)+'H',data))
    while value>>16:value=(value&0xffff)+(value>>16)
    return (~value)&0xffff
def ipv4(payload,protocol,source,destination,ident):
    src=socket.inet_aton(source);dst=socket.inet_aton(destination)
    header=struct.pack('!BBHHHBBH4s4s',0x45,0,20+len(payload),ident,0x4000,64,protocol,0,src,dst)
    header=header[:10]+struct.pack('!H',checksum(header))+header[12:]
    return header+payload
def fixture_bytes():
    src=b'\x02\0\0\0\0\x10';dst=b'\x02\0\0\0\0\x20'
    arp=struct.pack('!HHBBH',1,0x0800,6,4,1)+src+socket.inet_aton('192.0.2.10')+b'\0'*6+socket.inet_aton('192.0.2.1')
    arp_frame=b'\xff'*6+src+struct.pack('!H',0x0806)+arp
    tcp=struct.pack('!HHIIBBHHH',12345,80,1,0,0x50,0x02,64240,0,0)
    pseudo=socket.inet_aton('192.0.2.10')+socket.inet_aton('198.51.100.20')+struct.pack('!BBH',0,6,len(tcp))
    tcp=tcp[:16]+struct.pack('!H',checksum(pseudo+tcp))+tcp[18:]
    tcp_frame=dst+src+struct.pack('!H',0x0800)+ipv4(tcp,6,'192.0.2.10','198.51.100.20',1)
    dns=struct.pack('!HHHHHH',0x1234,0x0100,1,0,0,0)+b'\x07example\x07invalid\0'+struct.pack('!HH',1,1)
    udp=struct.pack('!HHHH',53000,53,8+len(dns),0)+dns
    pseudo=socket.inet_aton('192.0.2.10')+socket.inet_aton('198.51.100.53')+struct.pack('!BBH',0,17,len(udp))
    udp=udp[:6]+struct.pack('!H',checksum(pseudo+udp) or 0xffff)+udp[8:]
    udp_frame=dst+src+struct.pack('!H',0x0800)+ipv4(udp,17,'192.0.2.10','198.51.100.53',2)
    data=struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1)
    for index,packet in enumerate([arp_frame,tcp_frame,udp_frame]):
        data+=struct.pack('<IIII',1700000000+index,0,len(packet),len(packet))+packet
    return data
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args()
    assert shutil.which('tcpdump')
    record=json.loads((ROOT/'catalog/source-registry.json').read_text(encoding='utf-8'))['tcpdump'];doc=record['documents'][0]
    manual=pathlib.Path(doc['installed_path']);manual_before=sha(manual.read_bytes())
    commands=[];checks=[]
    with tempfile.TemporaryDirectory(prefix='tcpdump-offline-') as temporary:
        temp=pathlib.Path(temporary);capture=temp/'fixture.pcap';payload=fixture_bytes();capture.write_bytes(payload)
        env=dict(os.environ,LC_ALL='C',TZ='UTC',HOME=temporary)
        def run(label,argv,expected=0):
            # No caller accepts live interface/capture arguments.
            assert '-i' not in argv
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=20,cwd=temporary,env=env)
            commands.append({'label':label,'argv':[x.replace(temporary,'<TEST_DIR>') for x in argv],
                'stdout':p.stdout.replace(temporary,'<TEST_DIR>'),'stderr':p.stderr.replace(temporary,'<TEST_DIR>'),
                'exit_status':p.returncode,'expected_exit_status':expected})
            checks.append({'check':label+' exit status','pass':p.returncode==expected})
            return p
        run('help',['tcpdump','--help'])
        version=run('version',['tcpdump','--version']).stdout
        package=run('package-version',['dpkg-query','-W','-f='+chr(36)+'{Version}','tcpdump']).stdout
        shown=run('read-all',['tcpdump','-nn','-tt','-r',str(capture)])
        lines=[s for s in shown.stdout.splitlines() if s.strip()]
        checks.append({'check':'Synthetic input decodes as three packets','pass':len(lines)==3,'observed_lines':len(lines)})
        for expression,wanted in [('tcp port 80',1),('udp port 53',1),('arp',1),('ip',2),('(tcp or udp) and port 53',1),('not ip',1)]:
            p=run('count '+expression,['tcpdump','-nn','--count','-r',str(capture),expression])
            match=re.fullmatch(r'\s*(\d+)(?:\s+packets?)?\s*',p.stdout)
            observed=int(match[1]) if match else None
            checks.append({'check':'Offline filter '+expression,'pass':observed==wanted,'expected_count':wanted,'observed_count':observed})
        output=temp/'tcp-only.pcap'
        run('write-filtered',['tcpdump','-nn','-r',str(capture),'-w',str(output),'tcp'])
        reread=run('read-filtered',['tcpdump','-nn','--count','-r',str(output)])
        match=re.fullmatch(r'\s*(\d+)(?:\s+packets?)?\s*',reread.stdout)
        checks.append({'check':'Filtered output contains one packet','pass':bool(match) and int(match[1])==1})
        run('compile-filter',['tcpdump','-nn','-d','-r',str(capture),'tcp'])
        invalid=run('invalid-filter',['tcpdump','-nn','-r',str(capture),'tcp and ('],expected=1)
        checks.append({'check':'Invalid filter reports syntax error','pass':'syntax error' in invalid.stderr.lower()})
        checks.append({'check':'Input PCAP bytes unchanged','pass':capture.read_bytes()==payload})
        output_hash=sha(output.read_bytes()) if output.exists() else None
    manual_after=sha(manual.read_bytes())
    checks.append({'check':'Installed manual bytes unchanged','pass':manual_before==manual_after==doc['compressed_sha256']})
    checks.append({'check':'Installed package matches recorded source','pass':package==record['binary_version']})
    result={'passed':all(c['pass'] for c in checks),'binary':'tcpdump','installed_version':version.splitlines()[0] if version else None,
        'test_status':'offline-fixture','commands':commands,'checks':checks,'fixture':'Synthetic owned Ethernet PCAP: ARP request, TCP SYN, UDP DNS query; reserved documentation addresses only',
        'fixture_sha256':sha(payload),'fixture_bytes':len(payload),'fixture_packets':3,'filtered_output_sha256':output_hash,
        'source_manual_sha256':doc['sha256'],'test_script':'scripts/test_tcpdump_offline.py','test_script_sha256':sha(pathlib.Path(__file__).read_bytes()),
        'manual_options_not_listed_by_installed_help':[],'installed_help_options_not_in_manual':[],
        'installed_manual_before_sha256':manual_before,'installed_manual_after_sha256':manual_after,
        'live_capture_requested':False,'packet_send_operation_requested':False,'temporary_directory_removed':not temp.exists(),
        'compatibility_summary_pt':'Ajuda/versão e leitura de PCAP sintético próprio verificadas. Filtros, contagem, gravação de cópia filtrada e rejeição de filtro inválido foram exercitados somente com -r. A ajuda compacta não foi tratada como lista integral de opções. Nenhuma captura ao vivo, interface ou envio foi solicitado.',
        'verification_scope_pt':'Teste offline limitado aos comandos registrados; não comprova todas as opções, protocolos ou backends.',
        'limits':['No live capture, interface enumeration, packet transmission or external DNS lookup was requested.',
                  'Only three synthetic protocol examples and selected offline filters tested; original historical examples were not executed.']}
    if args.record:
        fixture=ROOT/'vault/99-Assets/fixtures/tcpdump-demo.pcap'
        fixture.parent.mkdir(parents=True,exist_ok=True)
        fixture.write_bytes(payload)
        for path in [ROOT/'evidence/tcpdump-local-tests.json',ROOT/'vault/99-Assets/evidence/tcpdump-local-tests.json']:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
