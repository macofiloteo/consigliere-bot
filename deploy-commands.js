const { REST, Routes } = require('discord.js');
const { CLIENT_ID, GUILD_ID, TOKEN } = require('./config');
const fs = require('node:fs');


const deployCommands = async (clientId, guildId) => {
	const rest = new REST({ version: '10' }).setToken(TOKEN);
	const commands = [];
	// Grab all the command files from the commands directory you created earlier
	const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
	
	// Grab the SlashCommandBuilder#toJSON() output of each command's data for deployment
	for (const file of commandFiles) {
		const command = require(`./commands/${file}`);
		commands.push(command.data.toJSON());
	}
	
	try {
		console.log(`Started refreshing ${commands.length} application (/) commands.`);

		// The put method is used to fully refresh all commands in the guild with the current set
		const data = await rest.put(
			Routes.applicationGuildCommands(clientId, guildId),
			{ body: commands },
		);

		console.log(`Successfully reloaded ${data.length} application (/) commands.`);
	} catch (error) {
		// And of course, make sure you catch and log any errors!
		console.error(error);
	}
}

if (require.main === module) {
    deployCommands(CLIENT_ID, GUILD_ID);
}