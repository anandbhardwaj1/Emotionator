// Script to handle video camera status

var vidStatus = document.getElementById('camera-status');
navigator.getMedia = ( navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

navigator.getMedia({video: true}, function() {
    vidStatus.style = "color: #2ECC40;";
    vidStatus.innerHTML = 'Available';
}, function() {
    vidStatus.style = "color: #FF4136;";
    vidStatus.innerHTML = 'Not Available';
    document.getElementById('record-video').disabled = true;
});

// Function to handle navbar layout on scrolling 

window.addEventListener('scroll',function(e) {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        document.getElementById('navbar').style.position = 'fixed';
    }
    else {
        document.getElementById('navbar').style.position = 'sticky';
    }
});

// Script to handle video recording status bar 

var rflag = 0;
function move() {
    if (rflag == 0) {
        rflag = 1;
        var elem = document.getElementById("bar");
        var width = 1;
        var id = setInterval(frame, 68);
        function frame() {
            if (width >= 100) {
                clearInterval(id);
                rflag = 0;
            } 
            else {
                width++;
                elem.style.width = width + "%";
            }
        }
    }
}


// Script to handle uploading and reccording audio files

URL = window.URL || window.webkitURL;

var gumStream; 						
var rec; 							
var input; 							

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input,{numChannels:1})
        rec.record()
        console.log("Recording started");

    }).catch(function(err) {
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
};

function pauseRecording() {
    
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording) {
        rec.stop();
        pauseButton.innerHTML="Resume";
    }
    else {
        rec.record()
        pauseButton.innerHTML="Pause";

    }
};

function stopRecording() {

    console.log("stopButton clicked");

    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;
    pauseButton.innerHTML="Pause";

    rec.stop();
    gumStream.getAudioTracks()[0].stop();

    rec.exportWAV(createDownloadLink);
};

function createDownloadLink(blob) {
    
    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('div');
    var link = document.createElement('a');

    var filename = new Date().toISOString();

    au.controls = true;
    au.src = url;

    link.href = url;
    link.download = filename+".wav";
    link.classList.add('record-link', 'btn', 'btn-info');
    link.innerHTML = "Save to disk";

    li.appendChild(au);
    li.appendChild(link);
    
    var upload = document.createElement('a');
    upload.href="#";
    upload.classList.add('record-link', 'btn', 'btn-success');
    upload.innerHTML = "Upload";
    upload.addEventListener("click", function(event){
            var fd=new FormData();
            fd.append('csrfmiddlewaretoken', csrftoken);
            fd.append("audio-file",blob, filename);
            fd.append('source', 'recording');
            $.ajax({
                    type: 'POST',
                    url: '/speech-emotion',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        updateEmotions(response, 'audio');
                        console.log(window.emotions);
                    }
                });
        });
    li.appendChild(document.createTextNode (" "));
    li.appendChild(upload);

    recordingsList.innerHTML = '';
    recordingsList.appendChild(li);
}

// Function to update emotion state-variables according to the user input

function updateEmotions(emotionProbs, source) {

    if(source != 'form') {
        window.inputs += 1;
        
        emotionProbs['happy'] *= window.weightage[source];
        emotionProbs['sad'] *= window.weightage[source];
        emotionProbs['angry'] *= window.weightage[source];
        emotionProbs['calm'] *= window.weightage[source];

        if(window.inputs > 1) {

            window.emotions['happy'] *= (window.inputs - 1)/window.inputs;
            window.emotions['sad'] *= (window.inputs - 1)/window.inputs;
            window.emotions['angry'] *= (window.inputs - 1)/window.inputs;
            window.emotions['calm'] *= (window.inputs - 1)/window.inputs;
    
            emotionProbs['happy'] *= (window.inputs - 1)/window.inputs;
            emotionProbs['sad'] *= (window.inputs - 1)/window.inputs;
            emotionProbs['angry'] *= (window.inputs - 1)/window.inputs;
            emotionProbs['calm'] *= (window.inputs - 1)/window.inputs;
        }

        window.emotions['happy'] += emotionProbs['happy'];
        window.emotions['sad'] += emotionProbs['sad'];
        window.emotions['angry'] += emotionProbs['angry'];
        window.emotions['calm'] += emotionProbs['calm'];

        document.getElementById('happy-prob').innerHTML = roundProb(window.emotions['happy']);
        document.getElementById('sad-prob').innerHTML = roundProb(window.emotions['sad']);
        document.getElementById('angry-prob').innerHTML = roundProb(window.emotions['angry']);
        document.getElementById('calm-prob').innerHTML = roundProb(window.emotions['calm']);

        document.getElementById(`${source}-emotion-holder`).classList.remove('hide');
        document.getElementById(`${source}-happy-state-value`).innerHTML = `${roundProb(emotionProbs['happy'])} %`;
        document.getElementById(`${source}-sad-state-value`).innerHTML = `${roundProb(emotionProbs['sad'])} %`;
        document.getElementById(`${source}-angry-state-value`).innerHTML = `${roundProb(emotionProbs['angry'])} %`;
        document.getElementById(`${source}-calm-state-value`).innerHTML = `${roundProb(emotionProbs['calm'])} %`;
        setEmotions(window.emotions);
    
    }

    else {
        window.inputs = 0;

        window.emotions['happy'] = emotionProbs['happy'];
        window.emotions['sad'] = emotionProbs['sad'];
        window.emotions['angry'] = emotionProbs['angry'];
        window.emotions['calm'] = emotionProbs['calm'];

        setEmotions(window.emotions);

        window.emotions['happy'] = 0;
        window.emotions['sad'] = 0;
        window.emotions['angry'] = 0;
        window.emotions['calm'] = 0;

        document.getElementById('happy-prob').innerHTML = roundProb(window.emotions['happy']);
        document.getElementById('sad-prob').innerHTML = roundProb(window.emotions['sad']);
        document.getElementById('angry-prob').innerHTML = roundProb(window.emotions['angry']);
        document.getElementById('calm-prob').innerHTML = roundProb(window.emotions['calm']);
    }
};

// Helper function to round a number to two-decimal places

function roundProb(num) {
    return Math.round(num * 100) / 100;
};


// Function to fetch final emotions from emotion probabilities

function setEmotions(emotionVals) {
    $.ajax({
        type: 'POST',
        url: '/identify-emotion',
        data: {
            csrfmiddlewaretoken: csrftoken,
            'happy' : emotionVals['happy'],
            'sad' : emotionVals['sad'],
            'angry' : emotionVals['angry'],
            'calm' : emotionVals['calm']
        },
        success: function(response) {
            window.primary_emotion = response['primaryEmotion'];
            window.enhanced_emotion = response['enhancedEmotion'];
            console.log(primary_emotion);
            console.log(enhanced_emotion);
            pEmotion = document.getElementById('primary-emotion');
            eEmotion = document.getElementById('enhanced-emotion');

            pEmotion.innerHTML = sentenceCase(primary_emotion)
            pEmotion.classList.remove('font-italic', 'text-muted');
            eEmotion.innerHTML = sentenceCase(enhanced_emotion)
            eEmotion.classList.remove('font-italic', 'text-muted');
        }
    });

    // Helper function to capitalize first letter of a sentence

    function sentenceCase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    };
};

// Function to fetch appropriate genres and web content using the final emotions

function getGenres(primaryEmotion, enhancedEmotion) {
    if(primaryEmotion == "Null" || primaryEmotion == "") {
        window.alert("No Emotions Available!");
    }
    else {
        document.getElementById('genre-loader').classList.remove('hide');
        $.ajax({
            type: 'POST',
            url: '/recommend-genres',
            data: {
                csrfmiddlewaretoken: csrftoken,
                'primary-emotion': primaryEmotion,
                'enhanced-emotion': enhancedEmotion
            },
            success: function(response) {
                console.log("Got genres");
                window.genres = response;
                document.getElementById('genre-loader').classList.add('hide');
                fillGenres(window.genres);
                fillContent(window.genres);
            },
            error: function(error) { 
                console.log(error);
                window.alert("Network Error!");
                document.getElementById('genre-loader').classList.add('hide');
            }    
        });
    }
};

// Function to fill fetched genres to the Genre panel

function fillGenres(genreDict) {
    musicGenreList = document.getElementById('music-genre-list');
    videoGenreList = document.getElementById('video-genre-list');
    newsGenreList = document.getElementById('news-genre-list');

    musicGenreList.innerHTML = '';
    videoGenreList.innerHTML = '';
    newsGenreList.innerHTML = '';

    for(genre in genreDict['musicGenres']) {
        musicGenreList.innerHTML += `<li class="genre">${capCase(genreDict['musicGenres'][genre])}</li>`;
    };
    for(genre in genreDict['videoGenres']) {
        if(genreDict['videoGenres'][genre] == 'facts english') {
            videoGenreList.innerHTML += `<li class="genre">${capCase('informative')}</li>`;
        }
        else {
            videoGenreList.innerHTML += `<li class="genre">${capCase(genreDict['videoGenres'][genre])}</li>`;
        }
    };
    for(genre in genreDict['newsGenres']) {
        if(genreDict['newsGenres'][genre] == 'world') {
            newsGenreList.innerHTML += `<li class="genre">${capCase('positive')}</li>`;
        }
        else {
            newsGenreList.innerHTML += `<li class="genre">${capCase(genreDict['newsGenres'][genre])}</li>`; 
        }
    };

    function capCase(string) {
        if(typeof(string) == 'object') {
            return string;
        }
        return string.charAt(0).toUpperCase() + string.slice(1);
    };
};

// Function to fill music titles into the content page

function fillContent(genreDict) {

    // Removing filler content

    var fillerList = document.getElementsByClassName('genre-filler');
    fillerList[0].classList.add("hide");
    fillerList[1].classList.add("hide");
    fillerList[2].classList.add("hide");

    // Filling music content

    musicList = document.getElementById('music-list');

    musicList.innerHTML = '';

    for(genre in genreDict['musicContent']) {
        var i;
        for(i = 0; i < 25; i++) {
            musicList.innerHTML += 
            `
            <li class="music-item">
                <img class="list-pic cover-art" src="${genreDict['musicContent'][genre]['cover_art'][i]}" alt="cover-art">
                <p class="music-info text-left">
                    <span class="music-title">${genreDict['musicContent'][genre]['track_name'][i]}</span>
                    <br>
                    <span class="small music-artist">${genreDict['musicContent'][genre]['artist_name'][i]}</span>
                    <br>
                    <a class="music-link btn btn-success" href="${genreDict['musicContent'][genre]['track_url'][i]['spotify']}" target="_blank">PLAY</a>
                </p>
            </li>
            `
        }
    }

    // Filling video content

    videosList = document.getElementById('videos-list');

    videosList.innerHTML = '';

    function youtubeURL(id) {
        return `https://www.youtube.com/watch?v=${id}`
    };

    function titleLim(title) {
        if(title.length > 65) {
            return (title.slice(0, 65) + "...")
        }
        else {
            return title
        }
    };

    for(genre in genreDict['videoContent']) {
        var i;
        for(i = 0; i < 50; i++) {
            videosList.innerHTML += 
            `
            <li class="video-item">
                <img class="list-pic video-thumb" src="${genreDict['videoContent'][genre]['thumbnails'][i]}" alt="video-thumbnail">
                <p class="video-info text-left">
                    <span class="video-title">${titleLim(genreDict['videoContent'][genre]['title'][i])}</span>
                    <br>
                    <span class="small video-artist">${genreDict['videoContent'][genre]['channelTitle'][i]}</span>
                    <br>
                    <a class="video-link btn btn-success" href="${youtubeURL(genreDict['videoContent'][genre]['videoId'][i])}" target="_blank">PLAY</a>
                </p>
            </li>
            `
        }
    }

    // Filling news content

    newsList = document.getElementById('news-list');

    newsList.innerHTML = '';

    for(genre in genreDict['newsContent']) {
        var i;
        for(i = 0; i < 20; i++) {
            newsList.innerHTML += 
            `
            <li class="news-item">
                <img class="list-pic news-image" src="${genreDict['newsContent'][genre][2][i]}" alt="news-pic">
                <p class="news-info text-left">
                    <span class="news-title">${genreDict['newsContent'][genre][0][i]}</span>
                    <br>
                    <a class="news-link btn btn-success" href="${genreDict['newsContent'][genre][1][i]}" target="_blank">READ MORE</a>
                </p>
            </li>
            `
        }
    }

};

// Function to clear the currently measured emotional levels 

function clearGenres() {
    console.log(window.emotions['happy']);

    window.emotions['happy'] = 0;
    document.getElementById('happy-prob').innerHTML = 0;
    window.emotions['sad'] = 0;
    document.getElementById('sad-prob').innerHTML = 0;
    window.emotions['angry'] = 0;
    document.getElementById('angry-prob').innerHTML = 0;
    window.emotions['calm'] = 0;
    document.getElementById('calm-prob').innerHTML = 0;
    setEmotions(window.emotions);
    window.inputs = 0;

    pEmotion = document.getElementById('primary-emotion');
    eEmotion = document.getElementById('enhanced-emotion');

    pEmotion.innerHTML = 'N/A';
    pEmotion.classList.add('font-italic', 'text-muted');
    eEmotion.innerHTML = 'N/A';
    eEmotion.classList.add('font-italic', 'text-muted');

    console.log(window.emotions['happy']);
};

// jQuery functions

$(document).ready(function() {

    // Declaring global state variables in 'window' scope

    window.inputs = 0;
    window.weightage = {
        'audio' : 0.75,
        'video' : 0.84
    };
    window.emotions = {
        'happy' : 0,
        'sad' : 0,
        'angry' : 0,
        'calm' : 0
    };

    window.primary_emotion = '';
    window.enhanced_emotion = '';

    window.genres = {};

    // Submit event-handler function for Emotion form

    $('#emotion-input-form').submit(function(event) {
        event.preventDefault();
        console.log('Form Submitted Successfully');
        console.log($('#primary-emotion-sel').val());
        console.log($('#enhanced-emotion-sel').val());
        emotionVals =  {
            'happy' : 0,
            'sad' : 0,
            'angry' : 0,
            'calm' : 0
        };
        emotionVals[$('#primary-emotion-sel').val()] = 100;
        if($('#enhanced-emotion-sel').val() != 'null' && $('#enhanced-emotion-sel').val() != $('#primary-emotion-sel').val()) {
            emotionVals[$('#enhanced-emotion-sel').val()] = 50;
        }
        updateEmotions(emotionVals, 'form');
        console.log(window.emotions);
    });

    // Event handler function for uploading pre-existing audio-files

    $('#audio-input-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        formData.append('source', 'upload');
        console.log('Audio Uploaded Successfully');
        $.ajax({
            type: 'POST',
            url: '/speech-emotion',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                updateEmotions(response, 'audio');
                console.log(window.emotions);
            }
        });
    });

    // Function to initiate video capture session and facial emotion recognition

    $('#record-video').click(function(event) {
        var rstate = document.getElementById('record-status');
        rstate.innerHTML = 'Recording';
        rstate.style = "color: #2ECC40;"
        move();
        $.ajax({
            type: 'POST',
            url: '/facial-emotion',
            data: {
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(response) {
                updateEmotions(response, 'video');
                console.log(window.emotions);
                rstate.style = "color: #FF4136;"
                rstate.innerHTML = 'Not Recording';
            }
        });
    });

    // Function to initiate fetching of web-content

    $('#get-genres').click(function(event) {
        console.log('Fetching Genres');
        getGenres(window.primary_emotion, window.enhanced_emotion);
    });

    // Function to initiate emotion reset

    $('#clear-genres').click(function(event) {
        console.log('Clearing Emotions');
        clearGenres();
    });
    
});