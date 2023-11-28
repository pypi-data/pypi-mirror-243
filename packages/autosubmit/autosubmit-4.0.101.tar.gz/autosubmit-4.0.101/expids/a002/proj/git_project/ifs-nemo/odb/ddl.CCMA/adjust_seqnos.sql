//
//-- ODB/SQL file 'adjust_seqnos.sql'
//
//   Last updated:  01-Jun-2008
//


CREATE VIEW adjust_seqnos AS
  SELECT seqno, subseqno UPDATED
    FROM hdr
;
