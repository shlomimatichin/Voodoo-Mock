#ifndef __VOODOO_EXPECTATION_HOOK_MACROS_H__
#define __VOODOO_EXPECTATION_HOOK_MACROS_H__

#define VOODOO_HOOK_CLASS_0( Name, code ) \
	class Name { \
	public: \
		void operator () () \
		{ \
			code \
		} \
	}; \
	class Name ##Hook: public VoodooCommon::Expect::Hook::Value< Name > {\
	public: \
		Name ##Hook() : \
			VoodooCommon::Expect::Hook::Value< Name >( Name() ) \
		{} \
	};

#define VOODOO_HOOK_CLASS_1( Name, Param, PARAM_NAME, code ) \
	class Name { \
	public: \
		Name( Param param ) : PARAM_NAME( param ) {} \
		Param PARAM_NAME; \
		void operator () () \
		{ \
			code \
		} \
	}; \
	class Name ##Hook: public VoodooCommon::Expect::Hook::Value< Name > {\
	public: \
		Name ##Hook( Param param ) : \
			VoodooCommon::Expect::Hook::Value< Name >( Name( param ) ) \
		{} \
	};

#define VOODOO_HOOK_CLASS_2( Name, Param1, PARAM_NAME1, Param2, PARAM_NAME2, code ) \
	class Name { \
	public: \
		Name( Param1 param1, Param2 param2 ) : \
			PARAM_NAME1( param1 ), PARAM_NAME2( param2 ) {} \
		Param1 PARAM_NAME1; \
		Param2 PARAM_NAME2; \
		void operator () () \
		{ \
			code \
		} \
	}; \
	class Name ##Hook: public VoodooCommon::Expect::Hook::Value< Name > {\
	public: \
		Name ##Hook( Param1 param1, Param2 param2 ) : \
			VoodooCommon::Expect::Hook::Value< Name >( Name( param1, param2 ) ) \
		{} \
	};

#define VOODOO_HOOK_CLASS_3( Name, Param1, PARAM_NAME1, Param2, PARAM_NAME2, Param3, PARAM_NAME3, code ) \
	class Name { \
	public: \
		Name( Param1 param1, Param2 param2, Param3 param3 ) : \
			PARAM_NAME1( param1 ), PARAM_NAME2( param2 ), PARAM_NAME3( param3 ) {} \
		Param1 PARAM_NAME1; \
		Param2 PARAM_NAME2; \
		Param3 PARAM_NAME3; \
		void operator () () \
		{ \
			code \
		} \
	}; \
	class Name ##Hook: public VoodooCommon::Expect::Hook::Value< Name > {\
	public: \
		Name ##Hook( Param1 param1, Param2 param2, Param3 param3 ) : \
			VoodooCommon::Expect::Hook::Value< Name >( Name( param1, param2, param3 ) ) \
		{} \
	};

#define VOODOO_HOOK_CLASS_4( Name, Param1, PARAM_NAME1, Param2, PARAM_NAME2, Param3, PARAM_NAME3, Param4, PARAM_NAME4, code ) \
	class Name { \
	public: \
		Name( Param1 param1, Param2 param2, Param3 param3, Param4 param4 ) : \
			PARAM_NAME1( param1 ), PARAM_NAME2( param2 ), PARAM_NAME3( param3 ), PARAM_NAME4( param4 ) {} \
		Param1 PARAM_NAME1; \
		Param2 PARAM_NAME2; \
		Param3 PARAM_NAME3; \
		Param4 PARAM_NAME4; \
		void operator () () \
		{ \
			code \
		} \
	}; \
	class Name ##Hook: public VoodooCommon::Expect::Hook::Value< Name > {\
	public: \
		Name ##Hook( Param1 param1, Param2 param2, Param3 param3, Param4 param4 ) : \
			VoodooCommon::Expect::Hook::Value< Name >( Name( param1, param2, param3, param4 ) ) \
		{} \
	};

#endif // __VOODOO_EXPECTATION_HOOK_MACROS_H__
