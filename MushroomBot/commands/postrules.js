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
    name: 'postrules',
    description: 'Posts the rules message into the rules channel',
    execute: async (client, message) => {
            const channelID = '1137205056752586782';
            const channel = client.channels.cache.get(channelID);
            message.reply('Done!')
            channel.messages.fetch({
                    limit: 10
                })
                .then(messages => {
                    const botMessages = messages.filter(msg => msg.author.id === client.user.id);
                    botMessages.forEach(msg => {
                        msg.delete().catch(console.error);
                    });
                    const embed = new EmbedBuilder()
                        .setTitle('Server Rules')
                        .setDescription('Welcome to our server! Please make sure to read and follow the rules below:')
                        .setColor('Red')
                        .addFields({
                            name: 'Discord TOS',
                            value: `All members must abide by Discord's Terms of Service.\nhttps://discord.com/terms`,
                            inline: false,
                        }, {
                            name: 'No Cracking',
                            value: `Cracking Mushroom Client is not allowed. Anyone caught doing so will be banned.`,
                            inline: false,
                        }, {
                            name: 'No NSFW',
                            value: `NSFW is not allowed anywhere inside the server.`,
                            inline: false,
                        }, {
                            name: 'Respect Staff',
                            value: `Staff members have the right to take appropriate action (mute, kick, ban) if they deem it necessary. Please be respectful.`,
                            inline: false,
                        }, {
                            name: 'No Ban Evading',
                            value: `Do not attempt to evade bans by creating alternate accounts.`,
                            inline: false,
                        }, {
                            name: 'Tickets',
                            value: `Do not create tickets without a reason, valid reasons are listed in the tickets channel.`,
                            inline: false,
                        }, {
                            name: 'Batman\'s Rule',
                            value: `we enforce a strict anti-retard policy in this Discord sever, as part of our average IQ goals for Q4 of this year.`,
                            inline: false,
                        }, {
                            name: 'Have A problem?',
                            value: `If you have a problem with a staff member or one of the listed rules, feel free to open a ticket.`,
                            inline: false,
                        })
                        .setImage('https://images-ext-1.discordapp.net/external/50pdR63B0QaR3v4ATvV7ZbO33Wcnnbdz3hFT4L5HO7Y/https/media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzJydzA3ZWc2MndpcW80Z2F5dHBwMDFuM2s2amdiMXR6NXN1Z2l5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZO7JobQkihqr1meNep/giphy.gif');
                    channel.send({
                        embeds: [embed]
                    });
                })
                .catch(console.error);
        }
};