//
//-- ODB/SQL file 'ssa_robhdr_snow.sql'
//
//   Last updated:  17-May-2002
//

READONLY;

CREATE VIEW ssa_robhdr_snow AS // SSA-analysis (snow only); ROBHDR-part
  SELECT seqno,              // r/o; Must become first
         body.len,           // r/o
         date, time,         // r/o
         obstype,            // r/o
         codetype,          // r/o
         lat, lon, statid, stalt  // r/o
    FROM hdr
   WHERE obstype= $imsims or 
   (obstype = $synop AND ( codetype = $synop_land OR codetype = $synop_land_auto OR codetype = $add_land_surface OR codetype == 170 ))
;
