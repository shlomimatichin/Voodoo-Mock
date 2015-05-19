#ifndef __CXXTEST_PRINT_STACK_H__
#define __CXXTEST_PRINT_STACK_H__

#if !defined(_WIN32) && defined( __GNUG__ )

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

namespace CxxTest
{

class _StackFormatter
{
public:
    _StackFormatter( std::string filename )
    {
        std::string contents = readFile( filename );
        std::string selfRemoved = removeUntilFirst( removeUntilFirst( contents, "CxxTest::printTrace" ), "\n" );
        iterateLines( selfRemoved );
    }

    const std::string output() const { return _output; }

private:
    std::string _output;

    void iterateLines( std::string contents )
    {
        size_t firstChar = 0;
        while ( true ) {
            size_t lineEnd = contents.find( "\n", firstChar );
            size_t lineLength = ( lineEnd == std::string::npos ) ? std::string::npos : lineEnd - firstChar;
            processLine( contents.substr( firstChar, lineLength ) );
            if ( lineEnd == std::string::npos )
                return;
            firstChar = lineEnd + 1;
        }
    }

    void processLine( const std::string & line )
    {
        static const std::string AT( " at " );
        size_t found = line.rfind( AT );
        if ( found == std::string::npos )
            return;
        std::string outputLine = line.substr( found + AT.size() ) + ": " + line.substr( 0, found ) + "\n";
        _output += outputLine;
    }

    static std::string readFile( std::string filename )
    {
        FILE * f = fopen(filename.c_str(), "r");
        if (f == NULL) {
            fprintf( stderr, "Output stack trace was not created, Unable to print stack trace\n" );
            return "";
        }
        char data[ 4096 ];
        std::string output;
        while ( true ) {
            size_t read = fread( data, 1, sizeof( data ), f );
            if ( read == 0 )
                break;
            output += std::string( data, read );
        }
        return output;
    }

    static std::string removeUntilFirst( const std::string & contents, const std::string toFind )
    {
        size_t found = contents.find( toFind );
        if ( found == std::string::npos )
            return contents;
        else
            return contents.substr( found + toFind.size() );
    }
};

static inline void printTrace()
{
    char pid_buf[30];
    sprintf(pid_buf, "%d", getpid());
    char name_buf[512];
    name_buf[readlink("/proc/self/exe", name_buf, 511)]=0;
    char output_name[128];
    strcpy(output_name, "/tmp/stacktrace.XXXXXX");
    int result = mkstemp(output_name);
    if (result < 0) {
        printf( "Unable to show stack trace, mkstemp failed %d\n", result );
        return;
    }
    int child_pid = fork();
    if (!child_pid) {           
        dup2(result, 1);
        dup2(result, 2);
        execlp("gdb", "gdb", "--batch", "-n", "-ex", "thread", "-ex", "bt", name_buf, pid_buf, NULL);
        abort(); /* If gdb failed to start */
    } else {
        prctl(PR_SET_PTRACER, child_pid, 0, 0, 0);
        waitpid(child_pid,NULL,0);
        _StackFormatter formatter(output_name);
        printf( "Stack trace:\n%s\n", formatter.output().c_str() );
    }
    close(result);
    unlink( output_name );
}

} // namespace CxxTest

#else // __GNUG__

namespace CxxTest {

static inline void printTrace() {}

} // namespace CxxTest

#endif // __GNUG__

#endif // __CXXTEST_PRINT_STACK_H__
