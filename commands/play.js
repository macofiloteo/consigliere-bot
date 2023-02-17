const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('play')
		.setDescription('Search the string in Youtube and plays the first entry!'),
	async execute(interaction) {
		const voiceChannel = interaction.member.voice.channelId;
		if (!voiceChannel) {
			await interaction.reply("You need to be in a voice channel to play music!");
			return;
		}
		console.log('Hello');
	},
};