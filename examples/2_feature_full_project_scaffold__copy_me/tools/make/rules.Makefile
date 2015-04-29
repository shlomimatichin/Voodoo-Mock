define template_per_OBJECT
-include $(1).deps
endef
#endef template_per_OBJECT

define template_per_TARGET
template_per_TARGET_target = $$(if $$(filter %.cpp,$$($(1))), \
									$$(patsubst TARGET_%,build/cpp/%.bin,$(1)), \
									$$(if $$(filter %.c,$$($(1))), \
										$$(patsubst TARGET_%,build/c/%.bin,$(1)), \
										$$(patsubst TARGET_%,build/%.bin,$(1))))
template_per_TARGET_objects = $$(patsubst c/%.c,build/c/%.o, $$(patsubst cpp/%.cpp,build/cpp/%.o,$$($(1))))
all-targets: $$(template_per_TARGET_target)
$$(template_per_TARGET_target): $$(template_per_TARGET_objects) $$($$(patsubst TARGET_%,%,$(1))_TP_OBJECTS)
$$(foreach object,$$(template_per_TARGET_objects), \
	$$(eval $$(call template_per_OBJECT,$$(object))) \
)
endef
#endef template_per_TARGET

$(foreach target,$(filter TARGET_%, $(.VARIABLES)), \
	$(eval $(call template_per_TARGET,$(target))) \
)

define template_per_SHAREDLIBRARY
template_per_SHAREDLIBRARY_target = $$(if $$(filter %.cpp,$$($(1))), \
											$$(patsubst SHAREDLIBRARY_%,build/cpp/%.so,$(1)), \
											$$(patsubst SHAREDLIBRARY_%,build/c/%.so,$(1)))
template_per_SHAREDLIBRARY_objects = $$(patsubst build/%.cp,build/%.o, $$(patsubst build/%.cxx,build/%.o, $$(patsubst c/%.c,build/c/%.o, $$(patsubst cpp/%.cpp,build/cpp/%.o,$$($(1))))))
all-targets: $$(template_per_SHAREDLIBRARY_target)
$$(template_per_SHAREDLIBRARY_target): $$(template_per_SHAREDLIBRARY_objects)
$$(foreach object,$$(template_per_SHAREDLIBRARY_objects), \
	$$(eval $$(call template_per_OBJECT,$$(object))) \
)
endef
#endef template_per_SHAREDLIBRARY

$(foreach target,$(filter SHAREDLIBRARY_%, $(.VARIABLES)), \
	$(eval $(call template_per_SHAREDLIBRARY,$(target))) \
)

build/cpp/%.o: cpp/%.cpp
	$(Q)$(call MKDIR, $(@D))
	@echo 'C++     ' $@
	$(Q)g++ $(CXXFLAGS) $($(subst /,_,$(subst .,_,$*))_o_CFLAGS) -MMD -MF $@.deps -c $< -o $@

build/c/%.o: c/%.c
	$(Q)$(call MKDIR, $(@D))
	@echo 'C       ' $@
	$(Q)gcc $(CFLAGS) $($(subst /,_,$(subst .,_,$*))_o_CFLAGS) -MMD -MF $@.deps -c $< -o $@

build/cpp/%.bin:
	$(Q)$(call MKDIR, $(@D))
	@echo 'LINK++  ' $@
	$(Q)g++ $(LDFLAGS) -o $@ $^ $($*_LDFLAGS) $($*_LIBRARIES)

build/c/%.bin:
	$(Q)$(call MKDIR, $(@D))
	@echo 'LINK    ' $@
	$(Q)gcc $(LDFLAGS) -o $@ $^ $($*_LDFLAGS) $($*_LIBRARIES)

build/cpp/%.so:
	$(Q)$(call MKDIR, $(@D))
	@echo 'LINK++  ' $@
	$(Q)g++ -shared $(LDFLAGS) -o $@ $^ $($*_LDFLAGS) $($*_LIBRARIES)

build/c/%.so:
	$(Q)$(call MKDIR, $(@D))
	@echo 'LINK    ' $@
	$(Q)gcc -shared $(LDFLAGS) -o $@ $^ $($*_LDFLAGS) $($*_LIBRARIES)
