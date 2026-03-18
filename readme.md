<h1 align="center">
  Urna Eletrônica Brasileira (Simulador) 🗳️
</h1>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" />
  <img alt="Tkinter" src="https://img.shields.io/badge/GUI-Tkinter-lightgray.svg?logo=python" />
  <img alt="Pillow" src="https://img.shields.io/badge/Pillow-Image%20Processing-yellow.svg" />
  <img alt="License" src="https://img.shields.io/badge/License-Creative%20Commons-green.svg" />
</p>

 Um simulador interativo, desenvolvido puramente em **Python**, que recria com fidelidade a experiência visual e sonora da **Urna Eletrônica Brasileira**. O projeto utiliza `tkinter` sobrepondo perfeitamente o layout visual de uma urna real e mapeando os cliques nos botões da imagem com Canvas.

---

## 🚀 Funcionalidades Principais

- **Visual Fiel:** A interface é desenhada diretamente sobre a imagem real de uma urna, garantindo imersão física total.
- **Teclado Interativo:** Botões invisíveis mapeados pixel a pixel na imagem para digitação, correção e confirmação.
- **Feedback Sonoro:** Inclui os clássicos sons de cliques nos botões (`botoes_audio.mp3`) e o icônico aviso "pilililili" ao confirmar (`confirma_audio.mp3`), tocados nativamente usando `winmm.dll` do Windows (sem latência ou bibliotecas pesadas).
- **Animações Instantâneas:** Brilho sutil (glow) nas teclas ao serem clicadas.
- **Voto Completo:** Suporte a números válidos, nulos (com exibição visual de "NÚMERO ERRADO") e voto em branco.

---

## 👥 Candidatos Disponíveis

No banco de dados do simulador, os seguintes presidenciáveis estão registrados e mostrarão **Nome, Partido e Foto**:

| Número | Candidato | Partido |
| :---: | --- | --- |
| **13** | LULA | PT |
| **14** | RENAN SANTOS | MISSÃO |
| **22** | FLÁVIO BOLSONARO | PL |
| **30** | ROMEU ZEMA | NOVO |
| **55** | RONALDO CAIADO | PSD |

---

## 🛠️ Instalação e Requisitos

Este projeto depende apenas da biblioteca de processamento de imagens **Pillow** (pois o `tkinter` e reprodutores de áudio Windows já acompanham o Python nativo).

1. Clone o repositório ou baixe os arquivos.
2. Na pasta do projeto, instale as dependências executando o comando abaixo usando pip:

```bash
pip install -r requirements.txt
```

---

## 🎮 Como Executar

Para ligar a Urna, simplesmente rode o arquivo principal com o Python na mesma pasta:

```bash
python urna.py
```

---

## 📝 Instruções de Votação (Passo a Passo)

1. **Iniciando o Voto:** O cursor na tela "PRESIDENTE" começará em branco. Utilize o mouse para clicar nos números do painel numérico na imagem da urna.
2. **Conferência:** Após digitar **2 dígitos**, a foto e dados do candidato aparecerão no painel luminoso.
3. **Corrigindo Erros:** Caso tenha se arrependido do número, clique no botão laranja **`CORRIGE`**. A tela será limpa e você poderá recomeçar.
4. **Votando em Branco:** Clique diretamente no botão branco **`BRANCO`**. Aparecerá a tela especial confirmando o voto em branco.
5. **Finalizando:** Estando de acordo com os dados apresentados (ou branco impresso na tela), aperte o botão verde gigante **`CONFIRMA`**. Aguarde o som característico de sucesso e a tela informando "FIM". O sistema resetará depois de 3 segundos, pronto para o próximo eleitor.
