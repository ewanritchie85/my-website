// Fetch and display Spotify now playing info
fetch('/spotify-info')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('spotify-now-playing');
    if (data.currently_playing && data.currently_playing.name) {
      const track = data.currently_playing;
      container.innerHTML = `
        <img src="${track.album_art}" alt="Album Art" style="height:100px;border-radius:8px;" />
        <h2>${track.name}</h2>
        <p>by ${track.artists.join(', ')}</p>
      `;
    } else {
      container.innerHTML = '<p>Not currently playing anything.</p>';
    }
  })
  .catch(err => {
    document.getElementById('spotify-now-playing').innerHTML = '<p>Could not load Spotify info.</p>';
  });
