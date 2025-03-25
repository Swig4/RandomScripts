require('dotenv').config();
const {
    ActivityType
} = require('discord.js');
require("moment-duration-format");
module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        try {
            await client.guilds.fetch();
            let totalMembers = 0;

            client.guilds.cache.forEach(guild => {
                totalMembers += guild.memberCount;
            });
        } catch (error) {
            console.error('Error fetching guilds:', error);
        }

        console.log(`✅ ${client.user.username} is online.`);
        client.user.setPresence({
            activities: [{
                name: '.mc help | Made By swig5',
                type: ActivityType.Watching,
                status: 'online',
            }],
        });
    },
};