// const swapButton = document.querySelector('.swap-button');
const sourceRadios = document.querySelectorAll('input[name="source"]');
const resultRadios = document.querySelectorAll('input[name="result"]');

let valueSource = Array.from(sourceRadios).find((radio) => radio.checked).value;
let valueResult = Array.from(resultRadios).find((radio) => radio.checked).value;

export function swapCurrencies() {
  let selectedSource = Array.from(sourceRadios).find((radio) => radio.checked);
  let selectedResult = Array.from(resultRadios).find((radio) => radio.checked);

  if (selectedSource && selectedResult) {
    selectedSource.checked = false;
    selectedResult.checked = false;

    const newSource = Array.from(sourceRadios).find(
      (radio) => radio.value === selectedResult.value
    );
    
    const newResult = Array.from(resultRadios).find(
      (radio) => radio.value === selectedSource.value
    );

    newSource.checked = true;
    newResult.checked = true;
    
    valueSource = newSource.value;
    valueResult = newResult.value;
  }
}

function preventSameCurrency(event) {
  const isSource = event.target.name === 'source';
  const isResult = event.target.name === 'result';

  const sourceChecked = Array.from(sourceRadios).find(radio => radio.checked);
  const resultChecked = Array.from(resultRadios).find(radio => radio.checked);

  if (sourceChecked.value === resultChecked.value) {
    if (isSource) {
      const newSource = Array.from(resultRadios).find(
      (radio) => radio.value === valueSource
      );
    
      if (newSource) {
        newSource.checked = true;
        valueResult = newSource.value;
      }
    } else if (isResult) {
      const newResult = Array.from(sourceRadios).find(
        (radio) => radio.value === valueResult
      );
    
      if (newResult) {
        newResult.checked = true;
        valueSource = newResult.value;
      }
    }
  } 

  if (isSource) {
    valueSource = event.target.value;
  } else if (isResult) {
    valueResult = event.target.value;
  }
}

// swapButton.addEventListener('click', swapCurrencies);

sourceRadios.forEach((radio) =>
  radio.addEventListener('change', preventSameCurrency)
);
resultRadios.forEach((radio) =>
  radio.addEventListener('change', preventSameCurrency)
);
