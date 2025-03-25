require('dotenv').config();
require("moment-duration-format");
const cheerio = require('cheerio');
var SnipeAPIKey = process.env.ANTISNIPEKEY;
const {
    fetchMinecraftUuid
} = require('../utils/functions');

module.exports = {
    name: 'ws',
    description: 'Fetches hypixel bedwars winstreaks for a minecraft account',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const name = args.slice(1).join(' ');
                if (!name) {
                    message.reply("Please Provide A Minecraft Name.");
                    return;
                }
                const replyMessage = await message.reply(`Fetching \`${name}\`'s Current Winstreaks...`);

                const uuid = await fetchMinecraftUuid(name);

                if (uuid == "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }
                const [overallWS, bedwarsResponse] = await Promise.all([
                    fetch(`https://api.antisniper.net/v2/player/winstreak?key=${SnipeAPIKey}&player=${name}`),
                    fetch(`https://bwstats.shivam.pro/user/${name}`)
                ]);

                if (!overallWS.ok || !bedwarsResponse.ok) {
                    throw new Error('Failed To Fetch Winstreak Stats. Response Not OK.');
                }

                const winstreakData = await overallWS.json();
                const overallWinstreak = winstreakData.overall_winstreak;
                const soloWinstreak = winstreakData.eight_one_winstreak;
                const duoWinstreak = winstreakData.eight_two_winstreak;
                const trioWinstreak = winstreakData.four_three_winstreak;

                const htmlResponse = await bedwarsResponse.text();
                const $ = cheerio.load(htmlResponse);
                let level = $("body > div > main > div.main-content > div:nth-child(2) > p:nth-child(1)").text();
                level = level.replace('Level: ', '').trim();

                replyMessage.edit(`\`${level} ${name}\`'s Estimated Winstreaks:\n>>> Overall: ${overallWinstreak}\nSolo: ${soloWinstreak}\nDoubles: ${duoWinstreak}\nTrios: ${trioWinstreak}`);
            } catch (error) {
                console.log('Failed To Find Winstreak: ', error);
                message.reply("There Was An Error While Fetching Winstreak.");
            }
    }
};