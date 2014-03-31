import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "--generated", required = True )
parser.add_argument( "--toStdout", action = "store_true" )
parser.add_argument( "--testName", required = True )
args = parser.parse_args()

contents = open( args.generated ).read()
split = contents.split( "\n\n" )
keep = [ s for s in split if 'CxxTest::RealTestDescription' not in s or '"' + args.testName + '"' in s ]
result = "\n\n".join( keep )

if args.toStdout:
    print result
else:
    with open( args.generated, "w" ) as f:
        f.write( result )
