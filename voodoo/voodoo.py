from preprocessor import Preprocessor
from voodoomultiplexeriterator import VoodooMultiplexerIterator
from perfilesettings import PerFileSettings
import re

def _readLinesOfFile( fileName ):
	f = file( fileName )
	try:
		return f.readlines()
	finally:
		f.close()

def voodoo( input, output, pathToRemoveFromIdentifier, voodooDBFile, includes, defines, preIncludes, trace = False ):
	inputLines = _readLinesOfFile( input )
	perFileSettings = PerFileSettings( inputLines )
	preprocessor = Preprocessor( input, output, inputLines, pathToRemoveFromIdentifier )

	out = preprocessor.header()
	out += '#include <VoodooCommon/Common.h>\n\n'
	iterator = VoodooMultiplexerIterator( perFileSettings, voodooDBFile )
	iterator.process( input, includes = includes, defines = defines, preIncludes = preIncludes )
	out += iterator.iter()
	out += preprocessor.switchToExpectation()
	out += '#include "VoodooCommon/All.h"\n\n'
	out += iterator.expect()
	out += preprocessor.footer()
	return out

def externalVoodoo( input, output, linkTo, pathToRemoveFromIdentifier = "", trace = False ):
	inputLines = _readLinesOfFile( input )
	perFileSettings = PerFileSettings( inputLines )
	preprocessor = Preprocessor( linkTo, output, inputLines, pathToRemoveFromIdentifier )

	out = preprocessor.externalHeader()
	out += '#include "VoodooConfiguration.h"\n'
	out += '#include <VoodooCommon/Common.h>\n\n'
	out += "namespace External\n{\n\n"
	iterator = VoodooMultiplexerIterator( perFileSettings )
	iterator.process( input )
	out += iterator.iter()
	out += "\n}\n\n"
	out += preprocessor.externalSwitchToExpectation()
	out += '#include "VoodooCommon/All.h"\n\n'
	out += "namespace External\n{\n\n"
	out += iterator.expect()
	out += "\n}\n\n"
	out += preprocessor.externalFooter()
	return out


def voodooExpectSource( input, output, pathToRemoveFromIdentifier, voodooDBFile, includes, defines, preIncludes, trace = False ):
	inputLines = _readLinesOfFile( input )
	perFileSettings = PerFileSettings( inputLines )
	preprocessor = Preprocessor( input, output, inputLines, pathToRemoveFromIdentifier )

	iterator = VoodooMultiplexerIterator( perFileSettings, voodooDBFile )
	iterator.process( input, includes = includes, defines = defines, preIncludes = preIncludes )

	out = preprocessor.headerOfHeader() + '\n'
	out += '#include "VoodooCommon/All.h"\n\n'

	out += iterator.expect()
	return out


def voodooExpectHeader( input, output, pathToRemoveFromIdentifier, voodooDBFile, includes, defines, preIncludes, trace = False ):
	inputLines = _readLinesOfFile( input )
	perFileSettings = PerFileSettings( inputLines )
	preprocessor = Preprocessor( input, output, inputLines, pathToRemoveFromIdentifier )

	iterator = VoodooMultiplexerIterator( perFileSettings, voodooDBFile )
	iterator.process( input, includes = includes, defines = defines, preIncludes = preIncludes )

	out = preprocessor.headerOfHeader() + '\n'
        
	return out

