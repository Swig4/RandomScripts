require('dotenv').config();
require("moment-duration-format");

module.exports = {
    name: 'pingdrops',
    description: 'Pings people with the drops role',
    execute: async (client, message) => {
            let roleID = '1242283066739789987';
            if (message.member.roles.cache.has(roleID)) {
                message.reply('<@&1242994975793483897>');
                return;
            } else {
                message.reply('You Do Not Have The Drops Role.');
            }
        }
};