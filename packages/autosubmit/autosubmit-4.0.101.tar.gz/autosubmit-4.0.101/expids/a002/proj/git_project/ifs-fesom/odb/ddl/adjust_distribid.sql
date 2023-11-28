//
//-- ODB/SQL file 'adjust_distribid.sql'
//
//   Last updated:  15-Jun-2009
//


CREATE VIEW adjust_distribid AS
  SELECT seqno, 
         target UPDATED,
         distribid 
    FROM hdr,index
    WHERE distribtype = 1 AND report_status.active = 1
    ORDERBY seqno
;
