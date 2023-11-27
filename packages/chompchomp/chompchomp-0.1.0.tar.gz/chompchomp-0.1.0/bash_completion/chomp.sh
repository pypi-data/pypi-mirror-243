#!/usr/bin/bash

# WIP
# https://opensource.com/article/18/3/creating-bash-completion-script

function _chomp () {
	cur="${COMP_WORDS[COMP_CWORD]}"
	#prev="${COMP_WORDS[COMP_CWORD-1]}"

	foods=$(yq '[.[].name] | @csv' ~/.chomp/food_library.yml | tr ',' ' ' | tr '"' ' ' | tr '\\' ' ')
	COMPREPLY=($(compgen -W '$foods' -- $cur))
}

complete -F _chomp chomp
