# bootstrap-chm
Bootstrap documentation in chm. See [Releases](https://github.com/aviaryan/bootstrap-chm/releases) for download links. Current version is 3.3.5.


### Just a word

For the docs to be presented in CHM format, all JavaScript had to be removed. So the CHM docs may not behave exactly as their online counterpart. 


### Building the docs

1. Get Jekyll and compile the [official Bootstrap docs](https://github.com/twbs/bootstrap).
2. Copy the compiled site into `src` directory. 
3. Run bootstrap-chm.py
4. Compile the files in `build` directory using a HtmlHelp compiler. I am using [Precision Helper](http://www.be-precision.com/products/precision-helper/).
