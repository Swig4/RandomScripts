require('dotenv').config();
require("moment-duration-format");
const {
    fetchMinecraftUsername
} = require('../utils/functions');

module.exports = {
    name: 'name',
    description: 'Fetches name for a minecraft account',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const uuid = args.slice(1).join(' ');
                const replyMessage = await message.reply('Fetching Name...');
                if (!uuid) {
                    await replyMessage.edit('Please Provide A Minecraft UUID.');
                    return;
                }

                const minecraftUsername = await fetchMinecraftUsername(uuid);
                if (minecraftUsername == uuid || minecraftUsername == "Unknown") {
                    await replyMessage.edit(`Invalid UUID Provided.`);
                    return;
                }
                await replyMessage.edit(`\`${minecraftUsername}\``);
            } catch (error) {
                console.error('Error fetching name:', error);
                message.reply('An error occurred while fetching name.');
            }
        }
};