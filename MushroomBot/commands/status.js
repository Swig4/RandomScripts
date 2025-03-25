require('dotenv').config();
require("moment-duration-format");
const {
    fetchMinecraftUuid,
    getStatus
} = require('../utils/functions');

module.exports = {
    name: 'status',
    description: 'Fetches online status for a minecraft account on Hypixel',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const playerName = args.slice(1).join(' ');
                if (!playerName) {
                    message.reply('Please Provide A Minecraft Name.');
                    return;
                }

                const replyMessage = await message.reply(`Fetching Online Status For \`${playerName}\`...`);
                const uuid = await fetchMinecraftUuid(playerName);
                if (uuid == "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }

                const statusData = await getStatus(uuid);

                if (typeof statusData === 'string') {
                    await replyMessage.edit(statusData);
                    return;
                }

                let statusText = statusData.session.online ? 'Online' : 'Offline';
                let status = "";
                let gameMode = "";
                if (statusText === "Offline") {
                    status = " (Their API Could Be Off, Or they Set Their Status To Offline.)";
                    gameMode = "";
                } else {
                    status = "";
                    gameMode = statusData.session.gameType;
                    gameMode = gameMode.toLowerCase();
                }
                await replyMessage.edit(`\`${playerName}\` Is **${statusText}**${status}${gameMode ? ` | Playing ${gameMode}` : ''}`);
                //await replyMessage.edit(`${statusText}`);
            } catch (error) {
                console.error('Error fetching online status:', error);
                message.reply('An Error Occurred While Fetching Online Status. Please Try Again Later.');
            }
        }
};