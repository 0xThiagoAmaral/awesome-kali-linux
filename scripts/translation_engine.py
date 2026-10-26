#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Local English-to-Portuguese inference with cache; no network in this module."""
import hashlib
import json
import pathlib
import re
import sys

BT=chr(96)
PROTECTED=re.compile(BT+r'+[^'+BT+r']*'+BT+r'+|!?\[[^\]]*\]\([^)]+\)|<[^>]+>|https?://[^\s<>]+|\*\*|__|(?<!\w)[*_]|[*_](?!\w)|[\U0001F300-\U0001FAFF]|\b\d+(?:\.\d+)+\b|\b(?:ffuf|Gobuster|Subfinder|Nuclei|Naabu|Katana|Go|fuzzing|fuzzer|HTTP|HTTPS|DNS|TCP|UDP|API)\b')

def normalize_pt(text):
    text=text.replace(chr(9601),' ').strip()
    for old,new in {'ficheiros':'arquivos','ficheiro':'arquivo','utilizadores':'usuários','utilizador':'usuário',
                    'palavras-passe':'senhas','palavra-passe':'senha','ecrã':'tela','descarregar':'baixar'}.items():
        text=re.sub(r'\b'+re.escape(old)+r'\b',new,text,flags=re.I)
    return text

class LocalTranslator:
    def __init__(self,runtime):
        runtime=pathlib.Path(runtime)
        sys.path.insert(0,str(runtime/'lib'))
        import ctranslate2
        import sentencepiece
        self.runtime=runtime
        self.cache_file=runtime/'translation-cache.json'
        self.cache=json.loads(self.cache_file.read_text(encoding='utf-8')) if self.cache_file.exists() else {}
        self.cache={k:v.replace(chr(9601),' ').strip() for k,v in self.cache.items()}
        self.model=next((runtime/'model').glob('*/model'))
        self.sp=sentencepiece.SentencePieceProcessor(model_file=str(self.model.parent/'sentencepiece.model'))
        self.translator=ctranslate2.Translator(str(self.model),device='cpu',compute_type='int8',inter_threads=1,intra_threads=4)
        self.calls=0
        self.versions={'ctranslate2':ctranslate2.__version__,'sentencepiece':sentencepiece.__version__}
    def raw(self,text):
        if not re.search(r'[A-Za-z]{2,}',text) or len(text.strip())<2:
            return text
        if text in self.cache:
            self.cache[text]=normalize_pt(self.cache[text])
            return self.cache[text]
        tokens=self.sp.encode(text,out_type=str)
        if len(tokens)>450:
            parts=re.split(r'(?<=[.!?])\s+',text)
            if len(parts)==1:
                words=text.split()
                parts=[' '.join(words[i:i+100]) for i in range(0,len(words),100)]
            result=' '.join(self.raw(p) for p in parts)
        else:
            result=self.sp.decode_pieces(self.translator.translate_batch([tokens],beam_size=4,max_input_length=0,
                                  max_decoding_length=min(1024,max(64,len(tokens)*3)))[0].hypotheses[0]).replace(chr(9601),' ').strip()
        glossary={'ficheiros':'arquivos','ficheiro':'arquivo','utilizadores':'usuários','utilizador':'usuário',
                  'palavras-passe':'senhas','palavra-passe':'senha','ecrã':'tela','descarregar':'baixar'}
        for old,new in glossary.items():
            result=re.sub(r'\b'+re.escape(old)+r'\b',new,result,flags=re.I)
        self.cache[text]=result
        self.calls+=1
        if self.calls%20==0:
            self.flush()
            print('TRANSLATED_SEGMENTS='+str(self.calls),flush=True)
        return result
    def text(self,text):
        def label(match):
            if match.group(0).startswith('!'):
                return match.group(0)
            title=match.group(1)
            if title in ['ffuf','Gobuster','Subfinder','Nuclei','Go','GitHub','Docker']:
                return match.group(0)
            def label_code(m):
                value=m.group(1)
                if value.startswith('-') or '/' in value or re.search(r'\d+\.\d+|\.[a-z]{2,}',value):
                    return m.group(0)
                return BT+self.raw(value)+BT
            title=re.sub(BT+'([^'+BT+']+)'+BT,label_code,title)
            return '['+self.text(title)+']('+match.group(2)+')'
        text=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',label,text)
        literals=[]
        def hide(match):
            literals.append(match.group())
            return 'ZXQ'+str(len(literals)-1)+'QXZ'
        protected=PROTECTED.sub(hide,text)
        result=self.raw(protected)
        if all(result.count('ZXQ'+str(i)+'QXZ')==1 for i in range(len(literals))):
            for i,value in enumerate(literals):
                result=result.replace('ZXQ'+str(i)+'QXZ',value)
            return result
        # Fallback retains every literal byte-for-byte, trading fluency for integrity.
        parts=[]
        pos=0
        for m in PROTECTED.finditer(text):
            chunk=text[pos:m.start()]
            if chunk:
                lead=chunk[:len(chunk)-len(chunk.lstrip())]
                trail=chunk[len(chunk.rstrip()):]
                parts.append(lead+self.raw(chunk.strip())+trail)
            parts.append(m.group())
            pos=m.end()
        chunk=text[pos:]
        if chunk:
            lead=chunk[:len(chunk)-len(chunk.lstrip())]
            trail=chunk[len(chunk.rstrip()):]
            parts.append(lead+self.raw(chunk.strip())+trail)
        return ''.join(parts)
    def flush(self):
        self.cache_file.write_text(json.dumps(self.cache,ensure_ascii=False,indent=2)+'\n',encoding='utf-8', newline='\n')
    def provenance(self):
        model=json.loads((self.runtime/'model-provenance.json').read_text(encoding='utf-8'))
        return {'engine':'Argos EN-PT model through CTranslate2','model_sha256':model['model_sha256'],
                'model_source':model['download_url'],'packages':self.versions,'paid_api_used':False,
                'inference_network_requests':0,'review_status':'machine-translation-not-human-reviewed',
                'editorial_adjustments':['SentencePiece whitespace decoded as in Argos tokenizer','Limited PT-BR terminology glossary; commands and URLs protected']}

if __name__=='__main__':
    tr=LocalTranslator(sys.argv[1])
    sample='This tool finds files and directories. Keep the command unchanged.'
    print(json.dumps({'source':sample,'translation':tr.text(sample),'provenance':tr.provenance()},ensure_ascii=False,indent=2))
    tr.flush()
