#lang racket

(require "../../p1.rkt")

(with-output-to-file "output"
                     (lambda ()
                       (print (winner? '(O O O 
                                         X X E 
                                         X E E)))))