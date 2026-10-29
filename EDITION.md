# Edition notes

**Ming-Zhe Dai**

PhD, Associate Professor, Central South University

*Viscosity: The Evolution of Intelligence in Bits, Atoms, and Life* is published in English and Chinese. The repository presents English first, with Chinese alongside it.

## Text

The English edition is being translated from the Chinese revision. It preserves the source's content and sequence, including every argument, example, equation, table, and figure.

The Chinese revision, dated 28 October 2026, contains a preface, seven chapters, and a theoretical appendix, organized into 44 source units. Its PDF, chapter readers, and LaTeX source are available in zh.

## Research status

Viscosity is the book's meta-concept. Resources, time, and topology provide the analytical framework, applied across bits, atoms, and genes. The framework supports qualitative analysis and classification; formalization and quantitative validation remain open research work.

Readers are invited to contribute measurable definitions, models, case studies, datasets, counterexamples, and empirical tests through GitHub Issues.

## Sources and verification

Contemporary cases in the Chinese revision were checked against primary sources through 28 October 2026. Announcements retain their announced or planned status; statistical reports retain their data year. Theoretical illustrations are identified as models or schematics.

The English and Chinese introductions open with eight corresponding questions, drawn from research and public discussions checked through 29 October 2026. Their linked sources appear in both introductions.

The Chinese PDF was compiled with XeLaTeX and biber, checked for missing citations and references, undefined commands, missing glyphs, and overflowing text, and rendered for layout review. Its chapter readers retain equations, tables, figures, and linked references.

English language and layout checks are in progress. The English edition will be published after translation and verification.

## Files

| Path | Contents |
| --- | --- |
| zh/viscosity-zh.pdf | Chinese PDF |
| zh/CONTENTS.md | Chinese chapter readers |
| zh/book.tex, zh/sections | Chinese source and its 44 units |
| shared/refs.bib | Bibliography |
| en/assets, zh/assets, zh/figures | Illustrations |
| shared/figures | Analytical figure sources |
| editorial/alignment.json | Translation status and source checksums |

## Rebuilding

Use XeLaTeX, biber, and the fonts named in the source. The Chinese source uses Windows CJK fonts; another system can substitute an installed CJK family. Compile book.tex, run biber on book, then compile twice more from the language directory.

The supplied PDF and chapter readers can be read without a typesetting environment.
