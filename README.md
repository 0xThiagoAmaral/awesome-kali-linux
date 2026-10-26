# Awesome Kali Linux

> Curadoria em português de ferramentas e referências do Kali Linux, com um vault Obsidian para consulta e estudo offline.

**Projeto independente, inspirado no formato Awesome. Não afiliado ao Kali/OffSec e ainda não submetido à lista Awesome.**

## Comece aqui

- [Abrir a home do vault](vault/00-Home.md).
- [Configurar o Obsidian](OBSIDIAN-SETUP.md).
- [Consultar o catálogo completo](docs/catalogo-kali.md).
- [Acompanhar a cobertura e as pendências](docs/COBERTURA.md).
- [Contribuir](CONTRIBUTING.md).

## Escopo e situação

- **32 recursos na curadoria inicial**: descrições autorais curtas e links oficiais.
- **820 registros no catálogo oficial versionado**, dos quais 806 indicam associação a `kali-linux-everything`.
- **Dois módulos-piloto offline em português**: Nmap e ffuf, com evidência de testes locais limitados.
- **Documentação integral de todas as ferramentas em português ainda não concluída.**

A lista Awesome é curada; o catálogo separado busca cobertura. Um link externo não conta como documentação offline.
O objetivo continua sendo preservar a estrutura das fontes oficiais, traduzir o texto explicativo com fidelidade
e manter comandos, opções, código e saídas originais sem alterações silenciosas.

## Conteúdo

- [Fontes oficiais](#fontes-oficiais)
- [Reconhecimento e rede](#reconhecimento-e-rede)
- [Web e APIs](#web-e-apis)
- [Windows e Active Directory](#windows-e-active-directory)
- [Senhas e hashes](#senhas-e-hashes)
- [Reversão e análise de binários](#reversão-e-análise-de-binários)
- [Forense e tráfego](#forense-e-tráfego)
- [Redes sem fio](#redes-sem-fio)
- [Vault offline](#vault-offline)
- [Contribuição e licenças](#contribuição-e-licenças)

## Fontes oficiais

- [Kali Linux](https://www.kali.org/) — Portal oficial da distribuição.
- [Documentação do Kali](https://www.kali.org/docs/) — Referência de instalação, administração e uso.
- [Kali Tools](https://www.kali.org/tools/) — Referência oficial de pacotes, binários e exemplos.
- [Metapacotes](https://www.kali.org/docs/general-use/metapackages/) — Diferenças entre default, large e everything.

## Reconhecimento e rede

- [Amass](https://www.kali.org/tools/amass/) — Mapeamento de superfície externa e ativos.
- [Nmap](https://www.kali.org/tools/nmap/) — Descoberta de portas e identificação de serviços.
- [Subfinder](https://www.kali.org/tools/subfinder/) — Enumeração de subdomínios a partir de fontes passivas.
- [theHarvester](https://www.kali.org/tools/theharvester/) — Coleta de informações de fontes abertas.

## Web e APIs

- [Burp Suite](https://www.kali.org/tools/burpsuite/) — Inspeção e testes de aplicações web.
- [Feroxbuster](https://www.kali.org/tools/feroxbuster/) — Descoberta recursiva de conteúdo web.
- [ffuf](https://www.kali.org/tools/ffuf/) — Fuzzing HTTP com entradas de wordlists.
- [Gobuster](https://www.kali.org/tools/gobuster/) — Enumeração orientada a wordlists.
- [Nuclei](https://www.kali.org/tools/nuclei/) — Verificações baseadas em templates.
- [SQLMap](https://www.kali.org/tools/sqlmap/) — Automação de testes de injeção SQL.
- [ZAP](https://www.kali.org/tools/zaproxy/) — Proxy e plataforma de testes web.

## Windows e Active Directory

- [BloodHound.py](https://www.kali.org/tools/bloodhound.py/) — Coleta de relações para análise de Active Directory.
- [Impacket](https://www.kali.org/tools/impacket/) — Bibliotecas e utilitários para protocolos de rede.
- [NetExec](https://www.kali.org/tools/netexec/) — Avaliação de serviços de rede em ambientes corporativos.
- [Responder](https://www.kali.org/tools/responder/) — Estudo de resolução de nomes e autenticação em redes locais.

## Senhas e hashes

- [Hashcat](https://www.kali.org/tools/hashcat/) — Recuperação e análise de hashes.
- [Hydra](https://www.kali.org/tools/hydra/) — Testes de autenticação em múltiplos protocolos.
- [John the Ripper](https://www.kali.org/tools/john/) — Recuperação de senhas e análise de formatos de hash.

## Reversão e análise de binários

- [Binwalk](https://www.kali.org/tools/binwalk/) — Análise e identificação de estruturas em firmware.
- [GDB](https://www.kali.org/tools/gdb/) — Depuração de programas.
- [Ghidra](https://www.kali.org/tools/ghidra/) — Análise e engenharia reversa de binários.
- [radare2](https://www.kali.org/tools/radare2/) — Conjunto de utilitários de análise de binários.

## Forense e tráfego

- [Sleuth Kit](https://www.kali.org/tools/sleuthkit/) — Análise de sistemas de arquivos e imagens de disco.
- [tcpdump](https://www.kali.org/tools/tcpdump/) — Captura e inspeção de pacotes.
- [Wireshark](https://www.kali.org/tools/wireshark/) — Análise gráfica de protocolos e capturas.
- [YARA](https://www.kali.org/tools/yara/) — Identificação de padrões por regras.

## Redes sem fio

- [Aircrack-ng](https://www.kali.org/tools/aircrack-ng/) — Ferramentas para análise de redes IEEE 802.11.
- [Kismet](https://www.kali.org/tools/kismet/) — Monitoramento e descoberta de redes sem fio.

## Vault offline

Extraia a pasta completa e abra a subpasta `vault` no Obsidian. A leitura dos módulos já incluídos
não requer plugins comunitários nem APIs. Links oficiais oferecem material adicional online.

- [Nmap — documentação-piloto](vault/02-Tools/nmap/nmap-guia.md) · [cheatsheet](vault/02-Tools/nmap/nmap-cheatsheet.md).
- [ffuf — documentação-piloto](vault/02-Tools/ffuf/ffuf-guia.md) · [cheatsheet](vault/02-Tools/ffuf/ffuf-cheatsheet.md).
- [Padrão editorial](EDITORIAL.md) · [Plano de expansão](PLANO_DO_PROJETO.md) · [Roadmap](ROADMAP.md).

Validar localmente, na raiz do repositório:

```bash
# Bash · raiz do repositório · Linux/WSL · Python 3.10+
python3 scripts/validate_vault.py
python3 scripts/check_readme_contract.py README.md
```

## Contribuição e licenças

Inclua referências oficiais e explique por que cada recurso merece entrar na curadoria.
Não copie manuais completos sem confirmar permissões específicas; indique tradução/adaptação e procedência.
Curadoria e notas autorais: CC BY-SA 4.0; scripts: MIT. Conteúdos upstream mantêm suas próprias licenças e avisos.

[Como contribuir](CONTRIBUTING.md) · [Política de licenças](LICENSE-POLICY.md) · [Situação das fontes](docs/COPYRIGHT-STATUS.md).
## Documentação offline — andamento


Já há **51 documentos de 27 ferramentas** no
[acervo offline](vault/01-Maps/documentacao-offline.md), com originais, licenças e hashes.
São traduções automáticas, traduções editoriais por assistente de IA ou português fornecido upstream, devidamente identificados.
O acervo também inclui **10 folhas de comandos** com exemplos oficiais e procedência verificável.
Há ainda **9 cheatsheets autorais complementares**, com limites de validação explícitos.
Isso **não** significa documentação integral das 820 ferramentas nem revisão humana concluída.

[Cobertura por ferramenta](catalog/documentation-coverage.csv) ·
[Metodologia e direitos](THIRD_PARTY.md) · [Licenças](LICENSE-POLICY.md).
