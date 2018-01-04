" Vim syntax file
" Language: Quiz
" Maintainer: Jerry Jiang
" Latest Revision: 2018-01-04

syn match quizQuestion "\*.*$"
syn match quizComment "#.*$"

hi link quizQuestion Title
hi link quizComment Comment
