READONLY;
CREATE VIEW ecma_hdr_4_psbias AS
SELECT seqno, body.len,
//        1       2
       report_rdbflag@hdr, obstype, instrument_type, codetype, report_status@hdr, report_event1@hdr,
//        3         4        5           6        7           8
       lat, lon, statid@hdr, time, date, source,
//      9   10    11      12    13    14
       stalt, orography, anemoht@conv, baroht@conv, numlev, subtype, bufrtype, station_type@conv
//      15      16       17     18       19      20       21           22
FROM hdr, modsurf, conv
WHERE obstype=1 OR obstype=4
ORDERBY date, time
;
