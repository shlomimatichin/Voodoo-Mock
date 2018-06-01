#!/bin/bash
SUITE=$1

function isPython {
    echo $SUITE | grep '\.py$' > /dev/null
}
function isCxxTest {
    echo $SUITE | grep 'Test_.*\.[hH].\?.\?$' > /dev/null
}

if isPython $SUITE; then
	python $VOODOO_ROOT_DIR/pytest/pytestrunner.py --verbose $SUITE
else
    if [ ! isCxxTest ]; then
        echo "$SUITE was not recognized as niether python test suite or CxxTest suite files"
        exit 1
    fi
    NO_EXT=`echo $SUITE | sed 's@\.[hH].\?.\?$@@'`
    NO_EXT_UNDERSCORE=`echo $NO_EXT | sed 's@/@_@g'`
    BIN=build_unittest/${NO_EXT_UNDERSCORE}.bin
    $BIN
fi
