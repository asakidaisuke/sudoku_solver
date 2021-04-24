(declare-fun x11 () Int)
(declare-fun x12 () Int)
(declare-fun x13 () Int)
(declare-fun x14 () Int)

(assert (and

  (= (+ x11 x12) 16)
  (<= 1 x11) (<= x11 9)
  (<= 1 x12) (<= x12 9)
  (<= 1 x13) (<= x13 9)
  (<= 1 x14) (<= x14 9)

  (distinct  x11 x12 x13 x14)
  ; which is equivalent to 
  ;   x11 != x12 && x11 != x13 && x11 != x14 &&
  ;   x12 != x13 && x12 != x14 && x13 != x14

))
(check-sat)
(get-value (x11 x12 x13 x14))
