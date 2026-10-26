---
title: "TCP connect"
type: "concept"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["fieldbook"]
cssclasses: ["fieldbook"]
---

# TCP connect

Uma conexão TCP pode ser iniciada pela API de sockets do sistema operacional.
O Nmap usa essa abordagem em `-sT`, sem exigir os raw sockets de outras técnicas.
Um resultado `open` indica aceitação da conexão, não a existência de uma vulnerabilidade.

Aplicação: [guia Nmap](../02-Tools/nmap/nmap-guia.md).
Fonte: [Nmap — scan techniques](https://nmap.org/book/man-port-scanning-techniques.html).
