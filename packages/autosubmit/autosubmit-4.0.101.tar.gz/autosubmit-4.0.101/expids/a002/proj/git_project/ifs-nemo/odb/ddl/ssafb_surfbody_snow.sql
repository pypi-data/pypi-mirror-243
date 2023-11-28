//
//-- ODB/SQL file 'ssafb_surfbody_snow.sql'
//
//   Last updated:  17-May-2002
//


READONLY;

CREATE VIEW ssafb_surfbody_snow AS // SSA-analysis (snow only); ROBODY-part
  SELECT seqno,                      // r/o; Must become first
         entryno, 
         varno,                      // r/o
         datum_status@surfbody_feedback UPDATED,        // possibly updated
         datum_sfc_event@surfbody_feedback UPDATED,        // possibly updated
         fg_depar@surfbody_feedback UPDATED,           // possibly updated
         an_depar@surfbody_feedback UPDATED,           // possibly updated
         snow_depth@surfbody_feedback UPDATED, 
         snow_density@surfbody_feedback UPDATED, 
    FROM hdr, body,surfbody_feedback
   WHERE obstype = $imsims or 
   (obstype = $synop AND ( codetype = $synop_land OR codetype = $synop_land_auto OR codetype = $add_land_surface OR codetype == 170 ))
;
