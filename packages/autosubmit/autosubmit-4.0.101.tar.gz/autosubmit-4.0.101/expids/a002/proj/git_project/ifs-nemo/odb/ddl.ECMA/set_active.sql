//
//-- ODB/SQL file 'set_active.sql'
//
//   Last updated:  01/02/2011
//


READONLY;
CREATE VIEW set_active AS
  SELECT seqno, 
         entryno,
         report_status UPDATED,
         datum_status  UPDATED,
         distribtype   UPDATED,
    FROM hdr, radiance, body, radiance_body
    where nobs_averaged IS NOT NULL AND nobs_averaged > 0
;

