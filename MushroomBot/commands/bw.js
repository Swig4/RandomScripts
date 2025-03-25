require('dotenv').config();
const {
    EmbedBuilder
} = require('discord.js');
require("moment-duration-format");
const cheerio = require('cheerio');

module.exports = {
    name: 'bw',
    description: 'Fetches hypixel bedwars stats for a minecraft account',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const playerName = args.slice(1).join(' ');
                if (!playerName) {
                    message.reply('Please Provide A Minecraft Name.');
                    return;
                }

                const replyMessage = await message.reply(`Fetching BedWars stats for \`${playerName}\`...`);
                const response = await fetch(`https://bwstats.shivam.pro/user/${playerName}`);

                if (!response.ok) {
                    throw new Error('Failed to fetch BedWars stats. Response not OK.');
                }

                const htmlResponse = await response.text();
                const $ = cheerio.load(htmlResponse);
                let level = $("body > div > main > div.main-content > div:nth-child(2) > p:nth-child(1)").text();
                level = level.replace('Level: ', '').trim();

                let FK = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(9) > td:nth-child(2)").text().trim();
                let FD = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(10) > td:nth-child(2)").text().trim();
                let KD = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(8) > td:nth-child(2)").text().trim();
                let losses = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)").text().trim();
                let overallWins = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text().trim();

                const winsNum = parseInt(overallWins.replace(/,/g, ''), 10);
                const lossesNum = parseInt(losses.replace(/,/g, ''), 10);
                const FKNum = parseInt(FK.replace(/,/g, ''), 10);
                const FDNum = parseInt(FD.replace(/,/g, ''), 10);

                const winLossRatio = lossesNum ? winsNum / lossesNum : winsNum;
                const FKDR = FDNum ? FKNum / FDNum : FKNum;

                const embedFields = [{
                        name: 'Level',
                        value: `\`${level}\``,
                        inline: false
                    },
                    {
                        name: 'FKDR',
                        value: `\`${FKDR.toFixed(2)}\` (Final Kills: \`${FK}\`, Final Deaths: \`${FD}\`)`,
                        inline: false
                    },
                    {
                        name: 'KD',
                        value: `\`${KD}\``,
                        inline: false
                    },
                    {
                        name: 'Win/Loss Ratio',
                        value: `\`${winLossRatio.toFixed(2)}\` (Wins: \`${overallWins}\`, Losses: \`${losses}\`)`,
                        inline: false
                    }
                ];

                const embed = new EmbedBuilder()
                    .setTitle(`\`${playerName}\`'s BedWars Stats`)
                    .setColor('Red');

                embedFields.forEach(field => {
                    embed.addFields(field);
                });

                await replyMessage.edit({
                    embeds: [embed]
                });
            } catch (error) {
                console.error('Error fetching BedWars stats:', error);
                message.reply('An error occurred while fetching BedWars stats. (Have they played Bedwars before?)');
            }
        }
};