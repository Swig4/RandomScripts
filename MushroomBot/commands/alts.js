require('dotenv').config();
require("moment-duration-format");
var SnipeAPIKey = process.env.ANTISNIPEKEY;
const {
    fetchMinecraftUuid
} = require('../utils/functions');

module.exports = {
    name: 'alts',
    description: 'Fetches potential alts for a given Minecraft name.',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const name = args.slice(1).join(' ');

                if (!name) {
                    message.reply("Please Provide A Minecraft Name.");
                    return;
                }

                const replyMessage = await message.reply(`Fetching Alts For \`${name}\`...`);

                const uuid = await fetchMinecraftUuid(name);

                if (uuid == "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }

                const response = await fetch(`https://api.antisniper.net/v2/player/altfinder?key=${SnipeAPIKey}&player=${name}`);
                const data = await response.json();

                if (!data.success) {
                    await replyMessage.edit(`Failed To Fetch Alts: ${data.error}`);
                    return;
                }

                let quickBuyAlts = [];
                let linkedSocialsAlts = [];

                for (const alt of data.data) {
                    if (alt.method === "quickshop") {
                        quickBuyAlts.push(`\`${alt.ign}\``);
                    } else if (alt.method === "discord") {
                        linkedSocialsAlts.push(`\`${alt.ign}\``);
                    }
                }
                let altNumber = quickBuyAlts.length + linkedSocialsAlts.length;
                let altsMessage = `Found ${altNumber} Potential Alts Owned By \`${name}\`\n`;

                if (quickBuyAlts.length > 0) {
                    altsMessage += `\nQuick Buy (${quickBuyAlts.length})\n`;
                    altsMessage += quickBuyAlts.join(', ') + '\n';
                }

                if (linkedSocialsAlts.length > 0) {
                    altsMessage += `\nLinked Socials (${linkedSocialsAlts.length})\n`;
                    altsMessage += linkedSocialsAlts.join(', ') + '\n';
                }

                await replyMessage.edit(altsMessage);
            } catch (error) {
                console.log('Failed To Fetch Alts: ', error);
                message.reply("There Was An Error While Fetching Alts.");
            }
        }
};