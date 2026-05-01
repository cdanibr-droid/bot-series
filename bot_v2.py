import json
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ✅ Token protegido — lido do arquivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

ARQUIVO = "series.json"

# ---------------- JSON ----------------

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    perfil = context.user_data.get("perfil")

    if perfil:
        teclado = [
            [InlineKeyboardButton("📚 Catálogo", callback_data="menu_list")],
            [InlineKeyboardButton("➕ Adicionar série", callback_data="menu_add")],
            [InlineKeyboardButton("▶ Continuar", callback_data="menu_continue")],
            [InlineKeyboardButton("🔄 Trocar usuário", callback_data="switch_user")]
        ]

        await update.message.reply_text(
            f"🎬 Bem-vinda de volta, {perfil.capitalize()}!",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    teclado = [
        [InlineKeyboardButton("👩 Cláudia", callback_data="user|claudia")],
        [InlineKeyboardButton("👩 Tereza", callback_data="user|tereza")]
    ]

    await update.message.reply_text(
        "🎬 CATÁLOGO DE SÉRIES TURCAS\n\nEscolha um perfil:",
        reply_markup=InlineKeyboardMarkup(teclado)
    )

# ---------------- CALLBACK ----------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    dados = carregar()
    data = query.data

    # TROCAR USUÁRIO
    if data == "switch_user":
        context.user_data.pop("perfil", None)

        teclado = [
            [InlineKeyboardButton("👩 Cláudia", callback_data="user|claudia")],
            [InlineKeyboardButton("👩 Tereza", callback_data="user|tereza")]
        ]

        await query.edit_message_text(
            "🔄 Escolha um perfil:",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # LOGIN
    if data.startswith("user"):
        _, perfil = data.split("|")
        context.user_data["perfil"] = perfil

        teclado = [
            [InlineKeyboardButton("📚 Catálogo", callback_data="menu_list")],
            [InlineKeyboardButton("➕ Adicionar série", callback_data="menu_add")],
            [InlineKeyboardButton("▶ Continuar", callback_data="menu_continue")],
            [InlineKeyboardButton("🔄 Trocar usuário", callback_data="switch_user")]
        ]

        await query.edit_message_text(
            f"👋 Bem-vinda, {perfil.capitalize()}!",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    perfil = context.user_data.get("perfil")
    if not perfil:
        await query.edit_message_text("❌ Escolha um perfil primeiro.")
        return

    user_data = dados.get(perfil, {})

    # MENU PRINCIPAL
    if data == "menu_principal":
        teclado = [
            [InlineKeyboardButton("📚 Catálogo", callback_data="menu_list")],
            [InlineKeyboardButton("➕ Adicionar série", callback_data="menu_add")],
            [InlineKeyboardButton("▶ Continuar", callback_data="menu_continue")],
            [InlineKeyboardButton("🔄 Trocar usuário", callback_data="switch_user")]
        ]

        await query.edit_message_text(
            f"🎬 Menu de {perfil.capitalize()}",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # LISTA
    if data == "menu_list":
        if not user_data:
            teclado = [
                [InlineKeyboardButton("⬅ Voltar ao menu", callback_data="menu_principal")]
            ]
            await query.edit_message_text(
                "📺 Nenhuma série ainda 😢",
                reply_markup=InlineKeyboardMarkup(teclado)
            )
            return

        texto = f"📚 Catálogo de {perfil.capitalize()}:\n\n"
        for nome, info in user_data.items():
            texto += f"▶ {nome} (E{info['episodio_atual_num']}) - {info['status']}\n"

        # ✅ Botão de voltar adicionado abaixo da lista
        teclado = [
            [InlineKeyboardButton("⬅ Voltar ao menu", callback_data="menu_principal")]
        ]

        await query.edit_message_text(
            texto,
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # ADD
    if data == "menu_add":
        context.user_data["step"] = "nome"
        await query.edit_message_text("📺 Digite o nome da série:")
        return

    # CONTINUAR
    if data == "menu_continue":
        if not user_data:
            teclado = [
                [InlineKeyboardButton("⬅ Voltar ao menu", callback_data="menu_principal")]
            ]

            await query.edit_message_text(
                "📺 Nenhuma série ainda 😢",
                reply_markup=InlineKeyboardMarkup(teclado)
            )
            return

        teclado = [
            [InlineKeyboardButton(
                f"▶ {nome} (E{info['episodio_atual_num']})",
                callback_data=f"open||{nome}"
            )]
            for nome, info in user_data.items()
        ]

        teclado.append([InlineKeyboardButton("⬅ Voltar ao menu", callback_data="menu_principal")])

        await query.edit_message_text(
            "▶ Continuar assistindo:",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # ABRIR SÉRIE
    if data.startswith("open"):
        _, nome = data.split("||")
        info = user_data[nome]

        teclado = [
            [
                InlineKeyboardButton("+ episódios", callback_data=f"up||{nome}"),
                InlineKeyboardButton("- episódios", callback_data=f"down||{nome}")
            ],
            [
                InlineKeyboardButton("🎬 finalizar episódio", callback_data=f"end||{nome}")
            ],
            [
                InlineKeyboardButton("✏️ Corrigir episódio", callback_data=f"fix_ep||{nome}"),
                InlineKeyboardButton("📝 Corrigir nome", callback_data=f"fix_nome||{nome}")
            ],
            [
                InlineKeyboardButton("⬅ voltar", callback_data="menu_continue")
            ]
        ]

        await query.edit_message_text(
            f"📺 {nome}\nE{info['episodio_atual_num']} - {info['status']}",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # CORRIGIR EPISÓDIO
    if data.startswith("fix_ep"):
        _, nome = data.split("||")
        context.user_data["fix_ep_nome"] = nome
        context.user_data["step"] = "fix_ep"

        await query.edit_message_text(
            f"✏️ Qual é o número correto do episódio de *{nome}*?",
            parse_mode="Markdown"
        )
        return

    # CORRIGIR NOME
    if data.startswith("fix_nome"):
        _, nome = data.split("||")
        context.user_data["fix_nome_antigo"] = nome
        context.user_data["step"] = "fix_nome"

        await query.edit_message_text(
            f"📝 Qual é o nome correto? (nome atual: *{nome}*)",
            parse_mode="Markdown"
        )
        return

    # AÇÕES
    if data.startswith(("up", "down", "end")):
        action, nome = data.split("||")
        info = user_data[nome]

        if action == "up":
            info["episodio_atual_num"] += 1
        elif action == "down":
            info["episodio_atual_num"] = max(1, info["episodio_atual_num"] - 1)
        elif action == "end":
            info["status"] = "episodio assistido"

        dados[perfil] = user_data
        salvar(dados)

        teclado = [
            [InlineKeyboardButton("➕ continuar editando", callback_data=f"open||{nome}")],
            [InlineKeyboardButton("🗑 apagar série", callback_data=f"delete||{nome}")],
            [InlineKeyboardButton("🏠 voltar ao catálogo", callback_data="menu_continue")]
        ]

        await query.edit_message_text(
            "Quer alterar algo?",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

    # DELETE
    if data.startswith("delete"):
        _, nome = data.split("||")

        if nome in user_data:
            del user_data[nome]

        dados[perfil] = user_data
        salvar(dados)

        await query.edit_message_text("🗑 Série apagada!")
        return

# ---------------- MENSAGEM ----------------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    if texto in ["oi", "menu", "ola", "olá", "catalogo"]:
        await start(update, context)
        return

    dados = carregar()
    perfil = context.user_data.get("perfil")

    if not perfil:
        await update.message.reply_text("❌ Escolha um perfil primeiro.")
        return

    step = context.user_data.get("step")

    if step == "fix_ep":
        try:
            episodio = int(texto)
        except:
            await update.message.reply_text("❌ Digite um número válido.")
            return

        nome = context.user_data["fix_ep_nome"]
        if perfil in dados and nome in dados[perfil]:
            dados[perfil][nome]["episodio_atual_num"] = episodio
            salvar(dados)

        context.user_data.pop("step", None)
        context.user_data.pop("fix_ep_nome", None)

        await update.message.reply_text(
            f"✅ Episódio de *{nome}* corrigido para E{episodio}!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Voltar ao menu", callback_data="menu_principal")]
            ])
        )
        return

    if step == "fix_nome":
        nome_antigo = context.user_data["fix_nome_antigo"]
        nome_novo = texto

        if perfil in dados and nome_antigo in dados[perfil]:
            dados[perfil][nome_novo] = dados[perfil].pop(nome_antigo)
            salvar(dados)

        context.user_data.pop("step", None)
        context.user_data.pop("fix_nome_antigo", None)

        await update.message.reply_text(
            f"✅ Nome corrigido de *{nome_antigo}* para *{nome_novo}*!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Voltar ao menu", callback_data="menu_principal")]
            ])
        )
        return

    if step == "nome":
        context.user_data["temp_nome"] = texto
        context.user_data["step"] = "episodio"
        await update.message.reply_text("🎬 Em qual episódio?")
        return

    if step == "episodio":
        try:
            episodio = int(texto)
        except:
            await update.message.reply_text("❌ Digite um número.")
            return

        context.user_data["temp_episodio"] = episodio
        context.user_data["step"] = "status"
        await update.message.reply_text("1 - Em andamento\n2 - Finalizada")
        return

    if step == "status":
        if texto in ["1", "em andamento"]:
            status = "em andamento"
        elif texto in ["2", "finalizada"]:
            status = "finalizada"
        else:
            await update.message.reply_text("❌ Digite 1 ou 2")
            return

        nome = context.user_data["temp_nome"]
        episodio = context.user_data["temp_episodio"]

        if perfil not in dados:
            dados[perfil] = {}

        dados[perfil][nome] = {
            "episodio_atual_num": episodio,
            "status": status
        }

        salvar(dados)
        perfil_atual = context.user_data.get("perfil")  # ✅ salva o perfil antes
        context.user_data.clear()
        context.user_data["perfil"] = perfil_atual  # ✅ restaura o perfil depois

        teclado = [
            [InlineKeyboardButton("🏠 Voltar ao menu", callback_data="menu_principal")]
        ]

        await update.message.reply_text(
            f"✅ Série salva: {nome} 😊\nDeseja voltar ao menu?",
            reply_markup=InlineKeyboardMarkup(teclado)
        )
        return

# ---------------- BOT ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("oi", start))
app.add_handler(CommandHandler("menu", start))

app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
