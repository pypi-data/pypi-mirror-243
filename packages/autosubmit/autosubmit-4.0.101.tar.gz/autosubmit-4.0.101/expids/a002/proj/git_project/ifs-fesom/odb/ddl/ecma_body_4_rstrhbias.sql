READONLY;
CREATE VIEW ecma_body_4_rstrhbias AS
SELECT seqno, body.len,
//        1        2
       varno,
//       3 
       datum_anflag, datum_status@body,
//       4        5
       vertco_reference_1, obsvalue, fg_depar, an_depar,
//       6       7         8         9 
       biascorr, datum_event1@body, datum_event2@body
//      10           11            12
//     repres_error
FROM  hdr, body
//FROM  hdr, body
WHERE obstype=5
//ORDERBY date, time
;
