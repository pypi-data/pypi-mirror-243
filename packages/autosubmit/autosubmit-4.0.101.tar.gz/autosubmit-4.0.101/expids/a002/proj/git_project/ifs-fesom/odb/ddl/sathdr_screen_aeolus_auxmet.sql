//
//-- ODB/SQL file 'sathdr_screen_aeolus_auxmet.sql'
//
//   Created:  2-Feb-2005
//   Last updated: 12-Jun-2012
//

READONLY; // .. except where  UPDATED qualifier was found

SET $kset = 0;
CREATE VIEW sathdr_screen_aeolus_auxmet AS
  SELECT seqno,                        // r/o; MUST BE FIRST
         retrtype,                   // r/o; MUST BE SECOND
         lev@aeolus_auxmet UPDATED, // possibly updated // distinct from lev@hdr
         ptop              UPDATED, // possibly updated
         pnom              UPDATED, // possibly updated
         ztop              UPDATED, // possibly updated
         znom              UPDATED, // possibly updated
         u                 UPDATED, // possibly updated
         v                 UPDATED, // possibly updated
         t                 UPDATED, // possibly updated
         rh                UPDATED, // possibly updated
         q                 UPDATED, // possibly updated
         cc                UPDATED, // possibly updated
         clwc              UPDATED, // possibly updated
         ciwc              UPDATED, // possibly updated
         error_t           UPDATED, // possibly updated
         error_rh          UPDATED, // possibly updated
         error_p           UPDATED, // possibly updated
  FROM index, hdr, sat, aeolus_hdr, aeolus_auxmet
  WHERE ( ( kset = $kset ) AND ( retrtype@hdr = 1 ) )
;
