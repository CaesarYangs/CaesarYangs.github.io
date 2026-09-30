/* Loaded only by pages that explicitly opt into mathematical notation. */
'use strict';
if (typeof window.renderMathInElement === 'function') {
  document.querySelectorAll('article[data-math]').forEach(article => {
    window.renderMathInElement(article, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '\\[', right: '\\]', display: true},
        {left: '\\(', right: '\\)', display: false}
      ],
      preProcess: expression => expression.normalize('NFKC').replaceAll('’', "'"),
      throwOnError: false,
      strict: 'ignore',
      trust: false
    });
  });
}
