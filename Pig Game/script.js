'use strict';
const initScore = 0;
let whoseTurn = 0; // if even player one, else player 2
let totalScorePlayers = [initScore, initScore];
let currentScorePlayers = [initScore, initScore];
let randomNumber = initScore; // to have data of current scores in our js and not just on the DOM
const NewGameButton = document.querySelector('.btn--new');
const TotalScorePlayerObjArr = document.querySelectorAll('.score');
const CurrentScorePlayerObjArr = document.querySelectorAll('.current-score');
const Players = document.querySelectorAll('.player');
const RollDiceButton = document.querySelector('.btn--roll');
const DiceImgArr = document.querySelectorAll('.dice');
const holdButton = document.querySelector('.btn--hold');
let PreviousWinner = Players[0];

const setAllImgToHidden = function () {
  for (let i = 0; i < DiceImgArr.length; i++) {
    if (!DiceImgArr[i].classList.contains('hidden')) {
      DiceImgArr[i].classList.add('hidden');
    }
  }
};

const whoseTurnIsit = function () {
  return whoseTurn % 2 === 0
    ? CurrentScorePlayerObjArr[0]
    : CurrentScorePlayerObjArr[1];
};

const newGameButtonHandler = function () {
  totalScorePlayers[0] = initScore;
  totalScorePlayers[1] = initScore; // to have data of current scores in our js and not just on the DOM
  currentScorePlayers[0] = initScore;
  currentScorePlayers[1] = initScore;
  CurrentScorePlayerObjArr[0].textContent = initScore;
  CurrentScorePlayerObjArr[1].textContent = initScore;
  TotalScorePlayerObjArr[0].textContent = initScore;
  TotalScorePlayerObjArr[1].textContent = initScore;
  PreviousWinner.classList.remove('player--winner', 'name');
  Players[0].classList.add('player--active');
  Players[1].classList.remove('player--active');

  RollDiceButton.addEventListener('click', rollDiceHandler);
  holdButton.addEventListener('click', holdButtonHandler);
  randomNumber = 0;
  whoseTurn = initScore;
  setAllImgToHidden();
};

NewGameButton.addEventListener('click', newGameButtonHandler);

const rollDiceHandler = function () {
  let random;
  random = randomDiceGenerator();
  showPic(random);
  const player = whoseTurnIsit();
  if (random === 1) {
    whoseTurn = (whoseTurn + 1) % 2;
    console.log(whoseTurn);
    player.textContent = 0;
    activePlayerDisplayToggle();
  } else {
    player.textContent = Number(player.textContent) + random;
  }
};

const showPic = function (num) {
  for (let i = 0; i < DiceImgArr.length; i++) {
    if (num === i + 1) {
      setAllImgToHidden();
      DiceImgArr[i].classList.remove('hidden');
      break;
    }
  }
};

const randomDiceGenerator = () => Math.trunc(Math.random() * 6) + 1;

RollDiceButton.addEventListener('click', rollDiceHandler);

const holdButtonHandler = function () {
  const currentPlayer = whoseTurnIsit();
  activePlayerDisplayToggle();
  for (let i = 0; i < CurrentScorePlayerObjArr.length; i++) {
    if (currentPlayer === CurrentScorePlayerObjArr[i]) {
      //or you can pass in whoseTurn as the index of the array , thereby eliminating the for loop
      TotalScorePlayerObjArr[i].textContent =
        Number(TotalScorePlayerObjArr[i].textContent) +
        Number(CurrentScorePlayerObjArr[i].textContent);

      if (Number(TotalScorePlayerObjArr[i].textContent) >= 100) {
        Players[i].classList.add('player--winner', 'name');
        holdButton.removeEventListener('click', holdButtonHandler);
        RollDiceButton.removeEventListener('click', rollDiceHandler);
        PreviousWinner = Players[i];
        Players[1 - i].classList.remove('player--active');
      } else CurrentScorePlayerObjArr[i].textContent = 0;
      break;
    }
  }
  whoseTurn = (whoseTurn + 1) % 2;
  console.log(whoseTurn);
};

holdButton.addEventListener('click', holdButtonHandler);

const activePlayerDisplayToggle = function () {
  document.querySelector('.player--0').classList.toggle('player--active');
  document.querySelector('.player--1').classList.toggle('player--active');
};
