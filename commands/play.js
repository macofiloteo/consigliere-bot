const play_dl = require('play-dl');
const _ = require('lodash');
const { SlashCommandBuilder } = require('discord.js');
const { joinVoiceChannel, getVoiceConnection, AudioPlayerStatus } = require('@discordjs/voice');
const { addSongToCache, shiftSongQueueAndGetNextSongCache, getGuildQueueData, initializeGuild } = require('../song-cache');


const playFunction = async (interaction) => {
	const voiceChannel = interaction.member.voice.channel;
	const guildID = interaction.guild.id;
	if (!voiceChannel) {
		await interaction.reply("You need to be in a voice channel to play music!");
		return;
	}

	await interaction.deferReply();
	let guildSongData;
	try {
		guildSongData = getGuildQueueData(guildID);
	} catch {
		guildSongData = initializeGuild(guildID);
	}
	let queryString = interaction.options.get('query');
	queryString = queryString.value
	let videoURL;
	if (queryString.includes('https') || queryString.includes('www')) {
		videoURL = queryString
	} else {
		const videos = await play_dl.search(queryString, {
            limit: 1
        })
		if (_.isEmpty(videos)) {
			await interaction.reply(`Cant find ${queryString} on Youtube!`);
			return;
		}
		videoURL = videos[0].url
	}
	let yt_info = await play_dl.video_info(videoURL)
	if (_.isEmpty(yt_info)) {
		await interaction.reply(`Cant find ${queryString} on Youtube!`);
		return;
	}
	const song = {
		title: yt_info.video_details.title,
		url: videoURL,
	};
	const stream = await play_dl.stream_from_info(yt_info)
	addSongToCache(guildID, song, stream)

	let voiceConnection = await getVoiceConnection(guildID);
	guildSongData = getGuildQueueData(guildID);
	if (!voiceConnection) {
		voiceConnection = await joinVoiceChannel({
			channelId: interaction.member.voice.channel.id,
			guildId: guildID,
			adapterCreator: interaction.guild.voiceAdapterCreator,
			selfDeaf: false,
			selfMute: false
		})
	}
	voiceConnection.subscribe(guildSongData.player);

	if (guildSongData.songQueue.length <= 1) {
		await interaction.editReply(`Now Playing: ${song.url}...`);
		guildSongData.player.play(guildSongData.songQueue[0].resource);
	} else {
		await interaction.editReply(`Added to Queue: ${song.url}...`);
	}
	if (!guildSongData.player['_events']['idle']) {
		guildSongData.player.on(AudioPlayerStatus.Idle, async () => {
			shiftSongQueueAndGetNextSongCache(guildID);
			guildSongData = getGuildQueueData(guildID);
			if (!_.isEmpty(guildSongData.songQueue)) {
				const { metadata, resource } = guildSongData.songQueue[0];
				await interaction.channel.send(`Now Playing: ${metadata.title}...`);
				guildSongData.player.play(resource);
				
			} else {
				await interaction.channel.send(`No more song to play...`);
			}
		});
	}
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