# English edition correction

The English text in the first release was an abridged adaptation. Its earlier description as a complete English edition was incorrect. A full translation preserving the Chinese revision's content and sequence is in progress.

# Edition notes

This repository publishes the complete Chinese revision and the English adaptation of *Viscosity: Intelligence Across Bits, Atoms, and Life*, dated 28 October 2026.

## Text and structure

The Chinese revision develops the existing manuscript. The English edition follows its argument in idiomatic English, with examples and explanatory transitions suited to English-speaking readers. Each contains a preface, seven chapters, and an appendix. The 44 numbered source units correspond across languages; English length and paragraph boundaries vary with the adaptation.

The revision tightens repeated explanations, separates physical relations from engineering analogies, corrects mathematical conditions, and gives institutional arguments their own explicit grounds. It distinguishes a lower total cost from a shifted burden, capability from authority, a demonstrated task from a deployed service, and a project milestone from an established outcome.

Ten new bilingual mechanism diagrams develop the argument through reaction barriers, response curves, model–action feedback, hover endurance, Hessian directions, transition losses, accountability, Pareto tradeoffs, delay stability, and critical paths. Existing Chinese diagrams are retained or revised where useful.

## Sources and checks

Contemporary cases were checked online against primary sources through 28 October 2026. The bibliography records the sources used in the text. Announcements retain their announced or planned status; statistical reports retain their data year. Theoretical illustrations are identified as models or schematics.

Both PDF editions were compiled with XeLaTeX and biber. Checks cover missing citations, cross-references, undefined commands, missing glyph warnings, and overflowing text boxes. All pages were rendered for layout review. The Markdown readers retain equations, tables, figures, and linked reference notes.

These checks establish the state of this revision. The book continues to welcome substantive corrections through issues.

## Files

| Path | Contents |
| --- | --- |
| en/viscosity-en.pdf | Complete English PDF |
| zh/viscosity-zh.pdf | Complete Chinese PDF |
| en/CONTENTS.md, zh/CONTENTS.md | Chapter readers |
| en/book.tex, zh/book.tex | Complete LaTeX sources |
| en/sections, zh/sections | 44 aligned units per language |
| shared/refs.bib | Shared bibliography |
| en/assets, zh/assets, zh/figures | Reader images and embedded vector figures |
| shared/figures | Bilingual analytical figures |
| editorial/alignment.json | Source and adaptation checksums |

## Rebuilding the PDFs

Use XeLaTeX, biber, and the fonts named in the source. The supplied Chinese source uses Windows CJK fonts; another system can substitute an installed CJK family in the font declarations. Compile book.tex, run biber on book, then compile twice more. Work from the language directory so the relative figure paths resolve.

The PDFs and Markdown readers are ready to read without a typesetting environment.
