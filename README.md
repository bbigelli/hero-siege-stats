📊 Sobre o Projeto
Hero Siege Stats é uma aplicação desktop para Windows que monitora e exibe estatísticas em tempo real do jogo Hero Siege. Através da captura de pacotes de rede, o aplicativo mostra informações como gold, experiência, duração da sessão e efeitos da Zona Satânica sem a necessidade de modificar o jogo.

### App preview

![App preview](/assets/readme/preview.png)

### ✨ Funcionalidades
🪙 Monitoramento de Gold - Total de gold, gold ganho na sessão e gold por hora

⭐ Monitoramento de XP - Experiência total, XP ganho na sessão e XP por hora

⏱️ Duração da Sessão - Tempo decorrido desde o início do monitoramento

📧 Status do Mail - Indica se há novos e-mails no jogo

🌙 Zona Satânica - Exibe buffs e debuffs ativos da Zona Satânica com ícones e descrições detalhadas

🔄 Reset de Estatísticas - Botão para reiniciar todas as estatísticas a qualquer momento

🖼️ Ícones Personalizados - Interface temática com ícones do jogo

## É permitido usar o APP?

![image](https://github.com/GuilhermeFaga/hero-siege-stats/assets/32572430/56a116cb-66b1-45de-afa9-3d3dc7a2ea6c)


### 🖥️ Requisitos do Sistema
Sistema Operacional: Windows 10 ou superior

Jogo: Hero Siege (qualquer versão recente)

Python: 3.11 ou superior (para executar a partir do código)

### 🚀 Como Usar
Executável (Recomendado)
Baixe o arquivo .exe da página de releases

Execute o arquivo (não precisa de instalação)

Inicie o Hero Siege

Acompanhe suas estatísticas em tempo real

#### Instruções para desenvolvedores

### A partir do código fonte

### Requirementos

- [Python 3.11](https://www.python.org/downloads/release/python-3116/)
- [Poetry](https://python-poetry.org/)

### Passo a Passo

# Clone o repositório
git clone https://github.com/bbigelli/hero-siege-stats.git

# Entre no diretório
cd hero-siege-stats

# Instale as dependências com Poetry
poetry install

# Execute o programa
python hero-siege-stats.py


## Contribuidores

- [Guilherme Faga](https://faga.dev)
- [Skijearz](https://github.com/Skijearz)
- [Elliot Chen](https://github.com/keoy7am)

Thanks to **Shalwkz** for helping me with finding the game server address.

Highly inspired by [Albion Online Stats](https://github.com/mazurwiktor/albion-online-stats).

# ⚠️ Observações
O aplicativo não modifica o jogo nem envia dados ao servidor.

Apenas lê os pacotes de rede que o jogo já envia naturalmente.

Este projeto é independente e não é afiliado oficialmente aos desenvolvedores do Hero Siege.
