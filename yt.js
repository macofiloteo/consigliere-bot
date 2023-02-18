const yt = require('youtube-search-without-api-key');
const ytdl = require('ytdl-core');


const run = async () => {
    const videos = await yt.search('ram ranch');
    const hello = ytdl(videos[0].snippet.url);
    console.log(hello);
};
run();