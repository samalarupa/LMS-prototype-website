const quizData = [
	{
		question: "What is the output of the following C program: `int x = 5; printf(\"%d\", x);`?",
		options: ["5", "10", "15", "Error"],
		answer: "5"
	},
	{
		question: "What is the purpose of the `#include` directive in C?",
		options: ["To define a function", "To include a header file", "To declare a variable", "To print a message"],
		answer: "To include a header file"
	},
	{
		question: "What is the difference between `=` and `==` in C?",
		options: ["`=` is used for assignment, `==` is used for comparison", "`=` is used for comparison, `==` is used for assignment", "Both are used for assignment", "Both are used for comparison"],
		answer: "`=` is used for assignment, `==` is used for comparison"
	},
	// Add more questions here
];

let currentQuestion = 0;
let score = 0;

document.getElementById("question").innerHTML = quizData[currentQuestion].question;
document.getElementById("option1").nextSibling.innerHTML = quizData[currentQuestion].options[0];
document.getElementById("option2").nextSibling.innerHTML = quizData[currentQuestion].options[1];
document.getElementById("option3").nextSibling.innerHTML = quizData[currentQuestion].options[2];
document.getElementById("option4").nextSibling.innerHTML = quizData[currentQuestion].options[3];

document.getElementById("submit-btn").addEventListener("click", checkAnswer);

function checkAnswer() {
	const userAnswer = document.querySelector('input[name="option"]:checked').value;
	if (userAnswer === quizData[currentQuestion].answer) {
		score++;
	}
	currentQuestion++;
	if (currentQuestion < quizData.length) {
		document.getElementById("question").innerHTML = quizData[currentQuestion].question;
		document.getElementById("option1").nextSibling.innerHTML = quizData[currentQuestion].options[0];
		document.getElementById("option2").nextSibling.innerHTML = quizData[currentQuestion].options[1];
		document.getElementById("option3").nextSibling.innerHTML = quizData[currentQuestion].options[2];
		document.getElementById("option4").nextSibling.innerHTML = quizData[currentQuestion].options[3];
	} else {
		document.getElementById("result-container").style.display = "block";
		document.getElementById("result").innerHTML = `You scored ${score} out of ${quizData.length}`;
	}
}