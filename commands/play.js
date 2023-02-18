const ytdl = require('ytdl-core');
const _ = require('lodash');
const yt = require('youtube-search-without-api-key');
const { SlashCommandBuilder } = require('discord.js');
const { joinVoiceChannel, createAudioPlayer, createAudioResource } = require('@discordjs/voice');

const playFunction = async (interaction) => {
	const voiceChannel = interaction.member.voice.channel;
	if (!voiceChannel) {
		await interaction.reply("You need to be in a voice channel to play music!");
		return;
	} else {
		const queryString = interaction.options.get('query');
		const videos = await yt.search(queryString.value);

		if (_.isEmpty(videos)) {
			await interaction.reply(`Cant find ${queryString} on Youtube!`);
			return;
		}
		
		const songInfo = await ytdl.getInfo(videos[0].snippet.url);
		const song = {
			title: songInfo.videoDetails.title,
			url: songInfo.videoDetails.video_url,
		};
		try {
			const player = createAudioPlayer();
			var connection = await joinVoiceChannel({
				channelId: interaction.member.voice.channel.id,
				guildId: interaction.guild.id,
				adapterCreator: interaction.guild.voiceAdapterCreator,
				selfDeaf: false,
				selfMute: false
			}).subscribe(player);
			const stream = await ytdl(song.url, {filter: "audioonly"})
			const resource = createAudioResource(stream);
			player.play(resource)
			// setTimeout(async()=>await connection.destroy(), 5000)
		} catch (err) {
			console.log(err);
		}
		await interaction.reply(`${song.title} added to the queue...`);
	}
	console.log('Hello');
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('play')
		.setDescription('Search the string in Youtube and plays the first entry!')
		.addStringOption(option => 
			option.setName('query')
			.setDescription('The string you type in youtube search bar')
			.setRequired(true)
		),
	execute: playFunction
};