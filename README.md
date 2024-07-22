# lua-doc-parser

This is a Python script that will generate Markdown documentation from Lua source code.  
It parses any Lua files in the current directory for any [multi-line comment](https://www.lua.org/pil/1.3.html) blocks and sequentially adds them to a markdown file based on the "header" of the comment block.

Example:
```lua
--[[ Header:method
Hello world!
--]]
```

This will create the following markup in a file named `Header.md`:
```markdown
### Header:method

Hello world!
```

`Header` and `method` can be anything you want, but has to be separated by a colon (`:`) or a period (`.`).  
The "magic" method name "header" can be used to force a block to appear on the top of the document as a header for the file, e.g:

```lua
--[[ MyObject:foo(_bar_)
This is a method `foo`, which takes argument `bar`.
--]]
--[[ MyObject:header
This will be at the **top** of the [MyObject](MyObject) document!  
Methods:
- [foo(_bar_)](MyObject#myobjectfoobar)
--]]
```

As you can see, any markdown notation is allowed inside the block.

Indentation is limited to _tabs_ for the blocks, and any indendation inside the blocks is limited to _spaces_.
This is to allow code snippets in documentation in-line in functions to parse correctly.

## Usage

```
usage: parse.py [-h] [-o OUTPUT_DIR] [-b SEPARATOR] [-s HEADER_SIZE]

optional arguments:
  -h, --help      show this help message and exit
  -o OUTPUT_DIR   output directory (default: "docs")
  -b SEPARATOR    block separator (default: "***")
  -s HEADER_SIZE  header size (default: 3)
```

## GitHub Action

This is an example workflow that will do the following:
- checkout the project and its wiki
- use this script as an action, outputting to the wiki directory
- commit and push the changes of the wiki directory

```yaml
name: Generate documentation
on: push

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - name: Clone project
        uses: actions/checkout@v4

      - name: Clone wiki
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository }}.wiki
          path: .wiki

      - name: Parse and generate documentation
        uses: p3lim/lua-doc-parser@v2
        with:
          output: .wiki

      - name: Push wiki changes
        working-directory: .wiki
        run: |
          git config user.name CI
          git config user.email "<>"
          git add .
          git diff --quiet HEAD || git commit -m "$GITHUB_SHA"
          git push
```
