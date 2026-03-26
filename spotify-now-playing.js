// Fetch and display Spotify now playing info
fetch('/spotify-info')
  .then(response => response.json())
  .then(data => {
    // Currently playing (left)
    const left = document.getElementById('spotify-currently-playing');
    let leftHtml = '';
    if (data.currently_playing && data.currently_playing.name) {
      const track = data.currently_playing;
      leftHtml += `
        <h3 style="margin-bottom:18px;">Currently listening to:</h3>
        <img src="${track.album_art}" alt="Album Art" style="height:200px;border-radius:10px;box-shadow:0 2px 8px #222;" />
        <h2 style="margin-top:16px;">${track.name}</h2>
        <p style="font-size:1.1em;">by ${track.artists.join(', ')}</p>
      `;
    } else {
      leftHtml += '<p>Not currently listening to anything.</p>';
    }
    left.innerHTML = leftHtml;

    // Top tunes (right)
    const right = document.getElementById('spotify-top-tracks');
    let rightHtml = '';
    if (data.top_tracks && Array.isArray(data.top_tracks) && data.top_tracks.length > 0) {
      rightHtml += '<h3>Most listened to this month:</h3><ul style="list-style:none;padding:0;">';
      data.top_tracks.forEach(track => {
        rightHtml += `
          <li style="margin-bottom:18px;display:flex;align-items:center;">
            <img src="${track.album_art}" alt="Album Art" style="height:60px;width:60px;border-radius:8px;margin-right:14px;box-shadow:0 1px 4px #222;" />
            <div>
              <strong>${track.name}</strong><br/>
              <span style="font-size:0.98em;">by ${track.artists.join(', ')}</span>
            </div>
          </li>
        `;
      });
      rightHtml += '</ul>';
    }
    right.innerHTML = rightHtml;
  })
  .catch(err => {
    document.getElementById('spotify-currently-playing').innerHTML = '<p>Could not load Spotify info.</p>';
    document.getElementById('spotify-top-tracks').innerHTML = '';
  });
