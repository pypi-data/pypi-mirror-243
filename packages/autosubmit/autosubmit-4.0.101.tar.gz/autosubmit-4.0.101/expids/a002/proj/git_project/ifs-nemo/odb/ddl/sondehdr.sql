READONLY;
CREATE VIEW sondehdr AS
SELECT seqno,                         //  1
       sonde_code,                    //  2
       sonde_name_1,                  //  3
       sonde_name_2,                  //  3
       sonde_name_3,                  //  3
       sonde_name_4,                  //  3
       sonde_name_5,                  //  3
       sonde_name_6,                  //  3
       sonde_name_7,                  //  3
       sonde_name_8                   //  3
FROM hdr
;
