const _ = require('lodash');
const { createAudioResource, createAudioPlayer, NoSubscriberBehavior } = require('@discordjs/voice');

const cache = {}

const getGuildQueueData = (guildID) => {
    const guildQueueData = cache[guildID];
    if (!guildQueueData) {
        throw new Error(`Guild ${guildID} not yet initialized!`);
    }
    return guildQueueData
};

const shiftSongQueueAndGetNextSongCache = (guildID) => {
    const guildQueueData = cache[guildID];
    if (!guildQueueData) {
        throw new Error(`Guild ${guildID} not yet initialized!`);
    }
    const { songQueue } = guildQueueData
    if (_.isEmpty(songQueue)) {
        return undefined;
    } else {
        return songQueue.shift();
    }
};

const addSongToCache = (guildID, songMetadata, songStream) => {
    const guildQueueData = cache[guildID];
    if (!guildQueueData) {
        throw new Error(`Guild ${guildID} not yet initialized!`);
    }
    const { songQueue } = guildQueueData;
    songQueue.push({
        metadata: songMetadata,
        resource: createAudioResource(songStream.stream, {
            inputType: songStream.type
        })
    });
}

const initializeGuild = (guildID) => {
    cache[guildID] = {
        isIdle: false,
        songQueue: [],
        player: createAudioPlayer(
            {
                behaviors: {
                    noSubscriber: NoSubscriberBehavior.Play
                }
            }
        )
    }
    return cache[guildID];
};
module.exports = {
	getGuildQueueData: getGuildQueueData,
    addSongToCache: addSongToCache,
    shiftSongQueueAndGetNextSongCache: shiftSongQueueAndGetNextSongCache,
    initializeGuild: initializeGuild
};