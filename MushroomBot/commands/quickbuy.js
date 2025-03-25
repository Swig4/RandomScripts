require('dotenv').config();
require("moment-duration-format");
const {
    fetchMinecraftUuid,
    getQuickbuy,
} = require('../utils/functions');

module.exports = {
    name: 'quickbuy',
    description: 'Fetches the users bedwars quickbuy',
    execute: async (client, message) => {
            try {
                const args = message.content.slice('.mc'.length).trim().split(/ +/);
                const name = args.slice(1).join(' ');
                if (!name) {
                    message.reply('Please Provide A Minecraft Name.');
                    return;
                }

                const replyMessage = await message.reply(`Fetching \`${name}\`'s Quickbuy...`);
                const uuid = await fetchMinecraftUuid(name);

                if (uuid == "Unknown") {
                    await replyMessage.edit(`Invalid Username Provided.`);
                    return;
                }

                const statusData = await getQuickbuy(uuid);

                if (typeof statusData === 'string') {
                    await replyMessage.edit(statusData);
                    return;
                }

                let image = statusData.data.image;
                replyMessage.edit(`\`${name}\`'s Quickbuy:\n[Image Link](${image})`)
            } catch (error) {
                console.log("error getting quickbuy", error);
                message.reply("There Was An Error Getting Their Quickbuy!");
            }
        }
};