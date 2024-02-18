(set-logic QF_NIA)
(declare-fun t0 () Int)
(declare-fun t1 () Int)
(declare-fun t2 () Int)
(declare-fun t3 () Int)
(declare-fun t4 () Int)

(assert (>=  t2  (+  t4 (* t2 t3 ))))

(assert (>= t0 (* t1 t3 )))

(assert (>= t1 (* t0 t3 )))

(assert (and (>= t0 1) (>= t1 1) (>= t2 0) (>= t3 1) (>= t4 0)))

(assert (or (>=  t2  (+  t4 (* t2 t3 ))) (>= t0 (* t1 t3 )) (>= t1 (* t0 t3 )) ))

(assert (and (or (and (> t0 1) (> t1 1)) (> t2 0)) (or (> t3 1) (> t4 0))))

(check-sat)
(get-model)
(exit)
