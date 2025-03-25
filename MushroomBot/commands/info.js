require('dotenv').config();
const { Client, IntentsBitField, EmbedBuilder } = require('discord.js');
const moment = require('moment');
require('moment-duration-format');

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
    name: 'info',
    description: 'Gets info for the bot',
    execute: async (client, message) => {
        try {
            const guild = message.guild;
            if (!guild) {
                throw new Error('Guild not found.');
            }

            await guild.members.fetch();

            let partnerID = '1235062467915415623';
            let partnerRole = guild.roles.cache.get(partnerID);
            let partners = partnerRole ? partnerRole.members.size : 0;

            let mediaID = '1241858277600395356';
            let mediaRole = guild.roles.cache.get(mediaID);
            let media = mediaRole ? mediaRole.members.size : 0;

            let supporterRoleID = '1234182734180778036';
            let supporterRole = guild.roles.cache.get(supporterRoleID);
            let supporters = supporterRole ? supporterRole.members.filter(member => !member.roles.cache.has(partnerID) && !member.roles.cache.has(mediaID)).size : 0;

            let memberCount = guild.memberCount;
            const duration = moment.duration(client.uptime);
            const formattedUptime = `${Math.floor(duration.asDays())} Days, ${duration.hours()} Hours, ${duration.minutes()} Minutes, ${duration.seconds()} Seconds`;

            const embed = new EmbedBuilder()
                .setTitle(`Info`)
                .setColor('Red')
                .addFields(
                    { name: 'Server Info', value: `${supporters} People Bought Mushroom Client.\n${media} Have The Media Role\nWatching Over ${memberCount} Members`, inline: true },
                    { name: 'Bot Info', value: `Uptime: ${formattedUptime}`, inline: true },
                    { name: 'Client Info', value: `Owned By swig5, 112batman, scoliosissy, sun3k, and sideload\nWebsite: https://mushroomer.top`, inline: true }
                );

            message.reply({ embeds: [embed] });
        } catch (error) {
            console.error('Error fetching guild info:', error);
            message.reply('An error occurred while fetching guild info.');
        }
    }
};
