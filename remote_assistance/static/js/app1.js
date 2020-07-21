const button = document.getElementById('join_leave');
const container = document.getElementById('container');
const photo = document.querySelector('#photo');
const canvas = document.querySelector("#canvas");
var connected = false;
var room;
var localtracks;
var user_connected = false;

Twilio.Video.createLocalTracks({
    audio: true,
    video: {facingMode : 'environment'}
}).then(function(localTracks) {
    var localMediaContainer = document.getElementById('local').firstChild;
    localtracks = localTracks;
    localTracks.forEach(function(track) {
      localMediaContainer.appendChild(track.attach());
    });
  });

function connectButtonHandler(event) {
    console.log('ok2')
    event.preventDefault();
    if (!connected) {
        var username = 'Usuario';
        button.disabled = true;
        button.innerHTML = 'Conectando...';
        button.setAttribute('class','btn btn-secondary');
        connect(username).then(() => {
            button.innerHTML = 'Colgar';
            button.setAttribute('class','btn btn-danger');
            button.disabled = false;
        }).catch(() => {
            alert('Falla en la conexión. Por favor asegurese de tener internet');
            button.innerHTML = 'Unirse';
            button.setAttribute('class','btn btn-success');
            button.disabled = false;
        });
    }
    else {
        disconnect();
        button.innerHTML = 'Unirse';
        button.setAttribute('class','btn btn-success');
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
    label_div.innerHTML ='Conectado con: ' + (participant.identity);
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
};

function trackUnsubscribed(track) {
    track.detach().forEach(element => element.remove());
};

function disconnect() {
    room.disconnect();
    if(user_connected){
        container.removeChild(container.lastChild);
    }
    button.innerHTML = 'Unirse';
    button.setAttribute('class','btn btn-success');
    connected = false;
    user_connected = false;
};

button.addEventListener('click', connectButtonHandler);