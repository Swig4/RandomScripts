require('dotenv').config();
require("moment-duration-format");
module.exports = {
    name: 'genkey',
    description: 'Generates a mushroom key',
    execute: async (client, message) => {
        let key = "bleh";
        message.author.send(`Here's Your Generated Key: \`${key}\`.\nYou can redeem your key at https://mushroomer.top by clicking the "Sign Up" button on the top right.`)
            .then(() => {
                message.reply('Check DMs!');
            })
            .catch(error => {
                console.error('Error sending DM:', error);
                message.reply('Failed to send DM. Please make sure your DMs are open.');
            });
    }
};