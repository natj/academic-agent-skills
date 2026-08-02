# LaTeX Conventions

Technical LaTeX conventions. When editing or writing LaTeX, always use the macros defined below instead of raw markup.


## Document Class & Key Packages

Key packages: `amsmath`, `amssymb`, `bm`, `natbib`, `hyperref`, `color`, `ulem`, `graphicx`, `times,txfonts`.

Bibliography style: `\bibpunct{(}{)}{;}{a}{}{,}` (A&A author-year style).


## Custom Commands

### Unit Macros

All units use `\unitspace` (`\,`) for thin space before the unit.

Definitions:

```latex
\newcommand{\unitspace}{\,}
\newcommand{\km}{\ensuremath{\unitspace \mathrm{km}}}
\newcommand{\meter}{\ensuremath{\unitspace \mathrm{m}}}
\newcommand{\cm}{\ensuremath{\unitspace \mathrm{cm}}}
\newcommand{\g}{\ensuremath{\unitspace \mathrm{g}}}
\newcommand{\Hz}{\ensuremath{\unitspace \mathrm{Hz}}}
\renewcommand{\sec}{\ensuremath{\unitspace \mathrm{s}}}
\newcommand{\yr}{\ensuremath{\unitspace \mathrm{yr}}}
\newcommand{\erg}{\ensuremath{\unitspace \mathrm{erg}}}
\newcommand{\ergs}{\ensuremath{\unitspace \mathrm{erg}\,\mathrm{s}^{-1}}}
\newcommand{\Gauss}{\ensuremath{\unitspace \mathrm{G}}}
\newcommand{\Kelvin}{\ensuremath{\unitspace \mathrm{K}}}
\newcommand{\keV}{\ensuremath{\unitspace \mathrm{keV}}}
\newcommand{\Msun}{\ensuremath{\unitspace \mathrm{M}_{\odot}}}
```

Quick reference:

| Command     | Output              | Example usage           |
|-------------|----------------------|------------------------|
| `\km`       | `\, km`             | `$10\km$`              |
| `\meter`    | `\, m`              | `$1\meter$`            |
| `\cm`       | `\, cm`             | `$R = 10^6\cm$`        |
| `\g`        | `\, g`              | `$\rho = 10^{14}\g$`   |
| `\Hz`       | `\, Hz`             | `$\nu = 10^9\Hz$`      |
| `\sec`      | `\, s`              | `$t = 0.1\sec$`        |
| `\yr`       | `\, yr`             | `$\tau = 10^6\yr$`     |
| `\erg`      | `\, erg`            | `$E = 10^{33}\erg$`    |
| `\ergs`     | `\, erg s^{-1}`     | `$L = 10^{36}\ergs$`   |
| `\Gauss`    | `\, G`              | `$B = 10^{12}\Gauss$`  |
| `\Kelvin`   | `\, K`              | `$T = 10^6\Kelvin$`    |
| `\keV`      | `\, keV`            | `$E = 1\keV$`          |
| `\Msun`     | `\, M_sun`          | `$M = 1.4\Msun$`       |

### Vector & Math Commands

Definitions:

```latex
\renewcommand{\vec}[1]{\bm{#1}}                % bold italic vector
\newcommand{\nvec}[1]{\hat{\bm{#1}}}            % unit vector

\makeatletter
\def\fvec#1{\underline{\sbox\tw@{$#1$}\dp\tw@\z@\box\tw@}}  % four-vector
\makeatother

\newcommand{\ud}{\mathrm{d}}                     % upright differential d
\newcommand{\Ten}[2]{\ensuremath{#1 \times 10^{#2}} }  % scientific notation
\newcommand{\lamC}{\ensuremath{\lambdabar_\mathrm{C}}}  % reduced Compton wavelength
\newcommand{\lamChat}{\ensuremath{\hat{\lambdabar}_\mathrm{C}}}
```

Quick reference:

| Command            | Output / Purpose                      |
|--------------------|---------------------------------------|
| `\vec{x}`          | `\bm{x}` (bold italic vector)        |
| `\nvec{x}`         | `\hat{\bm{x}}` (unit vector)         |
| `\fvec{x}`         | Underlined four-vector                |
| `\ud`              | Upright differential d (`\mathrm{d}`) |
| `\Ten{3.7}{-8}`    | `3.7 \times 10^{-8}`                 |
| `\lamC`            | Reduced Compton wavelength            |

### Bold Symbol Shortcuts

```latex
\def\bfnabla{\bm{\nabla}}
```

### Color Commands (for draft annotations)

```latex
\newcommand{\red}[1]{\textcolor{magenta}{#1}}
\newcommand{\sred}[1]{\textcolor{red}{\sout{#1}}}
\newcommand{\green}[1]{\textcolor{green}{#1}}
\newcommand{\blue}[1]{\textcolor{blue}{#1}}
\newcommand{\cyan}[1]{\textcolor{cyan}{#1}}
\definecolor{turq}{rgb}{.1,.3,.5}
\definecolor{cela}{rgb}{.0,.6,.5}
\newcommand{\turq}[1]{\textcolor{turq}{#1}}
\newcommand{\cela}[1]{\textcolor{cela}{#1}}
```

| Command      | Color                      |
|--------------|----------------------------|
| `\red{}`     | Magenta text               |
| `\sred{}`    | Red strikethrough           |
| `\green{}`   | Green text                 |
| `\blue{}`    | Blue text                  |
| `\cyan{}`    | Cyan text                  |
| `\turq{}`    | Custom turquoise (0.1, 0.3, 0.5) |
| `\cela{}`    | Custom celadon (0.0, 0.6, 0.5)   |


## Cross-References

### Label Prefixes

| Type       | Prefix        | Example                      |
|------------|---------------|------------------------------|
| Section    | `sect:`       | `\label{sect:discharge}`     |
| Equation   | `eq:`         | `\label{eq:ngj}`             |
| Figure     | `fig:`        | `\label{fig:circuit}`        |
| Appendix   | `app:`        | `\label{app:corot}`          |
| Footnote   | `footnote:`   | `\label{footnote:cartesian}` |

### Reference Formatting

- Equations: `Eq.~\eqref{eq:name}` (uses `\eqref` for auto-parentheses)
- Figures: `Fig.~\ref{fig:name}`
- Sections: `Sect.~\ref{sect:name}`
- Appendices: `Appendix~\ref{app:name}` or `App.~\ref{app:name}`
- Footnotes: `Footnote~\ref{footnote:name}`
- Always use `~` (non-breaking space) between label word and `\ref`/`\eqref`


## Citations

Natbib author-year style:

- **`\citet{}`** when authors are grammatical subject: `\citet{goldreich1969} showed...`
- **`\citep{}`** for parenthetical: `...as shown previously~\citep{smith2001}`
- **`\citealt{}`** for no parentheses (inside existing parens): `(\citealt{nattila2022}; ...)`
- Use `~` before `\citep{}` to prevent line break
- Never write `(Smith, 2001) shows...` -- use `\citet{}` instead


## Text Formatting

### One Sentence Per Line

Each sentence starts on a new line in the source. This makes diffs cleaner and easier to review:

```latex
The gap remains unscreened until pair creation begins.
High-energy curvature photons travel for a duration of $t_\pm$.
```

### Inline Phase/Item Labels

Use `\textbf{Label.}` (bold with trailing period) for inline labels:

```latex
\textbf{Loading.}
During this phase, ...

\textbf{Ignition.}
The cascade begins when ...
```

### Software Names

Use `\textsc{}` for software/code names: `\textsc{Runko}`, `\textsc{v4}~\textsc{kiwi}`.

### Punctuation

- Em-dashes: `---` (no spaces around them)
- Non-breaking space before references: `~`
- Equations follow standard punctuation (commas, periods after displayed equations)


## Equations

- Display equations use `equation` or `align` environments with `\label{eq:...}`
- Do not use multiple equations on one display line, e.g., separated by `\quad`/`\qquad` (e.g. `A=B,\qquad C=D`). Use `align` with each equation on its own line. 
- Punctuate displayed equations as part of the sentence (commas, periods)
- Do not leave blank lines after `\end{equation}` (creates unwanted paragraph break)
- Use `\left(`/`\right)` for auto-sizing; consider `\big(`/`\Big(` in final pass
- Use `\,` for thin spaces in integrals: `\int f \, \ud x`


## Figures

- `\label{}` must come after `\caption{}` (or inside it)
- Footnotes go after `.` and `,`
- Check for broken references (`??` in output)


## Comment Annotations

Use these prefixed comments for tracking issues in the source:

```latex
%DONE: <resolved question>
%FIX: <explanation of the fix applied>
%TODO: <unresolved task>
%NOTE: <informational remark>
```

`%DONE:`/`%FIX:` appear as pairs: the question and its resolution. They are working scaffolding — sweep the resolved pair out at the next tending pass, and always before a finalized or submitted version.
