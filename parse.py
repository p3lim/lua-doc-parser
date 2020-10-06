#!/usr/bin/env python3

import os
import re
from argparse import ArgumentParser
from glob import glob

# parse args
parser = ArgumentParser()
parser.add_argument('-o', dest='output_dir', default='docs', help='output directory (default: "docs")')
parser.add_argument('-b', dest='separator', default='***', help='block separator (default: "***")')
parser.add_argument('-s', dest='header_size', default=3, type=int, help='header size (default: 3)')
args = parser.parse_args()

PATH = args.output_dir.strip()
HSIZE = args.header_size
SEPARATOR = '\n{}\n\n'.format(args.separator)

# compile regex patterns beforehand
START = re.compile(r'^\t*--\[(=*)\[ ?((\w+)([:.](.+))?)$')
STOP = re.compile(r'^\t*--\](=*)\]$')

# create a dictionary to store our pages
pages = {}
headers = {}

print('Parsing documentation in \'{}\''.format(os.getcwd()))
for file in glob('**/*.lua', recursive=True):
	# iterates recursively for every Lua file, then open file for reading
	with open(file) as f:
		isReading = False
		textBlock = ''
		isHeader = False
		pageName = None
		numBlocks = 0
		comment = None

		# traverse file line-by-line for content
		for line in f:
			if not isReading:
				# we're not currently reading a text block, search for the start of one
				header = START.match(line)
				if header:
					# found a text block
					# the expected format is:
					# "--[[ PageName:foo..."
					if header.group(5) and header.group(5).lower() == 'header':
						# our "foo" was "header", which signifies this should be text on top of
						# the page, but there's already a dedicated heading for the page
						isHeader = True
					else:
						# everything else gets h3
						textBlock = '{} {}\n\n'.format('#' * HSIZE, header.group(2))

					# store the page name and toggle reading mode
					comment = header.group(1)
					pageName = header.group(3)
					isReading = True
			else:
				# we're reading, check if the line signifies the end of a block
				if STOP.match(line) and header.group(1) == comment:
					# line signified the end of a block, we'll need to store it
					# the expected format is:
					# "--]]"
					if not pageName in pages:
						# page does not have a list to store blocks in - create it
						pages[pageName] = []

					if isHeader:
						# the block was a header
						if pageName in headers:
							# append it to the existing block
							headers[pageName] += '\n\n{}'.format(textBlock)
						else:
							# add it
							headers[pageName] = textBlock
					else:
						# normal block, just append it
						pages[pageName].append(textBlock)

					# reset back to normal
					isReading = False
					isHeader = False
					textBlock = ''
					pageName = None
					numBlocks += 1
					comment = None
					continue
				else:
					# we're currently in the middle of a block, just store the line
					# we also need to strip leading tabs, forcing indented text blocks to use
					# spaces within as whitespace if needed
					textBlock += line.lstrip('\t')

		if numBlocks > 0:
			# at the end of a file, if we found some blocks, log it
			print('- Found {} blocks in \'{}\''.format(numBlocks, file))

for name, block in headers.items():
	# insert headers as the top-most item in pages
	pages[name].insert(0, block)

print(f'path: "{os.getcwd()}" "{PATH}"')

# done parsing docs, let's write it out
print('\nWriting to files')

for name, blocks in pages.items():
	# iterates over 'pages' dict
	# figure out the path we want to save to, and log it
	filepath = f'{name}.md'
	print('- {}'.format(os.path.join(PATH, filepath)))

	with open(os.path.join(os.getcwd(), PATH, filepath), 'w') as f:
		# open the output file for writing, join the blocks for the page, then write
		f.write(SEPARATOR.join(blocks))

print('\nDone!')
