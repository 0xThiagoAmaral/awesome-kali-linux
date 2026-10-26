---
title: "Nmap — troubleshooting"
type: "troubleshooting"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["fieldbook"]
cssclasses: ["fieldbook"]
tool: "nmap"
installed_version: "7.99+dfsg-1kali1"
test_status: "not-run"
---

# Nmap — troubleshooting

| Observação | Verificação |
|---|---|
| Porta fechada | O fixture iniciou na porta correta? |
| Nome de host não resolve | Separar DNS de conectividade; usar localhost no teste reproduzível. |
| Opção exige privilégios | O piloto usa `-sT`; outras técnicas têm requisitos próprios. |
| Identificação genérica | Serviço pode não fornecer uma assinatura reconhecível. |

Não trocar rede/DNS ou reiniciar WSL como primeira reação a qualquer resultado.
[Guia](nmap-guia.md) · [fontes](nmap-fontes.md).
