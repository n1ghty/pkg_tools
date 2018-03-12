## pkg_rename by n1ghty
REL_VERSION = 'v1.1.0'

import sys, os, struct, traceback, re, codecs, argparse
from lib import pkg_parser

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print 'pkg_tools / pkg_rename ' + REL_VERSION + ' by n1ghty'
NAME_FORMAT = u'%TITLE% (%TITLE_ID%) [v%VER%]'

## parse arguments
from argparse import RawTextHelpFormatter
parser = argparse.ArgumentParser(
	description = 'This tool renames PS4 pkg files to the sony format (default), a readable\n'
											'name format or a custom specified format.\n'
											'\n'
											'For the custom formatting, values can be replaced by surrounding them with\n'
											'%-characters.\n'
											'E.g. \'%TITLE% (%TITLE_ID%)\' will result in \'Game name (CUSA01234)\'\n'
											'\n'
											'Available values for formatting:\n'
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
											'     NO, PL, BR, GB, TR, LA, AR, CA, CS, HU, EL, RO, TH, VI, IN \n'
											'\n'
											'The readable name format (-n) uses the following format:\n'
											'\'' + NAME_FORMAT + '\'',
	formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pkg_path', type=unicode, help='the pkg file which shall be renamed (or directory when used with -d)')
parser.add_argument('-t', dest='testrun', action='store_true', help='only test the formatting without renaming')
parser.add_argument('-c', dest='custom_format', type=unicode, help='custom file name format')
parser.add_argument('-n', dest='name_format', action='store_true', help='use a readable name format')
parser.add_argument('-d', dest='dir', action='store_true', help='rename all files in the specified directory')
parser.add_argument('-r', dest='recursive', action='store_true', help='include subdirectories')

args = parser.parse_args()

if (args.dir):
	pkg_path = args.pkg_path
	if os.path.isfile(pkg_path):
		print 'error: invalid directory specified'
		sys.exit()
else:
	if not os.path.isfile(args.pkg_path):
		print 'error: invalid file specified'
		sys.exit()

## utility functions
def getReadableString(s):
	try:
		s_u = s.decode('utf-8')
	except:
		s_u = s
	return s_u

def doDictFormat(s, dict):
	s_f = s
	format_val_arr = []
	format_arr = re.findall('\%(.*?)\%', s)
	for val in format_arr:
		if (val.upper() == 'TITLE'):
			title = getReadableString(dict['TITLE']).replace(': ', ' - ').replace(':','-').replace('/','_').replace('\\','_')
			s_f = s_f.replace('%' + val + '%', '{}')
			format_val_arr.append(title)
		elif val.upper() in dict:
			s_f = s_f.replace('%' + val + '%', '{}')
			format_val_arr.append(dict[val.upper()])
	return s_f.format(*format_val_arr)

## main code
def renamePkg(pkg_file_path):
	try:
		pkgInfo = pkg_parser.getPkgInfo(pkg_file_path)

		if (pkgInfo):
			# add combined version for update / game versions
			if (pkgInfo['CATEGORY'] == 'gp'):
				# update, replace version
				pkgInfo['VER'] = pkgInfo['APP_VER'] + '(U)'
			else:
				pkgInfo['VER'] = pkgInfo['VERSION']

			format_out = ''
			if (args.custom_format):
				# use custom formatting
				format_out = doDictFormat(args.custom_format, pkgInfo)
			elif (args.name_format):
				# format with readable name
				format_out = doDictFormat(NAME_FORMAT, pkgInfo)
			else:
				# use default sony format
				if pkgInfo['CONTENT_ID'] and pkgInfo['APP_VER'] and pkgInfo['VERSION']:
					format_out = '{0}-A{1}-V{2}'.format(pkgInfo['CONTENT_ID'], pkgInfo['APP_VER'].replace('.',''), pkgInfo['VERSION'].replace('.',''))
				else:
					raise pkg_parser.MyError('parsing of param.sfo failed')
			format_out = format_out + '.pkg'

			print 'Renaming \'' + os.path.split(pkg_file_path)[1] + '\' to \'' + format_out + '\''
			if (args.testrun == False):
				pkg_new_file_path = os.path.dirname(os.path.abspath(pkg_file_path)) + '\\' + format_out
				if os.path.exists(pkg_new_file_path):
					raise pkg_parser.MyError('file \''+pkg_new_file_path+'\' already exists!')
				else:
					os.rename(pkg_file_path, pkg_new_file_path)

	except pkg_parser.MyError as e:
		print 'ERROR:', e.message
	except:
		print 'ERROR: unexpected error:  {} ({})'.format(sys.exc_info()[0], pkg_file_path)
		traceback.print_exc(file=sys.stdout)

if (args.dir):
	for root, directories, files in os.walk(pkg_path):
		for file in files: 
			if file.lower().endswith('.pkg'):
				renamePkg(os.path.join(root, file))
		if not (args.recursive):
			break
else:
	renamePkg(args.pkg_path)
