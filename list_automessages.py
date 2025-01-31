@bot.command()
async def list_auto_messages(ctx):
    """
    Liste tous les messages automatisés associés au canal actuel.
    Syntaxe : !list_auto_messages
    """
    # Connexion à la base de données
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    # Récupérer les messages associés au canal actuel
    cursor.execute("""
        SELECT message_id, message_content, interval_hours, interval_minutes
        FROM auto_messages
        WHERE channel_id = %s
    """, (ctx.channel.id,))

    messages = cursor.fetchall()
    db.close()

    if not messages:
        await ctx.send("Aucun message automatisé n'est configuré pour ce canal.")
        return

    # Construire une réponse lisible
    response = "**Messages automatisés pour ce canal :**\n"
    for message in messages:
        response += (
            f"**ID :** {message['message_id']}\n"
            f"**Message :** {message['message_content']}\n"
            f"**Intervalle :** {message['interval_hours']} heures et {message['interval_minutes']} minutes\n"
            "----------------------------------\n"
        )

    await ctx.send(response)