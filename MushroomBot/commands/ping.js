require('dotenv').config();
const {
    Client,
    IntentsBitField,
    EmbedBuilder
} = require('discord.js');
require("moment-duration-format");
const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
        IntentsBitField.Flags.DirectMessages
    ]
});
module.exports = {
    name: 'ping',
    description: 'Gets the bots ping',
    execute: async (client, message) => {
            const clientPing = Date.now() - message.createdTimestamp;
            const embed = new EmbedBuilder()
            .setTitle('Ping')
            .setDescription('Heres The Current Client And Websocket Ping')
            .setColor('Red')
            .addFields(
              {
                name: 'Client Ping',
                value: `${clientPing}ms`,
                inline: true,
              },
              {
                name: 'Websocket Ping',
                value: `${client.ws.ping}ms`,
                inline: true,
              }
            );
            message.reply({ embeds: [embed] });
        }
};