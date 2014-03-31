import __builtin__;
import imp;
import sys;

__all__ = [ "installUntee" ];

oldImport = __builtin__.__import__;

def importOverride( name, globals=None, locals=None, fromlist=None ):
    if name == "T":
        return importFromTee( name, fromlist );

    if name.startswith( "T." ):
        return importFromSubtee( name , globals , locals , fromlist );

    return oldImport( name, globals, locals, fromlist );

def importFromTee( name, fromlist ):
    if name not in sys.modules.keys():
        sys.modules[ name ] = imp.new_module( name );
    module = sys.modules[ name ];
    for each in fromlist:
        setattr( module, each, oldImport( each ) );
    return module;

def importFromSubtee( name , globals , locals , fromlist ):
    return oldImport( name[2:] , globals , locals , fromlist );

def installUntee():
    __builtin__.__import__ = importOverride;
