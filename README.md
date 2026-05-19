# ᯓ★ VeritaMed Bot 🩺✨

Um assistente virtual avançado para Discord desenvolvido em Python, focado em quebrar a barreira do idioma e otimizar o fluxo de trabalho na pesquisa científica em saúde e biológicas. O sistema consome a API oficial do PubMed, integra-se ao ecossistema de Inteligência Artificial do Google Gemini para resumir abstracts e automatiza a formatação de referências bibliográficas. ૮ ˶ᵔ ᵕ ᵔ˶ ა

# ⚗︎ Motivação do Projeto

A imensa maioria da literatura médica e científica de ponta é publicada em inglês, e a formatação manual de referências consome um tempo precioso que poderia ser dedicado ao estudo crítico. Unindo a vivência da rotina de saúde com a arquitetura de software, este bot nasceu para ser um facilitador no acesso à ciência. Ele centraliza a triagem, traduz os títulos, mastiga dados complexos via LLM e padroniza referências, mostrando o papel da tecnologia como ponte para o conhecimento científico. ⋆⁺₊⋆

# 𖦹 Funcionalidades

* **Busca Integrada (`!artigo`):** Conexão direta e automatizada com a base de dados do National Center for Biotechnology Information (NCBI / PubMed) para capturar os estudos mais recentes sobre o termo desejado.
* **Tradução Simultânea:** Processamento em tempo real para traduzir títulos científicos complexos do inglês para o português (Brasil).
* **Mastigador de Abstracts com IA (`!resumo`):** Integração com o modelo de linguagem **Gemini 2.5 Flash** para processar e resumir abstracts técnicos em inglês, devolvendo a conclusão sintetizada em 3 tópicos simples e claros em português.
* **Gerador Automático de ABNT (`!abnt`):** Extração de metadados da publicação (autores, revista, volume, ano) e formatação instantânea da referência bibliográfica nos padrões da ABNT.
* **Central de Monitoramento (Logs):** Sistema isolado de rastreamento assíncrono que reporta entradas de usuários e interações de cargos diretamente a um canal de moderação privado.

✦ Tecnologias Utilizadas

* **Linguagem Principal:** Python 3
* **Ecossistema & Bibliotecas:**
    * `discord.py` (Arquitetura de comandos assíncronos e eventos da plataforma)
    * `google-genai` (SDK oficial do Google para conexão com LLMs via API)
    * `requests` (Consumo da API RESTful pública do PubMed com tratamento de timeouts)
    * `deep-translator` (Motor de tradução automatizada de termos)
    * `python-dotenv` (Gerenciamento seguro de variáveis de ambiente e chaves de API)
    * `flask` & `threading` (Mecanismo keep-alive para estabilidade do servidor em nuvem)

⋆ Como executar o projeto localmente

1. Clone este repositório no seu ambiente:
  git clone [https://github.com/essiecarvalho/VeritaMed](https://github.com/essiecarvalho/VeritaMed)

2. Instale as dependências necessárias:
pip install -r requirements.txt

3. Configure o seu "cofre" local criando um arquivo .env na raiz do projeto e preenchendo suas credenciais confidenciais:
DISCORD_TOKEN=seu_token_aqui
LOG_CHANNEL_ID=id_do_canal_de_logs
GEMINI_API_KEY=sua_chave_do_google_ai_studio

4. Inicie o sistema:
python bot.py


❀ Próximos Passos (Roadmap)

[x] Implementar comando para tradução e resumo do Abstract completo via Inteligência Artificial.

[x] Desenvolver sistema automatizado de formatação de referências bibliográficas (ABNT).

[x] Criar painel interativo de Self-Roles por reação para gerenciamento de cargos estudantis.

[ ] Desenvolver sistema de "Radar" com alertas automatizados de novos artigos indexados para termos específicos.

[ ] Implementar banco de dados local para gamificação e Flashcards de revisão de termos anatômicos/clínicos.


Desenvolvido com dedicação, lógica e muito cappuccino! 
do código à saúde. ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧


***