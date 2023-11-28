READONLY;
CREATE VIEW ecma_hdr_4_rstrhbias AS
SELECT seqno, body.len,
//        1       2
       obstype, codetype, bufrtype, subtype, report_status@hdr,
//        3         4        5        6         7
       lat, lon, statid@hdr, date, time,
//      8    9    10      11    12
       stalt, sonde_type@conv, report_rdbflag@hdr, report_event1@hdr, report_event2@hdr,
//      13      14            15          16           17
FROM hdr, conv
WHERE obstype=5
//ORDERBY date, time
;
