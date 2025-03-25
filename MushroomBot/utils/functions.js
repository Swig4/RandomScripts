require('dotenv').config();
const {
    Client,
    IntentsBitField,
} = require('discord.js');
require("moment-duration-format");
const cheerio = require('cheerio');

const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
        IntentsBitField.Flags.DirectMessages
    ]
});

const antiSnipeKey = process.env.ANTISNIPEKEY;
const polsuAPIKey = process.env.POLSUKEY;
const HypixelAPIKey = process.env.HYPIXELAPIKEY;


async function fetchMinecraftUsername(uuid) {
    try {
        uuid = uuid.toLowerCase();
        const response = await fetch(`https://mcuuid.net/?q=${uuid}`);
        const html = await response.text();
        const $ = cheerio.load(html);

        const username = $('#results_username').val().trim();
        return username || 'Unknown';
    } catch (error) {
        console.error('Error fetching Minecraft username:', error);
        return 'Unknown';
    }
}
async function fetchMinecraftUuid(name) {
    try {
        name = name.toLowerCase();
        const response = await fetch(`https://mcuuid.net/?q=${name}`);
        const html = await response.text();
        const $ = cheerio.load(html);

        const uuid = $('#results_raw_id').val().trim();
        return uuid || 'Unknown';
    } catch (error) {
        console.error('Error fetching Minecraft UUID:', error);
        return 'Unknown';
    }
}

async function getStatus(uuid) {
    const apiUrl = `https://api.hypixel.net/v2/status?uuid=${uuid}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'API-Key': HypixelAPIKey
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
        }

        const data = await response.json();
        if (!data.success) {
            throw new Error('API error: ' + (data.cause || 'Unknown error'));
        }

        return data;
    } catch (error) {
        console.error('Error Getting Status:', error);
        return 'There Was An Error Fetching Status.';
    }
}

async function getCount() {
    const apiUrl = `https://api.hypixel.net/v2/counts`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'API-Key': HypixelAPIKey
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
        }

        const data = await response.json();
        if (!data.success) {
            throw new Error('API error: ' + (data.cause || 'Unknown error'));
        }

        return data;
    } catch (error) {
        console.error('Error Getting Count:', error);
        return 'There Was An Error Fetching Count.';
    }
}

async function getQuickbuy(uuid) {
    const apiUrl = `https://api.polsu.xyz/polsu/bedwars/quickbuy?uuid=${uuid}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'API-Key': polsuAPIKey
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
        }

        const data = await response.json();
        if (!data.success) {
            throw new Error('API error: ' + (data.cause || 'Unknown error'));
        }

        return data;
    } catch (error) {
        console.error('Error Getting Quickbuy:', error);
        return 'There Was An Error Fetching Quickbuy.';
    }
}

async function sendNotification(messageContent, guildId, channelId) {
    const guild = await client.guilds.fetch(guildId);
    const channel = await guild.channels.fetch(channelId);
    return channel.send(messageContent);
}

async function signIn(Username, Password) {
    try {
        const res = await fetch('https://api.mushroomer.top/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: Username,
                password: Password
            }),
            credentials: 'include'
        });
        if (res.status === 400) throw new Error('Bad request');
        if (!res.ok) throw new Error('Unexpected server response');
        return true;
    } catch (error) {
        console.error('Error Signing in: ', error);
        return false;
    }
}

module.exports = {
    fetchMinecraftUuid,
    fetchMinecraftUsername,
    signIn,
    sendNotification,
    getQuickbuy,
    getCount,
    getStatus
};