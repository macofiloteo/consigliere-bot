const _ = require('lodash');
const { SlashCommandBuilder } = require('discord.js');
const { addSongToCache, shiftSongQueueAndGetNextSongCache, getGuildQueueData, initializeGuild } = require('../song-cache');

const skipFunction = async (interaction) => {
	const voiceChannel = interaction.member.voice.channel;
	const guildID = interaction.guild.id;
	if (!voiceChannel) {
		await interaction.reply("You need to be in a voice channel to skip music!");
		return;
	}

    let guildSongData;
	try {
		guildSongData = getGuildQueueData(guildID);
	} catch {
		guildSongData = initializeGuild(guildID);
	}

    if (_.isEmpty(guildSongData.songQueue)) {
        await interaction.reply(`No song currently playing...`);
        return;
    }

    const skippedSong = shiftSongQueueAndGetNextSongCache(guildID);
    guildSongData = getGuildQueueData(guildID);
    if (!_.isEmpty(guildSongData.songQueue)) {
        guildSongData.player.play(guildSongData.songQueue[0].resource);
    } else {
        guildSongData.player.stop();
    }
    await interaction.reply(`Skipping ${skippedSong.metadata.title} Successfull...`);
    
};


module.exports = {
	data: new SlashCommandBuilder()
		.setName('skip')
		.setDescription('Skip the current song and play the next song in queue!'),
	execute: skipFunction
};