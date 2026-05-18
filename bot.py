import discord
from discord.ext import commands
import requests
from deep_translator import GoogleTranslator # O nosso novo cérebro poliglota!
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} logou com sucesso e está com o jaleco pronto!')

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
        # Pega o título original em inglês que o PubMed devolveu
        titulo_ingles = detalhes.get(artigo_id, {}).get("title", "Título indisponível")
        
        # Faz a tradução automática
        titulo_pt = tradutor.translate(titulo_ingles)
        
        # Monta o link clicável
        link = f"https://pubmed.ncbi.nlm.nih.gov/{artigo_id}/"
        
        # Junta tudo na mensagem do Discord
        mensagem += f"📚 **{titulo_pt}**\n🔗 Link oficial: <{link}>\n\n"
        
    await ctx.send(mensagem)

# Carrega o cofre
load_dotenv()
# Puxa a senha lá de dentro
TOKEN = os.getenv('DISCORD_TOKEN')

keep_alive() # Inicia o servidor web
bot.run(TOKEN)