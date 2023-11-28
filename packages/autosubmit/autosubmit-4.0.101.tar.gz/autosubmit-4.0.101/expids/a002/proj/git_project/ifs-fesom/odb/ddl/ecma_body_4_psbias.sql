READONLY;
CREATE VIEW ecma_body_4_psbias AS
SELECT seqno, body.len,
//        1        2
       varno, entryno, vertco_type,
//       3        4         5
       datum_anflag, datum_status@body, datum_rdbflag@body,
//       6        7               8
       datum_event1@body, datum_event2@body, ppcode@conv_body,
//       9             10            11
       vertco_reference_1, obsvalue, fg_depar, fg_error,
//      12                   13        14         15
       vertco_reference_2, an_depar, final_obs_error, obs_error, pers_error,
//      16                   17        18               19        20
       repres_error, biascorr, date, time
//      21            22        23    24
FROM  hdr, body, errstat, conv, conv_body
WHERE obstype=1 OR obstype=4
ORDERBY date, time
;
