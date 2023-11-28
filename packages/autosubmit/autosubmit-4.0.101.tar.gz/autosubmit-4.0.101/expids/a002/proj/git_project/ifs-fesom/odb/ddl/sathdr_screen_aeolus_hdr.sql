//
//-- ODB/SQL file 'sathdr_screen_aeolus_hdr.sql'
//
//   Created:  2-Feb-2005
//   Last updated: 11-Mar-2011
//

READONLY;
SET $kset = 0;
CREATE VIEW sathdr_screen_aeolus_hdr AS
  SELECT seqno,                        // r/o; MUST BE FIRST
         retrtype,                     // r/o; MUST BE SECOND
         aeolus_auxmet.offset    READONLY,
         aeolus_auxmet.len       READONLY,
         aeolus_hdrflag          READONLY,
  FROM index, hdr, sat, aeolus_hdr
  WHERE ( ( kset = $kset ) AND ( retrtype@hdr = 1 ) )
//
;
