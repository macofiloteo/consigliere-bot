require('dotenv').config()

const CONFIG = {
    PREFIX: "!",
    CLIENT_ID: process.env.CLIENT_ID,
    GUILD_ID: process.env.GUILD_ID,
    TOKEN: process.env.TOKEN
}

module.exports = { ...CONFIG };
