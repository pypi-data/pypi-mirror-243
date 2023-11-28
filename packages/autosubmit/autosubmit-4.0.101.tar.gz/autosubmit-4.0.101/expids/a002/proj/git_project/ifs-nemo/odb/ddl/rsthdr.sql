READONLY;
CREATE VIEW rsthdr AS
SELECT seqno, statid, lat, lon, stalt, sonde_name, sonde_code, date_from, time_from, date_to, time_to, body.offset, body.len
//        1      2     3    4     5         6           7          8          9         10        11       12           13 
FROM hdr
//WHERE
//ORDERBY
;
