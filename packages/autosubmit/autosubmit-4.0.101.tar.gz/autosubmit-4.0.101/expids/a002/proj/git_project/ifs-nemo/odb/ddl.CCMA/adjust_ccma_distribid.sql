//
//-- ODB/SQL file 'adjust_ccma_distribid.sql'
//
//   Last updated:  4-Dec-2009
//


CREATE VIEW adjust_ccma_distribid AS
  SELECT seqno, 
         target UPDATED,
         distribid 
    FROM hdr,index
    WHERE distribtype = 1 
    ORDERBY seqno
;
