// Declare all necessary variables
let scale = [], noteClicks = [], correct = 0.0, notes = document.querySelectorAll('.note')

// Configure the scale so it can track score appropriately
function setScale(arr) {
    scale = arr;

    // Disable other relevant buttons on page
    document.getElementById('start').disabled = true;
    document.getElementById('play-scale').disabled = true;
    document.getElementById('toggle-clef').disabled = true;

    // Track whether clef is showing while playing (for score bonus)
    if (document.getElementById('img-clef').style.visibility == 'hidden') {
        document.getElementById('showing-clef').value = "false";
    } else {
        document.getElementById('showing-clef').value = "true";
    }

    // Enable all notes to make them playable
    for (let i = 0; i < notes.length; i++) {
        notes[i].disabled = false;
    }
}

// Play major scale when play button is clicked
document.querySelector('#play-scale').addEventListener('click', function() {
    document.querySelector('#scale-audio').play();

    // Track that audio has been played (for score bonus)
    document.getElementById('played-audio').value = "true";
});

// Toggle Clef Visibility
buttonClef = document.querySelector('#toggle-clef');
imgClef = document.getElementById('img-clef');
buttonClef.addEventListener('click', function() {
    if (imgClef.style.visibility == 'visible') {
        imgClef.style.visibility = 'hidden';
        buttonClef.innerHTML = "Show Clef";
    } else {
        imgClef.style.visibility = 'visible';
        buttonClef.innerHTML = "Hide Clef";
    }
});

// Track (correct) clicks on note buttons and Display final results
function addClick(obj) {
    obj.disabled = true;
    noteClicks.push(obj);

    // Once 8 notes have been clicked (a full scale one-way)
    if (noteClicks.length == 8) {

        // Disable All Buttons
        for (let i = 0; i < notes.length; i++) {
            notes[i].disabled = true;
        }

        // Make buttons clicked green (right) or red (wrong)
        for (let i = 0; i < noteClicks.length; i++) {
            if (scale[i] === noteClicks[i].id) {
                correct += 1.0;
                noteClicks[i].style.backgroundColor = 'green';
            } else {
                noteClicks[i].style.backgroundColor = 'red';
            }
        }

        // Show how many user got correct
        if (correct < 8) {
            document.getElementById('showAnswer').innerHTML = "You got " + correct + " out of 8 correct.";
        } else {
            document.getElementById('showAnswer').innerHTML = "You got all 8 correct! Congratulations!";
        }
        document.getElementById('score').value = correct;
    }
}