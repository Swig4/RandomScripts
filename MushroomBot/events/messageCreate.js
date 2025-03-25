module.exports = {
    name: 'messageCreate',
    async execute(client, message) {
        const prefix = '.mc';
        const args = message.content.slice(prefix.length).trim().split(/ +/);
        const commandName = args.shift().toLowerCase();
        const cooldowns = new Map();

        let whitelist = [
            { id: "1143663692878192861", username: "swig4" },
            { id: "1197930638800584765", username: "scoliosissy" },
            { id: "464287642356285442", username: "112batman" },
            { id: "1235237261461950495", username: "112sillyman" },
            { id: "309681798957498368", username: "sideload" },
            { id: "683364835685040143", username: "sun3k" },
            { id: "1264016430022529124", username: "swig5" }
        ];

        // Respond to mentions with "Hai Hai Hai!!" with cooldown
        if (message.mentions.has(client.user.id) && !message.reference && !message.author.bot) {
            if (!cooldowns.has('haiHaiHai') || Date.now() - cooldowns.get('haiHaiHai') > 4000) {
                if (!message.content.match(/@(everyone|here)/i)) {
                    message.reply("Hai Hai Hai!!");
                    cooldowns.set('haiHaiHai', Date.now());
                }
            }
        }

        // Handle commands starting with the prefix
        if (message.content.startsWith(prefix)) {
            if (!message.author.bot) {
                const validCommands = [
                    'info', 'ping', 'help', 'givesupporter', 'givedrops', 'genkey',
                    'boosters', 'pingdrops', 'bw', 'status', 'uuid', 'name',
                    'count', 'snpr', 'sniper', 'ws', 'alts', 'qb', 'quickbuy',
                    'postrules', 'genalt', 'stock'
                ];
                
                if (!validCommands.includes(commandName)) {
                    message.reply('Invalid command. Use `.mc help` for a list of available commands.');
                    return;
                }

                // Check whitelist for specific commands
                if (!whitelist.some(user => user.id === message.author.id)) {
                    if (['ping', 'genkey', 'postrules'].includes(commandName)) {
                        message.reply("You're Not Authorized To Use Any Owner Commands.");
                        return;
                    }
                }

                const command = client.commands.get(commandName);
                if (!command) return;

                try {
                    // Pass client to the command's execute function
                    await command.execute(client, message);
                } catch (error) {
                    console.error(error);
                    message.reply('There was an error trying to execute that command!');
                }
            }
        }
    }
};
