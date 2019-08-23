# run provided command if current recipe is last in goals
define run_if_last
	@ARR=($(MAKECMDGOALS)); \
	if [ "$@" == "$${ARR[ $${#ARR[@]} - 1 ]}" ]; \
		then eval $1; \
	fi
endef
