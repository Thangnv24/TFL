(set-logic QF_NIA)
(declare-fun t0 () Int)
(declare-fun t1 () Int)
(declare-fun t2 () Int)
(declare-fun t3 () Int)
(declare-fun t4 () Int)
(declare-fun t5 () Int)

(assert (>= (+  t2 (* t5 t0 )) (+  t5 (* t5 t3 )(* t2 t4 )))

(assert (>= (+ (* t3 t0 )t1 ) (+ (* t0 t4 )(* t1 t4 )))

(assert (>= (* t4 t0 ) (+ (* t3 t3 )(* t4 t3 )))

(assert (and (>= t0 1) (>= t1 1) (>= t2 0) (>= t3 1) (>= t4 1) (>= t5 0)))

(assert (or (> (+  t2 (* t5 t0 )) (+  t5 (* t5 t3 )(* t2 t4 ))) (> (+ (* t3 t0 )t1 ) (+ (* t0 t4 )(* t1 t4 ))) (> (* t4 t0 ) (+ (* t3 t3 )(* t4 t3 ))) ))

(assert (and (or (and (> t0 1) (> t1 1)) (> t2 0)) (or (and (> t3 1) (> t4 1)) (> t5 0))))

(check-sat)
(get-model)
(exit)
