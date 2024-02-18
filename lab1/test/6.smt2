(set-logic QF_NIA)
(declare-fun t0 () Int)
(declare-fun t1 () Int)
(declare-fun t2 () Int)
(declare-fun t3 () Int)
(declare-fun t4 () Int)
(declare-fun t5 () Int)
(declare-fun t6 () Int)
(declare-fun t7 () Int)
(declare-fun t8 () Int)
(declare-fun t9 () Int)

(assert (>= (+  t1 (* t3 t0 )(* t6 t2 t0 ))  t9 ))

(assert (>= (* t4 t2 t0 ) t8))

(assert (>= (* t5 t2 t0 ) t7))

(assert (and (>= t0 1) (>= t1 0) (>= t2 1) (>= t3 0) (>= t4 1) (>= t5 1) (>= t6 0) (>= t7 1) (>= t8 1) (>= t9 0)))

(assert (or (>= (+  t1 (* t3 t0 )(* t6 t2 t0 ))  t9 ) (>= (* t4 t2 t0 ) t8) (>= (* t5 t2 t0 ) t7) ))

(assert (and (or (> t0 1) (> t1 0)) (or (> t2 1) (> t3 0)) (or (and (> t4 1) (> t5 1)) (> t6 0)) (or (and (> t7 1) (> t8 1)) (> t9 0))))

(check-sat)
(get-model)
(exit)
