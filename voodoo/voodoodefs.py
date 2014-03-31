MOCK_PREFIX = "Mock_"
FAKE_PREFIX = "Fake_"
FAKE_ND_PREFIX = "FakeND_"
VOODOO_CALL = "__voodooCall"

def mockClass( identifier ):
	return MOCK_PREFIX + identifier

def fakeClass( identifier ):
	return FAKE_PREFIX + identifier

def fakeNDClass( identifier ):
	return FAKE_ND_PREFIX + identifier

def templateLine( template ):
	if template == "":
		return template
	return template + "\n"

def returnIfNotVoid( functionDecomposition ):
    if functionDecomposition.returnType == 'void':
        return ""
    else:
        return "return "
