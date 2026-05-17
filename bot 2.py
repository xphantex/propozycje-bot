import discord
from discord.ext import commands

# 1. Ustawienia uprawnień bota (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Wymagane, aby bot mógł czytać treść propozycji

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= KRAINA KONFIGURACJI =================
# Zmień te dwie wartości na własne:

ID_KANALU_PROPOZYCJI = 1505540890066681876  # Wklej tutaj ID swojego kanału
TOKEN_BOTA = "TUTAJ_WKLEJ_SWOJ_TOKEN_Z_DEVELOPER_PORTAL"

# =======================================================


@bot.event
async def on_ready():
    print(f"Sukces! Bot {bot.user} jest gotowy do działania.")


@bot.event
async def on_message(message):
    # Ignoruj wiadomości wysyłane przez inne boty (i samego siebie)
    if message.author.bot:
        return

    # Sprawdź, czy wiadomość została napisana na odpowiednim kanale
    if message.channel.id == ID_KANALU_PROPOZYCJI:
        tresc_propozycji = message.content
        autor = message.author

        # Usuń oryginalną wiadomość użytkownika (żeby nie było spamu)
        try:
            await message.delete()
        except discord.Forbidden:
            print(
                "Błąd: Bot nie ma uprawnień do usuwania wiadomości (Manage Messages)!"
            )

        # Tworzenie wyglądu propozycji (Embed) dokładnie tak jak na zdjęciu
        embed = discord.Embed(
            title=f"Propozycja | {autor.display_name}",
            description=f"Przygotował propozycję o następującej treści:\n\n```text\n{tresc_propozycji}\n```",
            color=discord.Color.from_rgb(
                47, 49, 54
            ),  # Ciemny kolor pasujący do Discorda
        )

        # Ustawienie stopki z ikoną autora i czasem wysłania
        avatar_url = autor.avatar.url if autor.avatar else autor.default_avatar.url
        embed.set_footer(text="Data", icon_url=avatar_url)
        embed.timestamp = message.created_at

        # Wysyłanie propozycji i przypisanie jej do zmiennej
        bot_message = await message.channel.send(embed=embed)

        # Dodawanie reakcji (zielony haczyk i czerwony krzyżyk)
        await bot_message.add_reaction("✅")
        await bot_message.add_reaction("❌")

        # Automatyczne otwieranie wątku dyskusji pod wiadomością bota
        try:
            await bot_message.create_thread(
                name="Dyskusja dotycząca propozycji",
                auto_archive_duration=1440,  # Zamknie wątek po 24h nieaktywności
            )
        except discord.HTTPException as e:
            print(f"Nie udało się utworzyć wątku: {e}")

    # Pozwala botowi przetwarzać inne komendy tekstowe (jeśli je dopiszesz w przyszłości)
    await bot.process_commands(message)


# Uruchomienie bota
bot.run("TOKEN_BOTA")
