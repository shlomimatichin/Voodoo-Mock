If you read the previous chapter, you should recall that there are
thee types of expectations: Construction, Destruction, and Call.
Constructors and function calls can also expect parameters.
There are four types of parameter expectations:
1. Verifier - This expectation type checks that the value actually
              passed in the call is what was expected. Usually
              "IN" parameters will be verified.
2. Storage - This expectation type just stores the value passed to
             the call, without verifing it. These are used when
             the value cannot be verified simply, as with
             callbacks.
3. Assigner - This expectation type loads a value into the passed
              pointer or reference.
4. Programmable - You can implement whatever you want over the
                  received parameter.

For any parameter you can choose any parameter expectation to add
to the scenario, however, the correct number of parameters and
parameter types must be matched. E.g., a method call expectation
that expects two parameters, must have exactly two parameter
expectations attached to it, with the correct types, or an error
will accour.

As with calls return values, the template argument in the following
templates does not distinguish if the parameter is a value, or
reference to a value. Also, remember that you need the const
modifier.

Warning: some of the parameter expectations keep references.

Note: The parameter expectations implemented as needs came up while
working with Voodoo. It is not a "complete" collection, and not all
possible combinations have been implemented. If you find that what
you need is missing, you are encouraged to implement your own,
see the programmable parameter expectation section below. As in
any open project, constribution of code is welcome.

Catergoty 1: Verifiers:
-----------------------

There are several template classes that implement parameter
verification.

Ignore:
-------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
	new VoodooCommon::Expect::Parameter::Ignore< typename >();

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
    scenario <<
        new CallReturnBool( "openFile", false ) <<
			new Ignore< const char * >();

This verifier only checks the type of the parameter, and ignores
it's value. This is mostly used in failure scenarios, to ignore
the input.

Named:
------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::Named< typename >( "Instance Name" );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
    scenario <<
        new CallReturnVoid( "appendTo" ) <<
            new Named< File >( "File Object 1" ) <<
            new EqualsValue< String >( "another line to append\n" ); 

Mocked objects have the property voodooInstanceName(). This
method will return the instance name, provided either when on the
construction expectation (see "Expectation Types" chapter), or when
creating the Fake (see "Fake And FakeND" chapter). This verifier
checks that the object of type `typename' has the
voodooInstanceName() equal to "Instance Name".

NamedOrCopyOf:
--------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::Named< typename >( "Instance Name" );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
    scenario <<
        new CallReturnVoid( "freeSmartPointer" ) <<
            new NamedOrCopyOf< SmartPointer >( "Allocation1" );

This verifier is the same as Named, except it will also accept
fake objects copied from the instance name. Read the "Copy
Construction" chapter for more.

EqualsValue:
------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::EqualsValue< typename >( expectedValue );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
    scenario <<
        new CallReturnValue< double >( "Array::operator []" , 100.0 ) <<
            new EqualsValue< const unsigned >( 10 ); 

This verifier compares the value given to it in the constructor,
to the value passed to the mocked call. The comparison is performed
using operator ==.

EqualsValue copies the object of type `typename' into a private member
on construction. It is mostly suitable for simple types (e.g., `int'),
and copyable and comparable classes.

EqualsReference:
----------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::EqualsReference< typename >( expectedValueReference );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
    Shared< std::string > sharedString;
    scenario <<
        new CallReturnVoid( "Man::setName" ) <<
            new EqualsReference< Shared< std::string > >( sharedString ); 

This verifier compares the value given to it in the constructor,
to the value passed to the mocked call. The comparison is performed
using operator ==.

EqualsReference, unlike EqualsValue, does not copy the object on
construction, but only saves a reference to it. It is mostly suitable
for classes with operator ==, that cannot, or should not be copied.
It can also be used to modify the expectation retroactively.

SameDataValue:
--------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::SameDataValue< typename >( expectedValue );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	void setHeader( struct Header & );
    scenario <<
        new CallReturnVoid( "setHeader" ) <<
			new SameDataValue< struct Header >( Header( 10, 20, 30 ) );

This verifier compares the value given to it in the constructor,
to the value passed to the mocked call. The comparison is performed
using memcmp.

SameDataValue copies the object of type `typename' into a private member
on construction. It is mostly suitable for complex struct types, that have
a copy constructor.

ReferenceTo:
------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::ReferenceTo< typename >( expectedObject );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	void modify( Document & );
    scenario <<
        new CallReturnVoid( "modify" ) <<
			new ReferenceTo< Document >( doc1 );

This verifier compares the object in the mocked call is the same
object (i.e., same instance), as the object referenced in it's
construction.

ReferenceTo only keeps a reference to the object passed to it.
It is mostly suitable for non mocked objects, passed by reference.

Catergoty 2: Storage:
---------------------

There are several template classes that implement parameter
storage. Parameter storage is only recommended in cases where
the value of the parameter cannot be verified, as in passing
callbacks as parameters.

SaveValue:
----------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::SaveValue< typename >( referenceToPointerToTypename );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	Driver( Operations );
	Operations * lastOperations;
    scenario <<
        new Construction< Driver >( "Fake Driver" ) <<
			new SaveValue< Operations >( lastOperations );
	...
	delete lastOperations;

This expectation will allocate and copy construct the pointer given
to it, with the value from the mocked call.

This is the most generic form of storage expectation parameter.
It is mostly suitable for complex objects, that do not have a default
constructor, or that can not be constructed (e.g., pure virtual).
Note that freeing the expectation does not free the pointer - you
must code your own deletion.

SaveSimpleValue:
----------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::SaveValue< typename >( referenceToTypename );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	Timer( shared_ptr< Callback > );
	shared_ptr< Callback > lastCallback;
    scenario <<
        new Construction< Timer >( "Fake Timer" ) <<
			new SaveSimpleValue< shared_ptr< Callback > >( lastCallback );

This expectation will use operator = to copy the value from the
mocked call onto the object passed to it by reference on construction.

This is a bit less generic from of storage, that does not allocate
memory. It requires operator =, and an already built object (which
usually means a default constructor).

SaveReference:
--------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::SaveValue< typename >( referenceToTypename );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	Timer( Callback & );
	Callback * lastCallback;
    scenario <<
        new Construction< Timer >( "Fake Timer" ) <<
			new SaveReference< Callback >( lastCallback );

This expectation will store the address of the object from the
mock call.

This storage expectation is useful only in cases of a parameter
being passed by reference, of a type which is not mocked.

Catergoty 3: Assigners:
-----------------------

There are several template classes that implement parameter
assignment. Parameter assignment is required in cases of out
parameters.

AssignValue:
------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::AssignValue< typename >( value );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	void acquireSpinLock( IRQL & );
    scenario <<
        new CallReturnVoid( "acquireSpinLock" ) <<
			new AssignValue< IRQL >( 123 );

This expectation will assign the value copied on construction,
to the parameter passed to the mock call by reference, using
operator =.

AssignValueToPointer:
---------------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::AssignValueToPointer< typename >( value );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	void fillStats( struct Status * );
    scenario <<
        new CallReturnVoid( "fillStats" ) <<
			new AssignValueToPointer< struct Stats >( Stats(...) );

This expectation is the counterpart of AssignValue: it is used when
the out parameter is passed by pointer (using operator =).

AssignReference:
----------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::AssignReference< typename >( referenceToValue );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	void getCount( int & );
	int toBeAssigned;
    scenario <<
        new CallReturnVoid( "getCount" ) <<
			new AssignReference< int >( toBeAssigned );

This expectation uses operator =, but from a reference to an object.
This is useful in two cases: you need to modify the value assigned
after the expectation has been created (as in common expectations),
or when the class has operator =, but each copy has side effects.

Catergoty 4: Programmable:
--------------------------

There are several template classes that allow custom parameter
verification.

SimplePredicate:
----------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::SimplePredicate< typename, predicateTypename >();

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	class Valid { public: bool operator () ( const struct Data & d ) { return d.valid(); } };
	void sendData( struct Data & );
    scenario <<
        new CallReturnVoid( "sendData" ) <<
			new SimplePredicate< struct Data, Valid >();

PredicateValue:
---------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::PredicateValue< typename, predicateTypename >( predicateObjectToCopy );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	class AddressOf { public:
		bool operator () ( const struct Data & d ) { return & d == expected }
		Data * expected;
		AddressOf( unsigned pointerValue ) { expected = (Data *) pointerValue; }
	};
	void sendData( struct Data & );
    scenario <<
        new CallReturnVoid( "sendData" ) <<
			new SimplePredicate< struct Data, AddressOf >( AddressOf( 1 ) );

This parameter expectation is suitable for cases where the predicate
has context (private data). The predicate will be copied on construction
of the expectation.

PredicateReference:
-------------------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
    new VoodooCommon::Expect::Parameter::PredicateReference< typename, predicateTypename >( predicateObjectToReference );

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	class AddressOf { public:
		bool operator () ( const struct Data & d ) { return & d == expected }
		Data * expected;
		AddressOf( unsigned pointerValue ) { expected = (Data *) pointerValue; }
	};
	void sendData( struct Data & );
    scenario <<
        new CallReturnVoid( "sendData" ) <<
			new SimplePredicate< struct Data, AddressOf >( AddressOf( 1 ) );

This parameter expectation is suitable for cases where the predicate
has context (private data). The predicate will not be copied, only referenced.
This is suitable for cases where the predicate can not be copied.

Custom:
-------
usage:
VoodooCommon::Expect::Scenario scenario;
scenario <<
	new YourClassThatInheritsStrongType();

example:
    using namespace VoodooCommon::Expect;
    using namespace VoodooCommon::Expect::Parameter;
	class Reset : public StrongTyped< Hardware >
	{
	public:
		Reset() : StrongTyped< Hardware >( "Reset" ) {}
	private:
		void compare( Hardware & hardware ) { hardware.reset(); }
	};
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "reset" ) <<
			new Reset();

If you need a different combination of the above properties, or whish
to implement something else over the parameter (i.e., the exmaple above,
or maybe something that requires a combination of the parameters),
you can just inherit StrongTyped< T > and implement your own
void compare( T & ) function. 
