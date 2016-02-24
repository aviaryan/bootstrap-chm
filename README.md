# bootstrap-chm
Bootstrap documentation in chm, complete with **Index** and **TOC**. Current version is 3.3.5.


### Download

See [project releases](https://github.com/aviaryan/bootstrap-chm/releases)


### Preview

![Contents](http://i.imgur.com/VcaYF4U.png)

![Index](http://i.imgur.com/OgykiQi.png)


### Building the docs

1. Get Jekyll and compile the [official Bootstrap docs](https://github.com/twbs/bootstrap).
2. Copy the compiled site into `src` directory. 
3. `python bootstrap-chm.py`
4. Compile the files in `build` directory using a HtmlHelp compiler. I am using [Precision Helper](http://www.be-precision.com/products/precision-helper/).


### FAQ

> I see nothing/blank when I open the CHM file ? (Windows)

Open bootstrap.chm properties and unblock it.