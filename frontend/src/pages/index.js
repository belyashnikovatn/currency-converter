import './index.scss';

import { swapCurrencies } from "../components/swap";

const sourceInput = document.querySelector('.currency__value.source');
const resultInput = document.querySelector('.currency__value.result');
const sourceInfo = document.querySelector('.currency__info.source');
const resultInfo = document.querySelector('.currency__info.result');
const sourceRadios = document.querySelectorAll('.radio__input[name="source"]');
const resultRadios = document.querySelectorAll('.radio__input[name="result"]');
const swapButton = document.querySelector('.swap-button');

const symbol = {
  'RUB': '₽',
  'USD': '$',
  'EUR': '€',
};

// Получение данных курса
async function fetchExchangeRate(from, to, amount) {
  const amountWithDot = String(amount).replace(',', '.');
  // const response = await fetch(`https://currency-converter.hopto.org/api/convert?from=${from}&to=${to}&amount=${amountWithDot}`);
  const response = await fetch(`http://127.0.0.1:8000/api/convert?from=${from}&to=${to}&amount=${amountWithDot}`);
    const data = await response.json();
  return data;
}

// Форматирование перед выводом
function formatValue(value) {
  return value.toString().replace(/\./g, ',');
}

// Ограничение нажатия клавиш для контроля за вводимыми данными
function handleKeyDown(event) {
  const allowedKeys = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Home', 'End', ',', '.'];
  const isDigit = /\d/.test(event.key);

  if (!isDigit && !allowedKeys.includes(event.key)) {
    event.preventDefault();
  }

  if (event.key === ',' || event.key === '.') {
    const value = event.target.value;  
    if (value.includes(',') || value.includes('.')) {
      event.preventDefault();
    }
  }
}

// Форматирование: Удаление любых символов кроме цифр и одной запятой
// (разрешено воодить точку, но она заменяется на запятую)
// + запрет ввода более одного нуля перед запятой.
function handleInput(event) {
  let value = event.target.value;
  
  value = value.replace(/[^\d,\.]/g, '').replace(/\./g, ',');

  // Удаляет ноль в начале, если после него идет цифра
  if (value.match(/^0[0-9]/)) {
    value = value.substring(1);
  }

  // Добавляет ноль в начало, если первый символ запятая
  if (value.startsWith(',')) {
    value = '0' + value;
  }

  const parts = value.split(',');

  // Удаляет из строки все запятые кроме первой
  if (parts.length > 2) {
    value = parts[0] + ',' + parts.slice(1).join('');
  }


  event.target.value = value;
}

// Обновление данных конвертации
async function updateConversion(start = 'left') {

  let sourceValue = sourceInput.value.trim();
  let resultValue = resultInput.value.trim();
  const sourceCurrency = document.querySelector('.radio__input[name="source"]:checked').value.toUpperCase();
  const resultCurrency = document.querySelector('.radio__input[name="result"]:checked').value.toUpperCase();

  let initialValue;
  let fromCurrency;
  let toCurrency;

  if (start === 'right') {
    initialValue = parseFloat(resultValue.replace(',', '.'));
    fromCurrency = resultCurrency;
    toCurrency = sourceCurrency;
  } else {
    initialValue = parseFloat(sourceValue.replace(',', '.'));
    fromCurrency = sourceCurrency;
    toCurrency = resultCurrency;
  }

 if (!initialValue || initialValue <= 0 || isNaN(initialValue)) {
   start === 'right' 
     ? sourceInput.value = '' 
     : resultInput.value = '';
   sourceInfo.textContent = '';
   resultInfo.textContent = '';
   return;
 }

  if (sourceCurrency === resultCurrency) {
    resultInput.value = formatValue(initialValue);
    sourceInfo.textContent = formatValue(`1 ${symbol[sourceCurrency]} = 1 ${symbol[resultCurrency]}`);
    resultInfo.textContent = formatValue(`1 ${symbol[resultCurrency]} = 1 ${symbol[sourceCurrency]}`);
    return;
  }

  try {
    const data = await fetchExchangeRate(fromCurrency, toCurrency, initialValue);

    if (start === 'right') {
      sourceInput.value = formatValue(data.result.toFixed(2));
    } else {
      resultInput.value = formatValue(data.result.toFixed(2));
    }

    const rate = data.info.rate;
    sourceInfo.textContent = formatValue(`1 ${symbol[fromCurrency]} = ${rate.toFixed(2)} ${symbol[toCurrency]}`);
    resultInfo.textContent = formatValue(`1 ${symbol[toCurrency]} = ${(1 / rate).toFixed(2)} ${symbol[fromCurrency]}`);
  
  } catch (error) {
    console.error('Ошибка получения данных:', error);
  }
}

// Инвертирование по кнопке
swapButton.addEventListener('click', () => {
  swapCurrencies();
  updateConversion();
});

// Слушатели изменений радиокнопок и полей ввода
sourceRadios.forEach((radio) => radio.addEventListener('change', updateConversion));
resultRadios.forEach((radio) => radio.addEventListener('change', updateConversion));

sourceInput.addEventListener('keydown', handleKeyDown);
resultInput.addEventListener('keydown', handleKeyDown);

sourceInput.addEventListener('input', (e) => {
  handleInput(e);
  updateConversion();
});
resultInput.addEventListener('input', (e) => {
  handleInput(e);
  updateConversion('right')
});

updateConversion();
