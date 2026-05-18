# ᯓ★ PubMed Searcher Bot ✧

Um assistente virtual para Discord desenvolvido em Python, focado em quebrar a barreira do idioma na pesquisa científica. Ele consome a API oficial do PubMed, busca os artigos médicos mais recentes sobre o tema desejado e entrega os títulos traduzidos para o português diretamente no chat. ૮ ˶ᵔ ᵕ ᵔ˶ ა

# ⚗︎ Motivação do Projeto

A imensa maioria da literatura médica e científica de ponta é publicada em inglês, o que pode representar um obstáculo na rotina de estudantes e pesquisadores brasileiros. Unindo a vivência da rotina clínica com a arquitetura de software, este bot nasceu para otimizar o fluxo de estudos acadêmicos. Ele automatiza a triagem e tradução de artigos, mostrando como a tecnologia pode e deve ser uma facilitadora no acesso à ciência e à saúde. ⋆⁺₊⋆

# 𖦹 Funcionalidades

* **Busca Integrada:** Conexão direta e automatizada com a base de dados do *National Center for Biotechnology Information* (NCBI / PubMed).
* **Tradução Simultânea:** Processamento em tempo real para traduzir títulos científicos complexos do inglês para o português.
* **Acesso Imediato:** Entrega os links oficiais dos estudos formatados e prontos para clique direto na interface do servidor.

# ✦ Tecnologias Utilizadas

* **Linguagem Principal:** Python 3
* **Ecossistema & Bibliotecas:**
  * `discord.py` (Arquitetura de comandos e integração com a plataforma)
  * `requests` (Consumo da API RESTful pública do PubMed)
  * `deep-translator` (Motor de tradução assíncrona)

# ⋆ Como executar o projeto localmente

1. Clone este repositório no seu ambiente:
git clone [https://github.com/seu-usuario/-bot.git](https://github.com/seu-usuario/medisearch-bot.git)

2. Instale as dependências necessárias:
pip install discord.py requests deep-translator
Insira o seu Token de Aplicação do Discord no final do arquivo bot.py.

3. Inicie o sistema:
python bot.py


❀ Próximos Passos (Roadmap)
[ ] Implementar comando para tradução do Abstract (resumo) completo da publicação.

[ ] Desenvolver sistema de "Radar" com alertas automáticos no chat para novas publicações de termos específicos.

[ ] Otimização de tratamento de erros para buscas sem resultados.


Desenvolvido com dedicação e muito café! ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧


***