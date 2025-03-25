require('dotenv').config();
const {
    EmbedBuilder
} = require('discord.js');

const moment = require("moment");
require("moment-duration-format");
const {
    fetchMinecraftUsername
} = require('../utils/functions');

module.exports = {
    name: 'boosters',
    description: 'Fetches active boosters for Hypixel',
    execute: async (client, message) => {
            try {
                const replyMessage = await message.reply('Fetching boosters...');
                const response = await fetch('https://api.plancke.io/hypixel/v1/boosters');
                const data = await response.json();

                if (!data.success) {
                    throw new Error('Failed to fetch boosters.');
                }

                const boosters = data.record;
                const embed = new EmbedBuilder()
                    .setTitle('Available Boosters')
                    .setColor('Red');

                for (const booster of boosters) {
                    let gameType = '';
                    switch (booster.gameType) {
                        case 51:
                            gameType = 'Classic Games';
                            break;
                        case 56:
                            gameType = 'SkyWars';
                            break;
                        default:
                            gameType = 'Unknown';
                            break;
                    }

                    const minecraftUsername = await fetchMinecraftUsername(booster.purchaserUuid);
                    const duration = moment.duration(booster.length, 'seconds');
                    const hours = duration.hours();
                    const minutes = duration.minutes();
                    const seconds = duration.seconds();
                    const boostLength = `${hours > 0 ? hours + ' hours, ' : ''}${minutes > 0 ? minutes + ' minutes, ' : ''}${seconds} seconds`;

                    embed.addFields({
                        name: 'Username',
                        value: `\`${minecraftUsername}\``,
                        inline: true
                    }, {
                        name: 'Game Type',
                        value: gameType,
                        inline: true
                    }, {
                        name: 'Boost Length',
                        value: boostLength,
                        inline: true
                    }, {
                        name: '\u200B',
                        value: '\u200B'
                    });
                }
                await replyMessage.edit({
                    embeds: [embed]
                });
            } catch (error) {
                // console.error('Error fetching boosters:', error);
                message.reply('There Are No Avalible Boosters.');
            }
        }
};