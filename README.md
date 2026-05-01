🎬 Bot de Séries Turcas
Bot para o Telegram criado para organizar e acompanhar séries turcas, controlando episódios e status de cada título por perfil de usuária.

💡 Sobre o projeto
Este bot nasceu da necessidade de ter um catálogo simples e prático direto no Telegram, sem precisar abrir nenhum aplicativo extra.
Cada usuária tem seu próprio perfil e pode cadastrar, acompanhar e atualizar suas séries de forma fácil.

✨ Funcionalidades

👩 Seleção de perfil por usuária
➕ Cadastro de novas séries com nome, episódio e status
📚 Catálogo completo com todas as séries cadastradas
▶ Continuar assistindo — acessa rapidamente qualquer série
➕➖ Atualizar episódio atual com botões
✏️ Corrigir número do episódio
📝 Corrigir nome da série
🎬 Marcar episódio como assistido
🗑 Apagar série do catálogo
🔄 Trocar de perfil sem reiniciar o bot


🚀 Como usar

Encontre o bot no Telegram pelo nome configurado no BotFather
Digite /start ou oi para começar
Escolha seu perfil e comece a cadastrar suas séries!


🛠️ Tecnologias utilizadas

Python 3
python-telegram-bot
python-dotenv
JSON para armazenamento local dos dados


📁 Estrutura do projeto
bot-series/
│
├── bot_v2.py       → código principal do bot
├── .gitignore      → arquivos ignorados pelo GitHub
└── README.md       → documentação do projeto

⚙️ Como rodar localmente
1 — Instalar as dependências:
bashpip install python-telegram-bot python-dotenv
2 — Criar o arquivo .env na pasta do projeto:
TOKEN=seu_token_aqui
3 — Rodar o bot:
bashpython bot_v2.py

📌 Observações

O arquivo .env com o token não deve ser enviado ao GitHub
Os dados das séries ficam salvos no arquivo series.json localmente
O bot precisa estar rodando no computador para funcionar


🎓 Projeto desenvolvido por
cdanibr-droid — Estudante de Gestão de Tecnologia da Informação
