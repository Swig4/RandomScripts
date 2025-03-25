require('dotenv').config();
require("moment-duration-format");

const cooldowns = new Map();
module.exports = {
    name: 'givedrops',
    description: 'Gives user the drops role',
    execute: async (client, message) => {
            try {
                if (!cooldowns.has('givedrops') || Date.now() - cooldowns.get('givedrops') > 5000) {
                    cooldowns.set('givedrops', Date.now());

                    let roleID = '1242994975793483897';
                    let role = message.guild.roles.cache.get(roleID);
                    if (!role) {
                        throw new Error('Role Not Found For This Server.');
                    }

                    if (message.member.roles.cache.has(roleID)) {
                        await message.member.roles.remove(role);
                        message.reply('You Will No Longer Be Pinged For Drops.');
                    } else {
                        await message.member.roles.add(role);
                        message.reply('You Will Now Be Pinged For Drops!');
                    }
                } else {
                    message.reply("Command Is On Cooldown For This Server. Please Wait Before Using It Again.");
                }
            } catch (error) {
                console.error('Error assigning/removing role:', error);
                message.reply('An error occurred while assigning or removing the role.');
            }
        }
};