//
//-- ODB/SQL file 'mkglobstab_gpsro.sql'
//
//   Last updated:  16-Mar-2011
//

READONLY;

CREATE VIEW mkglobstab_gpsro AS
  SELECT seqno,timeslot, 
         azimuth,
    FROM index, hdr, sat
    WHERE ( obstype=$limb AND codetype=$gpsro ) OR obstype=$satem OR obstype=$allsky
 ORDERBY timeslot, seqno
;
