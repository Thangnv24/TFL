(set-logic QF_NIA)
(declare-fun t0 () Int)
(declare-fun t1 () Int)
(declare-fun t2 () Int)
(declare-fun t3 () Int)
(declare-fun t4 () Int)

(assert (>= (+  t1 (* t4 t0 ))  t4 ))

(assert (>= (* t2 t0 ) t2))

(assert (>= (* t2 t0 )(* t3 t0 ) t3))

(assert (and (>= t0 1) (>= t1 0) (>= t2 1) (>= t3 1) (>= t4 0)))

(assert (or (>= (+  t1 (* t4 t0 ))  t4 ) (>= (* t2 t0 ) t2) (>= (* t2 t0 )(* t3 t0 ) t3) ))

(assert (and (or (> t0 1) (> t1 0)) (or (and (> t2 1) (> t3 1)) (> t4 0))))

(check-sat)
(get-model)
(exit)
