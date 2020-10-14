const $submitBtn = $("#submit-btn");
const $guessInput = $("#guess-input");
const $scoreboard = $("#scoreboard");
const $playAgainBtn = $("#play-again-btn")

const GAME_TIME = 60;

let totalScore = 0;

$submitBtn.on("click", async function(evt) {
    evt.preventDefault();

    if ($guessInput.val()) {
        let res = await sendGuessToServer($guessInput.val());
        const wordStatus = res.data.result;
        handleWordStatus(wordStatus, $guessInput.val());
        $guessInput.val("");
    }
});

$playAgainBtn.on("click", function() {
    location.reload();
})

async function sendGuessToServer(guess) {
    let res = await axios.get("/check-word", {params: {word: guess}});
    return res;
}

function handleWordStatus(status, word) {
    // Clear previous notifications
    $("#not-word-notification").hide();
    $("#not-on-board-notification").hide();
    switch(status) {
        case "not-on-board":
            $("#not-on-board-notification").show();
            break;
        case "ok":
            scoreboardUpdate(word);
            break;
        case "not-word":
            $("#not-word-notification").show();
            break;
        default:
            break;
      } 
}

// Display and update scoreboard
function scoreboardUpdate(word) {

    // Display scoreboard section if not already visible
    if ($scoreboard.is(":hidden")) {
        $scoreboard.show();
    }

    createScoreboardLI(word);

    totalScore += word.length;
    $("#total-score").text(totalScore);

}

// Create an li element for a score entry
function createScoreboardLI(word) {
    let $item = $(`<li>${word} - ${word.length}pts</li>`);
    $("#scoreboard-list").append($item);
}

// Endgame logic
async function endGame() {
    $("#not-word-notification").hide();
    $("#not-on-board-notification").hide();
    $("#instructions").text("Times up! Play again");
    $submitBtn.attr("disabled", true);
    $("#timer").text(0);
    clearInterval(gameTimer);
    res = await axios.post("/end-game", {score: totalScore});
    $("#highscore-display").text(res.data.highscore);
    $("#times-played-display").text(res.data.timesPlayed);
    $playAgainBtn.show();
}



// Initialization
$("#timer").text(GAME_TIME);
let timerValue = GAME_TIME;
setTimeout(endGame, GAME_TIME * 1000);
gameTimer = setInterval(function() { 
    $("#timer").text(--timerValue);
}, 1000);
