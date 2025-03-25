require('dotenv').config();
require("moment-duration-format");
const {
    fetchMinecraftUuid
} = require('../utils/functions');

module.exports = {
    name: 'uuid',
    description: 'Fetches uuid for a minecraft account',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const name = args.slice(1).join(' ');
                const replyMessage = await message.reply('Fetching UUID...');
                if (!name) {
                    await replyMessage.edit('Please provide a Name.');
                    return;
                }
                const minecraftUsername = await fetchMinecraftUuid(name);
                if (minecraftUsername == "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }
                await replyMessage.edit(`\`${minecraftUsername}\``);
            } catch (error) {
                console.error('Error fetching uuid:', error);
                await replyMessage.edit('An error occurred while fetching UUID.');
            }
        }
};