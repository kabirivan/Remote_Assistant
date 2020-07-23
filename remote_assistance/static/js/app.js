const button = document.getElementById('join_leave');
const container = document.getElementById('container');
const count = document.getElementById('count');
const takePhoto = document.getElementById('take_photo');
const canvas = document.getElementById('canvas');
const photo = document.getElementById('photo');
var connected = false;
var room;
var localtracks;
var user_connected = false;
var videoPhoto;

Twilio.Video.createLocalTracks({
    audio: true,
}).then(function(localTracks) {
    localtracks = localTracks;
  });

function connectButtonHandler(event) {
    console.log('ok1')
    event.preventDefault();
    if (!connected) {
        var username = 'Asistente';
        button.disabled = true;
        button.innerHTML = 'Conectando...';
        button.setAttribute('class','btn btn-secondary');
        connect(username).then(() => {
            button.innerHTML = 'Colgar';
            button.setAttribute('class','btn btn-danger');
            button.disabled = false;
        }).catch(() => {
            alert('Conexión fallida. Asegúrate de tener internet y vuelvelo a intentar');
            button.innerHTML = 'Unirse';
            button.setAttribute('class','btn btn-success');
            button.disabled = false;
        });
    }
    else {
        disconnect();
        button.innerHTML = 'Unirse';
        connected = false;
    }
};

function connect(username) {
    var promise = new Promise((resolve, reject) => {
        // get a token from the back end
        fetch('/login', {
            method: 'POST',
            body: JSON.stringify({'username': username})
        }).then(res => res.json()).then(data => {
            // join video call
            return Twilio.Video.connect(data.token,{tracks: localtracks});
        }).then(_room => {
            room = _room;
            room.participants.forEach(participantConnected);
            room.on('participantConnected', participantConnected);
            room.on('participantDisconnected', participantDisconnected);
            connected = true;
            resolve();
        }).catch(() => {
            reject();
        });
    });
    return promise;
};

function participantConnected(participant) {
    var participant_div = document.createElement('div');
    participant_div.setAttribute('id', participant.sid);
    participant_div.setAttribute('class', 'participant');
    user_connected = true;
    var tracks_div = document.createElement('div');
    participant_div.appendChild(tracks_div);

    var label_div = document.createElement('div');
    label_div.innerHTML = participant.identity;
    participant_div.appendChild(label_div);

    container.appendChild(participant_div);

    participant.tracks.forEach(publication => {
        if (publication.isSubscribed)
            trackSubscribed(tracks_div, publication.track);
    });
    participant.on('trackSubscribed', track => trackSubscribed(tracks_div, track));
    participant.on('trackUnsubscribed', trackUnsubscribed);
};

function participantDisconnected(participant) {
    document.getElementById(participant.sid).remove();
    user_connected = false;
};

function trackSubscribed(div, track) {
    div.appendChild(track.attach());
    videoPhoto = track.attach();
};

function trackUnsubscribed(track) {
    track.detach().forEach(element => element.remove());
};

function disconnect() {
    room.disconnect();
    if(user_connected){
        container.removeChild(container.firstChild);
    }
    button.innerHTML = 'Unirse';
    button.setAttribute('class','btn btn-success');
    connected = false;
    user_connected = false;
};

function fn_get_photo(event){
    event.preventDefault();
    let contexto = canvas.getContext("2d");
    canvas.width = videoPhoto.videoWidth;
    canvas.height = videoPhoto.videoHeight;
    contexto.drawImage(videoPhoto, 0, 0, canvas.width, canvas.height);
    photo.src = canvas.toDataURL();

}

button.addEventListener('click', connectButtonHandler);
takePhoto.addEventListener('click',fn_get_photo);