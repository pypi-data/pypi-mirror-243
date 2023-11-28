READONLY;
CREATE VIEW sondetyperstrhhdr AS
SELECT seqno, sonde_type_code,
//       1           2
       sonde_name_1, sonde_name_2, sonde_name_3, sonde_name_4,
//           3            4             5            6
       sonde_name_5, sonde_name_6, sonde_name_7, sonde_name_8,
//           7            8             9           10
       body.offset, body.len
//          11           12
FROM hdr
//WHERE
//ORDERBY
;
