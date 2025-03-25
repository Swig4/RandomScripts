require('dotenv').config();
const {
    EmbedBuilder
} = require('discord.js');
require("moment-duration-format");
const cheerio = require('cheerio');
const {
    fetchMinecraftUuid,
    getStatus
} = require('../utils/functions');

module.exports = {
    name: 'sniper',
    description: 'Determines if the provided user is a likely hacker',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const name = args.slice(1).join(' ');
                if (!name) {
                    message.reply('Please Provide A Minecraft Name.');
                    return;
                }

                const replyMessage = await message.reply(`Determining \`${name}\`'s Sniper Score...`);
                const uuid = await fetchMinecraftUuid(name);

                if (uuid === "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }

                const [bedwarsResponse] = await Promise.all([
                    fetch(`https://bwstats.shivam.pro/user/${name}`)
                ]);

                if (!bedwarsResponse.ok) {
                    throw new Error('Failed To Fetch Bedwars Stats. Response Not OK.');
                }

                const htmlResponse = await bedwarsResponse.text();
                const $ = cheerio.load(htmlResponse);
                const errorText = $("body > div > h1").text().trim();
                if (errorText === 'Error: This player has never played Bedwars.') {
                    await replyMessage.edit(`\`${name}\` Has Never Played Bedwars.`);
                    return;
                }

                let level = $("body > div > main > div.main-content > div:nth-child(2) > p:nth-child(1)").text();
                level = level.replace('Level: ', '').trim();

                const levelNum = parseFloat(level.replace(/,/g, ''));

                let lossesNum = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)").text().trim();
                let winsNum = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text().trim();
                let FK = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(9) > td:nth-child(2)").text().trim();
                let FD = $("body > div > main > div.main-content > div:nth-child(2) > div > table > tbody > tr:nth-child(10) > td:nth-child(2)").text().trim();

                const wins = parseInt(winsNum.replace(/,/g, ''), 10);
                const losses = parseInt(lossesNum.replace(/,/g, ''), 10);
                const finalKills = parseInt(FK.replace(/,/g, ''), 10);
                const finalDeaths = parseInt(FD.replace(/,/g, ''), 10);

                const winLossRatio = losses ? wins / losses : wins;
                const FKDR = finalDeaths ? finalKills / finalDeaths : finalKills;

                let score = 0;

                if (levelNum < 100) {
                    score += Math.min(25, (100 - levelNum) * 0.25);
                } else if (levelNum < 500) {
                    score += Math.min(20, (500 - levelNum) * 0.04);
                } else if (levelNum < 1000) {
                    score += Math.min(15, (1000 - levelNum) * 0.015);
                } else if (levelNum < 2000) {
                    score += Math.min(10, (2000 - levelNum) * 0.005);
                } else {
                    score += Math.min(5, 5);
                }

                let fkdrImpact;
                if (levelNum < 100) {
                    fkdrImpact = 8;
                } else if (levelNum < 500) {
                    fkdrImpact = 4;
                } else if (levelNum < 1000) {
                    fkdrImpact = 3;
                } else {
                    fkdrImpact = 2;
                }

                if (FKDR > 1) {
                    score += Math.min(25, (FKDR - 1) * fkdrImpact);
                } else if (FKDR < 0.5) {
                    score -= Math.min(20, (0.5 - FKDR) * 40);
                }

                let winLossImpact;
                if (levelNum < 100) {
                    winLossImpact = 12;
                } else if (levelNum < 500) {
                    winLossImpact = 8;
                } else if (levelNum < 1000) {
                    winLossImpact = 6;
                } else {
                    winLossImpact = 4;
                }

                if (winLossRatio > 1) {
                    score += Math.min(30, (winLossRatio - 1) * winLossImpact);
                } else if (winLossRatio < 0.5) {
                    score -= Math.min(20, (0.5 - winLossRatio) * 40);
                }

                score = Math.min(100, Math.max(0, Math.round(score)));

                const statusData = await getStatus(uuid);

                if (typeof statusData === 'string') {
                    await replyMessage.edit(statusData);
                    return;
                }

                let statusText = statusData.session.online ? 'Online' : 'Offline';

                let emoji;
                if (score <= 39) {
                    emoji = '🟢';
                } else if (score <= 59) {
                    emoji = '🟡';
                } else {
                    emoji = '🔴';
                }

                const embed = new EmbedBuilder()
                    .setTitle(`\`${name}\`'s Sniper Score is \`${score}\` ${emoji}`)
                    .setDescription('60+ Means They Are Most Likely A Hacker/Sniper.')
                    .setColor('Red')
                    .addFields({
                        name: 'Bedwars Info',
                        value: `Level: ${level}\nFKDR: ${FKDR.toFixed(2)}\nWin/Loss Ratio: ${winLossRatio.toFixed(2)}`,
                        inline: true,
                    }, {
                        name: 'Account Info',
                        value: `Status: ${statusText}\nUUID: ${uuid}`,
                        inline: true,
                    });

                await replyMessage.edit({
                    embeds: [embed]
                });
            } catch (error) {
                console.error('Error determining if they are a sniper:', error);
                message.reply('An Error Occurred While Fetching Bedwars Stats. (Have They Played Bedwars Before? Or They Could Of Changed Their Name.)');
            }
        }
};