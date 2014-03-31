BOOL CreateProcessA(
		IN LPCSTR lpApplicationName ,
	   	IN LPSECURITY_ATTRIBUTES lpProcessAttributes ,
		IN LPSECURITY_ATTRIBUTES lpThreadAttributes ,
		IN BOOL bInheritHandles ,
		IN DWORD dwCreationFlags ,
		IN LPVOID lpEnvironment ,
		IN LPCSTR lpCurrentDirectory ,
		IN LPSTARTUPINFOA lpStartupInfo ,
		OUT LPPROCESS_INFORMATION lpProcessInformation );
