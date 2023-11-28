# MatpLaTeX

MatpLaTeX lets you save a matplotlib `Figure` as a combination of a pdf file containing the graphics and a tex file containing the text. With this, text in the figure will automatically use the typeface, size and other settings of the surrounding text.

## Installation

The matplatex package is on PyPI and can be installed with
```
pip install matplatex
```

### Requirements:
- python >= 3.10 (If someone asks I may add support for earlier versions.)
- matplotlib >= 3.5
- beartype


## Basic Usage

To save a figure, simply use
```
matplatex.save(fig, "myfig")
```
this will create two files named `myfig.pdf` and `myfig.pdf_tex`.
Add
```
\newsavebox\figurebox
``` 
to your LaTeX preamble and include the figure in your document with
```
\def\figurewidth{<width>}}
\input{myfig.pdf_tex}
```
LaTeX commands such as `\small` and `\textbf{}` will affect the text in the expected way.

## More Options

If you don't like the commands `\figurebox` and `\figurewidth`, you can change them to something else by passing the keyword arguments 'boxname' or 'widthcommand' to `matplatex.save`.

## Limitations

- Characters which need to be escaped in LaTeX must also be escaped in the plot.


## Why not …

### … adjust the plot settings in a matplotlib style sheet?
You’d need to recreate every figure each time you make a change.

### … use tikzplotlib?
Tikzplotlib is great for simple figures, but fails to accurately recreate more complex ones, or ones with too much data. MatpLaTeX is meant to cover a different usecase that tikzplotlib rather than compete with it.

### … use pgfplots from the getgo?
I like python.

### … spend time on actual work rather than on tiny details nobody cares about anyway?
_I_ care.

## Motivation
You've probably been there: you made a nice figure and now you want no include it in your LaTeX document. But the text is too small. And the font doesn't match.

You open the matplotlib documentation and adjust all the necessary settings for the figure to look right, perfectly at home in your manuscript.


