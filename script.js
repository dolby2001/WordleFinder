let patterns = [];
let word = '';

function runWordleSolver() {
    console.log('request');
    Loading();
    axios.get('http://localhost:5000/run_wordle_solver')
        .then(response => {
            clearInterval(intervalId); // Stop the loading animation
            console.log('Wordle Solver Result:', response.data.word);
            document.getElementById("answer").innerHTML = response.data.word;
            console.log(response.data.patterns);
            patterns = response.data.patterns;
            word = response.data.word;
            let words = response.data.words;
            patterns.forEach((pattern, rowIndex) => {
                for (let colIndex = 0; colIndex < pattern.length; colIndex++) {
                    const blockId = `bloc${colIndex + 1}`;
                    const blockElement = document.getElementById(`row${rowIndex + 1}`).querySelector(`#${blockId}`);

                    const letter = pattern[colIndex];
                    if (letter === "1") {
                        // Set background color to green for "1"
                        blockElement.style.backgroundColor = '#b59f3b';
                    } else if (letter === "2") {
                        // Set background color to red for "0"
                        blockElement.style.backgroundColor = '#538d4e';
                    }
                }
            });
            console.log(response.data.words);
            let guesses = '';
            words.forEach(word => {
                guesses += word + ', ';
            });
            guesses = guesses.slice(0, -2);

            document.getElementById('last').innerHTML = guesses;
        })
        .catch(error => {
            clearInterval(intervalId); // Stop the loading animation
            console.error('Error running Wordle Solver:', error);
        });
}

let intervalId; // Define intervalId outside the Loading function

function Loading() {
    console.log('loading');
    let answerElement = document.getElementById("answer");
    answerElement.innerHTML = "LOADING";
    
    // Add blinking dots every second
    let dots = 1;
    intervalId = setInterval(() => {
        answerElement.innerHTML = "LOADING" + ".".repeat(dots);
        dots = (dots % 4) + 1; // Cycle through 1, 2, 3, 4
    }, 1000);

    // Set a timeout to stop the loading after a certain time (e.g., 10 seconds)
    setTimeout(() => {
        clearInterval(intervalId);
        answerElement.innerHTML = "TIMEOUT: Unable to fetch word";
    },60000);
}

runWordleSolver();
