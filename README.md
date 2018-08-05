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

## Usage:

```
usage: parse.py [-h] [-o OUTPUT_DIR] [-b SEPARATOR] [-s HEADER_SIZE]

optional arguments:
  -h, --help      show this help message and exit
  -o OUTPUT_DIR   output directory (default: "docs")
  -b SEPARATOR    block separator (default: "***")
  -s HEADER_SIZE  header size (default: 3)
```

## Circle CI + GitHub Wiki

As an example of how to use this script in an automated fashion, I've provided a [Docker image](https://hub.docker.com/r/p3lim/lua-doc-parser/) for use with [Circle CI](https://circleci.com/). When set up, any pushes to the `master` branch on GitHub will trigger Circle CI to run the script and upload the docs to the repo Wiki pages on GitHub.

1. Create a SSH key pair by following the [GitHub instructions](https://help.github.com/articles/generating-ssh-keys/)
	- Note: Do not enter a passphrase!
2. Add the **public** key to the repo as a deploy key (`https://github.com/you/repo-name/settings/keys`)
	- Note: Make sure to enable the checkbox "Allow write access"!
3. Add the **private** key to the repo on Circle CI (`https://circleci.com/gh/you/repo-name/edit#ssh`)
	- Note: Enter `github.com` in the "Hostname" field.
4. Add the following Circle CI configuration to the repo (`.circleci/config.yml`)

```yaml
version: 2
jobs:
  build:
    docker:
      - image: p3lim/lua-doc-parser:latest
    steps:
      - checkout
      - run: build.sh
workflows:
  version: 2
  build:
    jobs:
      - build
```
