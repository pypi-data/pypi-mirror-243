READONLY;
CREATE VIEW rstbody AS
SELECT seqno, press,
//        1     2
       bccf_1, bccf_2, bccf_3, bccf_4, bccf_5, bccf_6, bccf_7, bccf_8, bccf_9, bccf_10, bccf_11, bccf_12, bccf_13
//        3       4       5       6       7       8       9      10      11      12       13       14       15  
FROM  hdr, body
//WHERE
//ORDERBY
;

