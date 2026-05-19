import os
import discord
from discord.ext import commands
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from keep_alive import keep_alive
import google.generativeai as genai

# Carrega as senhas do cofre
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')

# Configura o cérebro da IA (Gemini)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
modelo_ia = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

CARGOS_EMOJIS = {
    "🎓": "Graduando",
    "🔬": "Pós-graduando",
    "🐣": "Calouro",
    "🦉": "Veterano",
    "❤️": "ela/dela",
    "💚": "ele/dele",
    "💜": "elu/delu",
    "💛": "tanto faz"
}

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} logou com sucesso e está de plantão!')

# 📥 LOG DE ENTRADA: Quando alguém entra no servidor
@bot.event
async def on_member_join(member):
    cargo_pesquisador = discord.utils.get(member.guild.roles, name="Pesquisador")
    if cargo_pesquisador:
        await member.add_roles(cargo_pesquisador)
        
        # Envia o aviso para o seu canal de logs privado
        canal_log = bot.get_channel(int(os.getenv('LOG_CHANNEL_ID')))
        if canal_log:
            await canal_log.send(f"📥 **{member.name}** acabou de entrar no servidor e recebeu o cargo automático `Pesquisador`! 🩺")

# ✅ LOG DE ADIÇÃO: Quando alguém clica no emoji do painel
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    
    emoji = str(payload.emoji)
    if emoji in CARGOS_EMOJIS:
        guild = bot.get_guild(payload.guild_id)
        nome_cargo = CARGOS_EMOJIS[emoji]
        cargo = discord.utils.get(guild.roles, name=nome_cargo)
        
        if cargo:
            await payload.member.add_roles(cargo)
            
            # Envia o log de confirmação
            canal_log = bot.get_channel(int(os.getenv('LOG_CHANNEL_ID')))
            if canal_log:
                await canal_log.send(f"🟢 **{payload.member.name}** reagiu com {emoji} e ganhou o cargo `{nome_cargo}`.")

# ❌ LOG DE REMOÇÃO: Quando alguém clica de novo e tira a reação
@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    membro = guild.get_member(payload.user_id)
    
    if membro and not membro.bot:
        emoji = str(payload.emoji)
        if emoji in CARGOS_EMOJIS:
            nome_cargo = CARGOS_EMOJIS[emoji]
            cargo = discord.utils.get(guild.roles, name=nome_cargo)
            
            if cargo:
                await membro.remove_roles(cargo)
                
                # Envia o log de remoção
                canal_log = bot.get_channel(int(os.getenv('LOG_CHANNEL_ID')))
                if canal_log:
                    await canal_log.send(f"🔴 **{membro.name}** removeu a reação {emoji} e perdeu o cargo `{nome_cargo}`.")

# O Painel de Cargos (Apenas Admins)
@bot.command()
@commands.has_permissions(administrator=True)
async def painel(ctx):
    texto = (
        "**ᯓ★ Auto-Roles: Escolha seus cargos! ✧**\n\n"
        "Reaja a esta mensagem com os emojis correspondentes para receber (ou remover) seus cargos no servidor.\n\n"
        "**Nível Acadêmico:**\n"
        "🎓 - Graduando\n"
        "🔬 - Pós-graduando\n"
        "🐣 - Calouro\n"
        "🦉 - Veterano\n\n"
        "**Pronomes:**\n"
        "❤️ - ela/dela\n"
        "💚 - ele/dele\n"
        "💜 - elu/delu\n"
        "💛 - tanto faz"
    )
    mensagem = await ctx.send(texto)
    for emoji in CARGOS_EMOJIS.keys():
        await mensagem.add_reaction(emoji)

# Comando 0: Cérebro de Pesquisa Científica
@bot.command()
async def artigo(ctx, *, termo_de_busca):
    await ctx.send(f"🔍 Vasculhando os arquivos médicos globais sobre **{termo_de_busca}** e traduzindo...")
    
    url_pesquisa = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={termo_de_busca}&retmode=json&retmax=3"
    resposta = requests.get(url_pesquisa)
    ids = resposta.json().get("esearchresult", {}).get("idlist", [])
    
    if not ids:
        await ctx.send(f"❌ Poxa, não encontrei nenhum artigo recente sobre '{termo_de_busca}'. Tente outro termo em inglês!")
        return
    
    ids_string = ",".join(ids)
    url_detalhes = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_string}&retmode=json"
    resposta_detalhes = requests.get(url_detalhes)
    detalhes = resposta_detalhes.json().get("result", {})
    
    mensagem = f"✅ **Encontrei {len(ids)} artigos fresquinhos!** Aqui estão os resumos:\n\n"
    tradutor = GoogleTranslator(source='en', target='pt')
    
    for artigo_id in ids:
        titulo_ingles = detalhes.get(artigo_id, {}).get("title", "Título indisponível")
        titulo_pt = tradutor.translate(titulo_ingles)
        link = f"https://pubmed.ncbi.nlm.nih.gov/{artigo_id}/"
        mensagem += f"📚 **{titulo_pt}**\n🔗 Link oficial: <{link}>\n\n"
        
    await ctx.send(mensagem)

# COMANDO 1: O Mastigador de Abstracts com IA
@bot.command()
async def resumo(ctx, artigo_id):
    await ctx.send(f"🧠 Conectando à IA para ler e resumir o artigo **{artigo_id}**... um momento!")
    
    try:
        # 1. Busca o texto completo do abstract no PubMed
        url_abstract = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={artigo_id}&rettype=abstract&retmode=text"
        resposta = requests.get(url_abstract)
        abstract_texto = resposta.text
        
        # PubMed às vezes não tem o resumo de artigos muito antigos
        if "cannot get document summary" in abstract_texto.lower() or len(abstract_texto) < 20:
            await ctx.send(f"❌ O PubMed não disponibilizou o resumo em texto para o ID {artigo_id}. Tente um artigo mais recente!")
            return

        # 2. Pede para o Gemini mastigar o texto (Usando a função ASYNC para não congelar o bot)
        prompt = f"Você é um assistente acadêmico de saúde. Traduza e resuma o seguinte abstract médico para o português em 3 tópicos curtos, simples e fáceis de entender:\n\n{abstract_texto}"
        
        resposta_ia = await modelo_ia.generate_content_async(prompt)
        
        mensagem = f"✨ **Resumo Inteligente do Artigo ({artigo_id})** ✨\n\n{resposta_ia.text}"
        await ctx.send(mensagem)
        
    except Exception as erro:
        # Se QUALQUER coisa der errado, ele avisa no chat em vez de ficar mudo!
        await ctx.send(f"⚠️ Oops! Meus circuitos de IA tropeçaram. O erro foi: `{erro}`")


# COMANDO 2: Gerador de ABNT Automático
@bot.command()
async def abnt(ctx, artigo_id):
    url_detalhes = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={artigo_id}&retmode=json"
    resposta = requests.get(url_detalhes)
    detalhes = resposta.json().get("result", {}).get(artigo_id, {})
    
    if not detalhes:
        await ctx.send("❌ Artigo não encontrado para gerar a referência.")
        return
    
    # Extrai as informações
    titulo = detalhes.get("title", "Título indisponível")
    revista = detalhes.get("fulljournalname", "Revista indisponível")
    ano = detalhes.get("pubdate", "Ano").split(" ")[0]
    volume = detalhes.get("volume", "")
    
    # Formata os autores para o padrão ABNT (SOBRENOME, Iniciais.)
    lista_autores = detalhes.get("authors", [])
    autores_formatados = []
    
    for autor in lista_autores:
        nome = autor.get('name', '')
        partes = nome.split(' ')
        if len(partes) > 1:
            sobrenome = partes[0].upper()
            iniciais = ' '.join(partes[1:])
            autores_formatados.append(f"{sobrenome}, {iniciais}.")
        else:
            autores_formatados.append(nome.upper())
            
    str_autores = "; ".join(autores_formatados)
    
    # Monta a referência final
    referencia = f"{str_autores} {titulo}. **{revista}**, v. {volume}, {ano}. Disponível em: <https://pubmed.ncbi.nlm.nih.gov/{artigo_id}/>."
    
    await ctx.send(f"📖 **Sua referência ABNT está pronta:**\n\n{referencia}")

keep_alive()
bot.run(TOKEN)