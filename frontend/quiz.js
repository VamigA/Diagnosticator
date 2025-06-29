const API_URL = 'http://localhost:8000/v1/generate_question';

let currentQuestion = null;
let nextQuestion = null;
let correctIndex = null;
let selectedIndex = null;
let loadingNext = false;

const shuffle = array => {
	for(let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[array[i], array[j]] = [array[j], array[i]];
	}

	return array;
};

const convert = raw => {
	const answers = [
		{text: raw.right, correct: true},
		{text: raw.wrong_1, correct: false},
		{text: raw.wrong_2, correct: false},
		{text: raw.wrong_3, correct: false},
	];

	const shuffled = shuffle(answers);
	const correct = shuffled.findIndex(a => a.correct);

	return {
		question: raw.question,
		answers: shuffled.map(a => a.text),
		correct,
	};
};

const fetchQuestion = async () => {
	const res = await fetch(API_URL);
	const data = await res.json();
	return convert(data);
};

const renderQuestion = () => {
	const questionDiv = document.getElementById('question');
	const answersUl = document.getElementById('answers');
	const nextBtn = document.getElementById('next-btn');
	const loader = document.getElementById('loader');

	questionDiv.style.display = '';
	answersUl.innerHTML = '';
	nextBtn.style.display = 'none';
	loader.style.display = 'none';
	questionDiv.textContent = currentQuestion.question;

	currentQuestion.answers.forEach((ans, idx) => {
		const li = document.createElement('li');
		const btn = document.createElement('button');

		btn.className = 'answer-btn';
		btn.textContent = ans;
		btn.disabled = selectedIndex !== null;
		btn.addEventListener('click', () => selectAnswer(idx));

		if(selectedIndex !== null) {
			if(idx === currentQuestion.correct)
				btn.classList.add('correct');
			else if(idx === selectedIndex)
				btn.classList.add('wrong');
			else
				btn.style.opacity = '0.7';
		}

		li.appendChild(btn);
		answersUl.appendChild(li);
	});
};

const selectAnswer = idx => {
	if(selectedIndex !== null)
		return;

	selectedIndex = idx;
	renderQuestion();

	const nextBtn = document.getElementById('next-btn');
	nextBtn.style.display = '';
	nextBtn.disabled = loadingNext;
	nextBtn.textContent = loadingNext ? 'Генерация следующего вопроса...' : 'Далее';
};

const loadNextQuestion = async () => {
	loadingNext = true;
	const nextBtn = document.getElementById('next-btn');
	if(nextBtn) {
		nextBtn.disabled = true;
		nextBtn.textContent = 'Генерация следующего вопроса...';
	}

	nextQuestion = await fetchQuestion();
	loadingNext = false;
	if(nextBtn && selectedIndex !== null) {
		nextBtn.disabled = false;
		nextBtn.textContent = 'Далее';
	}
};

const startQuiz = async () => {
	const loader = document.getElementById('loader');
	loader.style.display = '';
	currentQuestion = await fetchQuestion();
	renderQuestion();
	loadNextQuestion();
};

const nextQuestionHandler = async () => {
	if(!nextQuestion)
		return;

	currentQuestion = nextQuestion;
	selectedIndex = null;

	renderQuestion();
	loadNextQuestion();
};

document.getElementById('next-btn').addEventListener('click', nextQuestionHandler);
window.addEventListener('load', startQuiz);