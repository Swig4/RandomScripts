const { EmbedBuilder } = require('discord.js');

module.exports = {
    name: 'help',
    description: 'Sends all commands for the bot',
    execute: async (client, message) => {
        const embed = new EmbedBuilder()
            .setTitle('Help')
            .setDescription('Here is the list of my commands:')
            .setColor('Red')
            .addFields(
                {
                    name: 'Owners Only',
                    value: `.mc ping\n.mc genkey\n.mc postrules`,
                    inline: true,
                },
                {
                    name: 'Server Commands',
                    value: `.mc info\n.mc givesupporter\n.mc givedrops\n.mc pingdrops\n.mc genalt\n.mc stock`,
                    inline: true,
                },
                {
                    name: 'Bedwars/Hypixel Commands',
                    value: `.mc boosters\n.mc bw <name>\n.mc status <name>\n.mc uuid <name>\n.mc name <UUID>\n.mc count\n.mc snpr | sniper <name>\n.mc ws <name>\n.mc alts <name>\n.mc qb | quickbuy <name>`,
                    inline: true,
                }
            );

        message.reply({
            embeds: [embed],
        });
    },
};
