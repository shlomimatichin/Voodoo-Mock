There are 3 possible expactation types:
1. Construction - this is used to describe the expectation that at this
                  point in the scenario, you expect a certain mock object to
                  be constructed.
2. Destruction - Same for destruction of the mocked object.
3. Calls - when you expect a call to a global function, class static
           method, or method.

Construction:
-------------

usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Construction< ClassName >( "Instance Name" );

example:
    using namespace VoodooCommon::Expect;
    scenario <<
        new Construction< File >( "The Log File" );

This will add an expectation of construction of ClassName. The object
will be named "Instance Name" for future reference (see the parameters
chapter).

The instance name can be fetched using a new method added to any mocked
class: voodooInstanceName().

ConstructionThrowsValue:
------------------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
	new VoodooCommon::Expect::ConstructionThrows< ClassName, Exception >( exceptionObject );

example:
	using namespace VoodooCommon::Except;
	scenario <<
		new ConstructionThrows< File, FileNotFound >( FileNotFound( "C:\\file.txt" ) );

This will add an expectation of construction of ClassName. However,
the construction will throw an exception, and an instance will not
actually be created.

Destruction:
------------

usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Destruction( "Instance Name" );

example:
    using namespace VoodooCommon::Expect;
    scenario <<
        new Destruction( "The Log File" );

This will add an expectation of destruction of the object named "Instance
Name".

Calls:
------
There are several classes to describe a call to a function or method, their
differnces is on how to return the return value. In all the classes below,
"Function Name" can be one of:
1. "Instance Name::Method Name" for methods of mock objects
2. "Namespace1::Namespace2::Function Name" for global functions
3. "Namespace::Class Name::Static Method Name" for static methods

Understand this: Voodoo-Mock does not distinguish between a type and a 
reference to it, in return values. E.g., `int len();' and `int & len();'
both considered `int' in the following templates argument.

Warning: Voodoo-Mock does however distinguish between a const and non
const return value. Remember to provide the correct modifier, or and
error will accour.

CallReturnVoid:
---------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::CallReturnVoid( "Function Name" );

example:
    using namespace VoodooCommon::Expect;
    scenario << CallReturnVoid( "the stream::flush" );

CallReturnValue:
----------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::CallReturnValue< typename >(
                                        "Function Name" , value );

example:
    using namespace VoodooCommon::Expect;
    scenario << CallReturnValue< int >( "Clients Name::len" , 3 );

CallReturnValue copies the value on construction. For all simple types
this is the best option.

If the call just returns typename, note that it will be copied twice:
once into CallReturnValue, and once on the return from the call itself.

If the call returns typename reference (i.e., int & offset();) the
reference returned will be to the value member of CallReturnValue,
a copy of the original value.

The value copy is destructed when the scenario objects destructs.

CallReturnReference:
--------------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::CallReturnReference< typename >(
                                         "Function Name" , object );

example:
    using namespace VoodooCommon::Expect;
    int fakeOffset;
    fakeOffset = 4;
    scenario << CallReturnReference< int >( "Buffer::offset" , fakeOffset );

CallReturnReference only keeps a reference of the object passed on
construction.

If the call returns typename, note that it will be copied when the
returning from the call itself. If the function returns typename
reference, the object is never copied. This is suitable for
getter methods that return references to non copyable objects.

CallReturnReference has nothing to do with the destruction of the object
passed to it.

CallReturnAuto:
---------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::CallReturnAuto< typename >(
                                         "Function Name" , object pointer );

example:
    using namespace VoodooCommon::Expect;
    int * fakeOffset = new int;
    * fakeOffset = 4;
    scenario <<
        new CallReturnAuto< int >( "Buffer::offset" , fakeOffset ) <<
        new CallReturnReference< int >( "Buffer2::offset" , * fakeOffset );

Call return Auto is similar to CallReturnValue, except for the first copy.
The pointer is kept, and the delete operator is called when scenario is
destructed. It is used for auto deleting the original pointer, when copies
of the object is out of the question.

CallThrowValue:
---------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::CallThrowValue< exceptionTypename >(
                                        "Function Name" , exceptionObject );

example:
    using namespace VoodooCommon::Expect;
    scenario <<
        new CallThrowValue< std::runtime_error >( "FakeFile::read" ,
                                    std::runtime_error( "An error" ) );

This call expectation will throw a copy of the exception given to
it at the constructor, instead of returning (only after all the
parameter expectations executed).
