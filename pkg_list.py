## pkg_list by n1ghty
REL_VERSION = 'v1.1.1'

import sys, os, struct, traceback, xlsxwriter, argparse
from lib import pkg_parser, xlsxlist

print 'pkg_tools / pkg_list ' + REL_VERSION + ' by n1ghty'

## parse arguments
from argparse import RawTextHelpFormatter
parser = argparse.ArgumentParser(
	description = 'This tool parses all pkg files in the specified directory/directories recursively\n'
											'and generates an excel sheet from the parsed infos.\n'
											'\n'
											'Available values for the columns:\n'
											' - Values from param.sfo like\n'
											'   TITLE, TITLE_ID, CONTENT_ID, VERSION, APP_VER, PARENTAL_LEVEL, \n'
											'   SYSTEM_VER, ...\n'
											' - LANGUAGES\n'
											'   The list of title name languages, e.g. \'EN,FR,RU\'\n'
											'   This does not always reflect supported languages.'
											' - VER\n'
											'   Equals VERSION for a game / an application and APP_VER(U) for an update\n'
											' - REGION\n'
											'   The region of the pkg (CN, EU, US)\n'
											' - SIZE\n'
											'   The filesize in a readable format, e.g. \'1.1 GB\'\n'
											' - SYS_VER\n'
											'   The required system version number in a readable format, e.g. \'2.70\'\n'
											' - SDK_VER\n'
											'   The used sdk version number in a readable format, e.g. \'2.70\'\n'
											' - TITLE_XX\n'
											'   The title name in a specific language XX. If not available, the default\n'
											'   language is used.\n'
											'\n'
											'   Available language codes:\n'
											'     JA, EN, FR, ES, DE, IT, NL, PT, RU, KO, CH, ZH, FI, SV, DA,\n'
											'     NO, PL, BR, GB, TR, LA, AR, CA, CS, HU, EL, RO, TH, VI, IN',
	formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pkg_path', type=unicode, nargs='+', help='the path(s) to scan for pkg files')
parser.add_argument('-r', dest='recursive', action='store_true', help='include subdirectories')
parser.add_argument('-c', dest='column', nargs='+', help='specify the columns')
parser.add_argument('-s', dest='sort', help='sort list by specific column')
parser.add_argument('-d', dest='descending', action='store_true', help='use descending sorting')
parser.add_argument('-o', dest='outfile', type=unicode, help='specify the output file name (without suffix)')

parser.set_defaults(column=['TITLE', 'TITLE_ID', 'REGION', 'VER', 'CONTENT_ID', 'SIZE'], outfile='pkg_list')

args = parser.parse_args()

# arg cleanup
if (args.sort):
	args.sort = args.sort.upper()
args.column = map(str.upper, args.column)

pkg_paths = []
for path in args.pkg_path:
	if not os.path.isdir(path):
		print 'ERROR: invalid path specified'
		sys.exit()
	pkg_paths.append(os.path.abspath(path))

if len(args.column) != len(set(args.column)):
	print 'ERROR: duplicate values in column list'
	sys.exit()

## utility functions
def getReadableString(s):
	try:
		s_u = s.decode('utf-8')
	except:
		s_u = s
	return s_u

## main code
# parse files
pkgInfos = {'app' : [], 'upd' : [], 'ps2' : [], 'err' : [], 'count' : 0}
for pkg_path in pkg_paths:
	for root, directories, files in os.walk(pkg_path):
		for file in files: 
			if file.lower().endswith('.pkg'):
				try:
					pkgInfos['count'] += 1
					pkgInfo = pkg_parser.getPkgInfo(os.path.join(root, file))
					# set worksheet
					if (pkgInfo['CATEGORY'] == 'gp'):
						# update
						pkgInfos['upd'].append(pkgInfo)
					elif (pkgInfo['CATEGORY'] == 'gpo'):
						# PS2
						pkgInfos['ps2'].append(pkgInfo)
					else:
						# Application / Game 'gd' and unknown
						pkgInfos['app'].append(pkgInfo)
				except:
					# failed to parse pkg
					pkgInfos['err'].append(file)
		if not (args.recursive):
			break

print
print 'Found {} files:'.format(pkgInfos['count'])
print '{} Applications'.format(len(pkgInfos['app']))
print '{} Updates'.format(len(pkgInfos['upd']))
print '{} PS2 Games'.format(len(pkgInfos['ps2']))
print '{} PKG files failed to parse'.format(len(pkgInfos['err']))
print

# sort lists
if args.sort and (args.sort in args.column):
	for id in ('app', 'upd', 'ps2'):
		# add value to every info to make it sortable
		for info in pkgInfos[id]:
			if not (args.sort in info):
				info[args.sort] = ''
		pkgInfos[id] = sorted(pkgInfos[id], key=lambda k: k[args.sort], reverse=args.descending)

# sort errorlist
pkgInfos['err'] = sorted(pkgInfos['err'])

# generate xlsx list
xlsxlist.writeFile(pkgInfos, args.column, args.outfile)
