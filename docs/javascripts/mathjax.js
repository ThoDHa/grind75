// MathJax setup for the LaTeX written in the problem and pattern write-ups.
//
// Arithmatex (`generic: true`) has already found the math at build time and
// wrapped it in `.arithmatex` spans using \(...\) and \[...\] delimiters, so
// MathJax only has to typeset those spans. Restricting it with
// `processHtmlClass` keeps it away from the literal dollar signs that appear in
// prose and code samples across the docs.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

// The theme enables `navigation.instant`, which swaps page content without a
// full reload. Without re-typesetting on each navigation, formulas render only
// on the first page loaded.
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
