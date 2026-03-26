// Fetch and display Spotify now playing info
fetch('/spotify-info')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('spotify-now-playing');
    let html = '';
    if (data.currently_playing && data.currently_playing.name) {
      const track = data.currently_playing;
      html += `
        <img src="${track.album_art}" alt="Album Art" style="height:100px;border-radius:8px;" />
        <h2>${track.name}</h2>
        <p>by ${track.artists.join(', ')}</p>
      `;
    } else {
      html += '<p>Not currently playing anything.</p>';
    }

    if (data.top_tracks && Array.isArray(data.top_tracks) && data.top_tracks.length > 0) {
      html += '<h3>Top Tracks</h3><ul style="list-style:none;padding:0;">';
      data.top_tracks.forEach(track => {
        html += `
          <li style="margin-bottom:16px;display:flex;align-items:center;">
            <img src="${track.album_art}" alt="Album Art" style="height:50px;width:50px;border-radius:6px;margin-right:12px;" />
            <div>
              <strong>${track.name}</strong><br/>
              <span>by ${track.artists.join(', ')}</span>
            </div>
          </li>
        `;
      });
      html += '</ul>';
    }
    container.innerHTML = html;
  })
  .catch(err => {
    document.getElementById('spotify-now-playing').innerHTML = '<p>Could not load Spotify info.</p>';
  });
