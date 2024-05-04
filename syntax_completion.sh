# ╭───────────────────────────────────────╮
# │ Syntax Completion for grocery_shopper │
# ╰───────────────────────────────────────╯
# I asked ChatGPT how to enable auto completion and for an explanation.
_pycomplete() {
    local recipe_dir=~/Documents/grocery_shopper
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(find $recipe_dir -iname "*.yaml" -type f -exec basename {} \; | grep "^$cur") )
}
complete -F _pycomplete grocery_shopper
