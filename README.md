### Commands

`cabal run -v0 exe:ft_turing -- tests/resources/valid/unary_mul.json '111*11='`

### TODO

-   [x] Parse arguments
-   [x] Parse JSON file
-   [x] Check valid keys
-   [x] Check valid `name`
-   [x] Check valid `alphabet`
-   [x] Check valid `blank`
-   [x] Check valid `states`
-   [x] Check valid `initial`
-   [x] Check valid `finals`
-   [x] Check valid `transitions`
-   [x] Check valid input
-   [x] Check JSON file has right format
-   [x] .cabal file
-   [x] Detected too many steps (hardcoded)
-   [x] `--max_steps=n` argument (check >= 0)
-   [ ] Detect infinite loops (axbrisse)
-   [ ] Test machine loop
-   [ ] Machine tester
-   [ ] Understanding bonus
-   [ ] Check unknown state as transition keys (amyroshn)
-   [ ] After replacing alphabet type with [char], we do not reject unexpected fields anymore :(, (amyroshn)
-   [ ] Test parsing (files/valid and files/invalid folders + chmod 000 + file that doesn't exist)
-   [ ] Test alias.json -> /dev/random

### Mandatory machines

-   [x] unary_add.json
-   [x] palindrome.json
-   [x] 0ton1ton.json
-   [x] 0to2n.json
-   [ ] inception.json

### Bonus machines

-   [x] unary_mul.json
-   [x] binary_not.json
-   [ ] binary_and.json
-   [ ] binary_or.json
-   [ ] binary_xor.json
-   [ ] binary_add.json

### Learning

-   [ ] https://en.wikipedia.org/wiki/Turing_machine
-   [ ] https://en.wikipedia.org/wiki/Universal_Turing_machine (Probably interesting for inception.json)
-   [ ] https://plato.stanford.edu/entries/turing-machine/
-   [ ] https://www.liafa.jussieu.fr/~carton/Enseignement/Complexite/MasterInfo/Cours/turing.html
-   [ ] [https://www.alanturing.net/turing_archive/pages/reference articles/The Turing-Church Thesis.html](https://www.alanturing.net/turing_archive/pages/reference%20articles/The%20Turing-Church%20Thesis.html)
-   [ ] https://en.wikipedia.org/wiki/Input/output_automaton
-   [ ] https://en.wikipedia.org/wiki/Real_RAM
-   [ ] https://en.wikipedia.org/wiki/Pushdown_automaton
-   [ ] https://en.wikipedia.org/wiki/Stored-program_computer
-   [ ] https://en.wikipedia.org/wiki/Random-access_stored-program_machine

### Haskell

-   [x] https://learnxinyminutes.com/docs/haskell/
-   [ ] https://wiki.haskell.org/Learn_Haskell_in_10_minutes
-   [ ] https://singlelogin.re/book/3502163/054cf9/get-programming-with-haskell.html
-   [ ] https://github.com/MondayMorningHaskell/haskellings
-   [ ] http://learn.hfm.io/
-   [ ] https://www.fpcomplete.com/haskell/learn/
