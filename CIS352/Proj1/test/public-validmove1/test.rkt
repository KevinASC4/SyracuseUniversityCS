#lang racket

(require "../../p1.rkt")

(with-output-to-file "output"
                     (lambda ()
                       (print (valid-move? '(X E E
                                              E X E 
                                              O E E) 0 1 'O))))