import re
import os.path

class Preprocessor:
	def __init__( self , inPath , outPath , inputLines , pathToRemoveFromIdentifer ):
		self._inPath = inPath
		self._setFilenameIdentifier( pathToRemoveFromIdentifer )
		self._setPathToOriginal( outPath )
		self._readAllIncludes( inputLines )

	def _setFilenameIdentifier( self , pathToRemoveFromIdentifer ):
		assert self._inPath.startswith( pathToRemoveFromIdentifer )
		lengthToIgnore = len( pathToRemoveFromIdentifer )
		self._filenameIdentifier = ''
		for char in self._inPath:
			if lengthToIgnore > 0:
				lengthToIgnore -= 1
				continue
			if char.isalnum():
				self._filenameIdentifier += char
			else:
				if len( self._filenameIdentifier ) > 0 and \
						self._filenameIdentifier[ -1 ] != "_":
					self._filenameIdentifier += "_"

	def _setPathToOriginal( self , outPath ):
		absPath = os.path.abspath( self._inPath ).split( os.path.sep )
		absOutPath = os.path.abspath( os.path.dirname( outPath ) ).split( os.path.sep )
		while (	len( absPath ) > 0 and len( absOutPath ) > 0 and
				absPath[ 0 ] == absOutPath[ 0 ] ):
			absPath.pop( 0 )
			absOutPath.pop( 0 )
		if len( absPath[ 0 ] ) == 2 and absPath[ 0 ][ 1 ] == ":":
			absOutPath = []
		self._pathToOriginal = '/'.join( [ ".." ] * len( absOutPath ) + absPath )

	def _readAllIncludes( self , inputLines ):
		inputLines = self._joinBackslashSplitLines( inputLines )
		self._includes = [ l for l in inputLines if self._includeLine( l ) ]
		self._macros = [ l for l in inputLines if self._macroLine( l ) ]

	def _joinBackslashSplitLines( self , inputLines ):
		inputLines = inputLines[ : ]
		i = 0
		while i < len( inputLines ):
			if inputLines[ i ].endswith( "\\\n" ):
				assert i < len( inputLines ) - 1
				inputLines[ i ] = inputLines[ i ] + inputLines.pop( i + 1 )
				continue
			i += 1
		return inputLines

	def _macroLine( self , line ):
		return re.match( "^\s*#" , line ) is not None

	def _includeLine( self , line ):
		return	re.match( "^\s*#\s*include" , line ) is not None or \
				re.match( "^\s*#\s*if" , line ) is not None or \
				re.match( "^\s*#\s*endif" , line ) is not None or \
				re.match( "^\s*#\s*else" , line ) is not None

	def __eq__( self , other ):
		return	self._inPath == other._inPath and \
				self._includes == other._includes

	def multiIncludePreventerHeader( self ):
		return	(	'#ifndef __VOODOO_MULTIINCLUDE_PREVENTER_%s__\n' +
					'#define __VOODOO_MULTIINCLUDE_PREVENTER_%s__\n\n' ) % (
							self._filenameIdentifier ,
							self._filenameIdentifier )

	def multiIncludePreventerFooter( self ):
		return '\n#endif // __VOODOO_MULTIINCLUDE_PREVENTER_%s__\n' % (
								self._filenameIdentifier )

	def headerOfHeader( self ):
		return	( '#include "%s"\n' ) % (	self._pathToOriginal )

	def header( self ):
		return	(	'%s' +
					'\n' +
					'#ifndef VOODOO_EXPECT_%s\n' +
					'#ifndef VOODOO_%s\n' +
					'#include "%s"\n' +
					'#else // VOODOO_%s\n' +
					'\n' +
					'%s' +
					'\n' +
					'%s' +
					'\n') % (	
								"".join( self._includes ) ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._pathToOriginal ,
								self._filenameIdentifier ,
								self.multiIncludePreventerHeader() ,
								"".join( self._macros ) )

	def switchToExpectation( self ):
		return (	'\n' +
					'%s\n' +
					'#endif // VOODOO_%s\n' +
					'#else // VOODOO_EXPECT_%s\n' +
					'\n' +
					'#ifdef VOODOO_%s\n' +
					'#error You must not define both VOODOO_%s ' +
								'and VOODOO_EXPECT_%s\n' +
					'#endif // VOODOO_%s\n' +
					'\n' +
					'%s' +
					'\n' +
					'%s' +
					'\n' ) % (
								self.multiIncludePreventerFooter() ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self.multiIncludePreventerHeader() ,
								"".join( self._macros ) )

	def footer( self ):
		return '\n%s\n#endif // VOODOO_EXPECT_%s' % (
								self.multiIncludePreventerFooter() ,
								self._filenameIdentifier )

	def externalHeader( self ):
		return ( 	'#include "%s"\n' +
					'\n' +
					'%s' +
					'#ifndef VOODOO_EXPECT_%s\n' +
					'\n' ) % (	self._pathToOriginal ,
								self.multiIncludePreventerHeader() ,
								self._filenameIdentifier )

	def externalSwitchToExpectation( self ):
		return (	'\n' +
					'#else // VOODOO_EXPECT_%s\n' +
					'\n' ) % (	self._filenameIdentifier )

	def externalFooter( self ):
		return (	'\n' +
					'#endif // VOODOO_EXPECT_%s\n' +
					'%s' ) % (	self._filenameIdentifier ,
								self.multiIncludePreventerFooter() )

	def intercepter( self ):
		return	(	'%s' +
					'\n' +
					'#ifdef VOODOO_%s\n' +
					'#error %s is only intercepted, cannot be voodooed ' +
						'(probably a parse error)\n' +
					'#endif // VOODOO_%s\n' +
					'\n' +
					'#ifdef VOODOO_EXPECT_%s\n' +
					'#error %s is only intercepted, cannot be voodooed ' +
						'(probably a parse error)\n' +
					'#endif // VOODOO_EXPECT_%s\n' +
					'\n' +
					'%s' +
					'\n' +
					'#include "%s"\n' ) % (
								"".join( self._includes ) ,
								self._filenameIdentifier ,
								self._inPath ,
								self._filenameIdentifier ,
								self._filenameIdentifier ,
								self._inPath ,
								self._filenameIdentifier ,
								"".join( self._includes ) ,
								self._pathToOriginal )
