(set-logic QF_NIA)
(declare-fun t0 () Int)
(declare-fun t1 () Int)
(declare-fun t2 () Int)
(declare-fun t3 () Int)

(assert (>=  t1   t3 )

(assert (>= t0  t2 )

(assert (and (>= t0 1) (>= t1 0) (>= t2 1) (>= t3 0)))

(assert (or (>  t1   t3 ) (> t0  t2 ) ))

(assert (and (or (> t0 1) (> t1 0)) (or (> t2 1) (> t3 0))))

(check-sat)
(get-model)
(exit)