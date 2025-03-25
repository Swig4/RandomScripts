require('dotenv').config();
require("moment-duration-format");
const {
    getCount
} = require('../utils/functions');

module.exports = {
    name: 'count',
    description: 'Fetches hypixel online count',
    execute: async (client, message) => {
            try {
                const replyMessage = await message.reply("Fetching Player Count For Hypixel...");

                const statusData = await getCount();

                if (typeof statusData === 'string') {
                    await replyMessage.edit(statusData);
                    return;
                }

                let playerCount = statusData.playerCount;

                if (playerCount) {
                    await replyMessage.edit(`There Are Currently \`${playerCount}\` Players On Hypixel Right Now.`);
                } else {
                    console.error('Failed to find the player count in the response.');
                    await replyMessage.edit('Unable To Fetch The Player Count From The Website.');
                }
            } catch (error) {
                console.error('Error fetching player count:', error);
                message.reply('An Error Occurred While Fetching The Player Count.');
            }
        }
};